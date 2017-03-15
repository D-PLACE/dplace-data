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
from pyglottolog.api import Glottolog
from clldutils.dsv import UnicodeWriter


IS_GLOTTOCODE = re.compile(r"""'.* <([a-z0-9]{4}\d{4})>.*'$""")


def clean_newick(newick):
    # hack to keep ISO code in leaf name
    return newick.replace("[", "<").replace("]", ">")


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
    print 'pruning ...'

    try:
        tree.prune(to_keep)
        print '... done'
    except:
        raise
        print "Exception pruning tree, returning un-pruned tree!"
    return True


GLOTTOLOG_FAMILIES = "http://glottolog.org/glottolog/language.atom?type=families&sSearch_1=Top-level+unit"
SUFFIX = '.glotto.trees'


def trees():
    outdir = os.path.join('..', 'trees')
    urls = {'global': 'http://glottolog.org/static/trees/tree-glottolog-newick.txt'}

    for entry in bs(requests.get(GLOTTOLOG_FAMILIES).text, 'html.parser').find_all('entry'):
        urls[entry.find('title').text] = entry.find('id').text

    for fname in os.listdir(outdir):
        if fname.endswith(SUFFIX):
            os.remove(os.path.join(outdir, fname))

    for family in sorted(urls):
        url = urls[family]
        if not url.endswith('newick.txt'):
            url += '.newick.txt'

        filename = os.path.join(outdir, (family + SUFFIX) if family != 'global' else family + '.trees')
        print("%30s <- %s" % (family, url))
        newick = requests.get(url).text.encode('utf-8')
        if family == 'global':
            tree = Tree()
            for n in newick.split(';\n'):
                subtree = Tree(clean_newick(n + ';'), format=3)
                nodenames = [_n.name for _n in subtree.traverse()]
                if len(nodenames) == len(set(nodenames)) + 1:
                    # FIXME: we must include isolates!
                    # just add single child?
                    tree.add_child(child=Tree(name=subtree.name), dist=1.0)
                    print 'adding isolate', subtree.name
                else:
                    tree.add_child(child=subtree, dist=1.0)
        else:
            tree = Tree(clean_newick(newick), format=3)

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


SQL = """\
select distinct
  languoid.id,
  languoid.name,
  family.id as family_id,
  family.name as family_name,
  iso.name as iso_code
from
  (
    select
      pk, id, name
    from
      language
    where
      active = TRUE
  ) as languoid
left outer join
  (
    select
      f.id, f.name, ll.pk
    from
      languoid as ll, language as f
    where
      ll.family_pk = f.pk
  ) as family on (family.pk = languoid.pk)
left outer join
  (
    select
      i.name, li.language_pk
    from
      languageidentifier as li, identifier as i
    where
      li.identifier_pk = i.pk and i.type = 'iso639-3'
  ) as iso on (iso.language_pk = languoid.pk)
order by languoid.id
"""


def languoids(repos):
    glottolog = Glottolog(repos)
    with UnicodeWriter('../csv/glottolog.csv') as writer:
        writer.writerow(['id', 'name', 'family_id', 'family_name', 'iso_code'])
        for lang in Glottolog(repos).languoids():
            writer.writerow([
                lang.id,
                lang.name,
                lang.lineage[0][1] if lang.lineage else '',
                lang.lineage[0][0] if lang.lineage else '',
                lang.iso or ''
            ])


if __name__ == '__main__':  # pragma: no cover
    cmd = sys.argv[1]
    if cmd == 'trees':
        trees()
    elif cmd == 'languoids':
        languoids(sys.argv[2])
    else:
        raise ValueError(cmd)
