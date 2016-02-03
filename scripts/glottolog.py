# coding: utf8
"""
Recreate glottolog data files from the current version published at http://glottolog.org
"""
import sys
import os
import re
import codecs

import requests
from bs4 import BeautifulSoup as bs
from ete2 import Tree


IS_GLOTTOCODE = re.compile(r"""'.* <([a-z0-9]{4}\d{4})>.*'$""")


def clean_tree(tree):  # pragma: no cover
    """Renames taxa to Glottocodes."""
    to_keep = []

    if len(tree.get_leaves()) < 3:  # skip trees with less than three leaves
        print tree.get_leaves()
        return False

    for node in tree.traverse():
        glotto = IS_GLOTTOCODE.findall(node.name)
        if len(glotto) == 1:
            node.name = glotto[0]  # rename to glotto code
            to_keep.append(node.name)

    try:
        tree.prune(to_keep)
    except:
        print "Exception pruning tree, returning un-pruned tree!"
    return True


SQL = """\
select distinct
  l.id,
  l.name,
  l.level,
  l.status,
  l.fid,
  l.latitude,
  l.longitude,
  iso.name
from
  (
    select
      l.pk,
      l.id,
      l.name,
      ll.level,
      ll.status,
      f.id as fid,
      f.name as fname,
      l.latitude,
      l.longitude
    from
      language as l,
      languoid as ll,
      language as f
    where
      l.pk = ll.pk and ll.family_pk = f.pk and l.active = TRUE
  ) as l
left outer join
  (
    select
      i.name, li.language_pk
    from
      languageidentifier as li, identifier as i
    where
      li.identifier_pk = i.pk and i.type = 'iso639-3'
  ) as iso on (iso.language_pk = l.pk)
order by l.id;
"""


GLOTTOLOG_FAMILIES = "http://glottolog.org/glottolog/language.atom?type=families&sSearch_1=Top-level+unit"
SUFFIX = '.glotto.trees'

if __name__ == '__main__':  # pragma: no cover
    urls = {}

    for entry in bs(requests.get(GLOTTOLOG_FAMILIES).text).find_all('entry'):
        urls[entry.find('title').text] = entry.find('id').text

    outdir = sys.argv[1]
    for fname in os.listdir(outdir):
        if fname.endswith(SUFFIX):
            os.remove(os.path.join(outdir, fname))

    for family in sorted(urls):
        url = urls[family]

        filename = os.path.join(outdir, family + SUFFIX)
        print("%30s <- %s" % (family, url))
        newick = requests.get(url + '.newick.txt').text.encode('utf-8')
        # hack to keep ISO code in leaf name
        newick = newick.replace("[", "<").replace("]", ">")
        tree = Tree(newick, format=3)

        if clean_tree(tree):
            newick_string = str(tree.write(format=3))
            with codecs.open(filename, 'w', encoding="utf-8") as handle:
                handle.write("#NEXUS\nBegin taxa;\n")  # write taxa to file
                for leaf in tree.traverse():
                    if str(leaf.name) in newick_string:
                        handle.write(leaf.name)
                        handle.write("\n")
                handle.write(";\nend;")
                # write newick string to file
                handle.write("\nBegin trees;\ntree UNTITLED = ")
                handle.write(newick_string)
                handle.write("\nend;")
