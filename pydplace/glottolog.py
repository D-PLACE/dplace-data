# coding: utf8
"""
Recreate glottolog data files from the current version published at http://glottolog.org
"""
from __future__ import unicode_literals
import re

from clldutils.dsv import UnicodeWriter
from ete3 import Tree
from pyglottolog.api import Glottolog

LABEL = re.compile("'[^\[]+\[([a-z0-9]{4}[0-9]{4})[^']*'")
NEXUS_TEMPLATE = """#NEXUS\nBegin taxa;
{0}
;
end;
Begin trees;
tree UNTITLED = {1}
end;"""


def reference(title, year):
    return "Hammarström, Harald & Forkel, Robert & Haspelmath, Martin. {0}. " \
           "{1}. Jena: Max Planck Institute for the Science of Human History. " \
           "http://glottolog.org/".format(title, year)


def write_tree(tree, fname):
    with fname.open('w', encoding="utf-8") as handle:
        handle.write(NEXUS_TEMPLATE.format(
            '\n'.join(l.name for l in tree.traverse()), tree.write(format=3)))


def trees(langs, outdir, year, title):
    index = []
    outdir = outdir.joinpath('trees')
    languoids = {}
    families = []
    for lang in langs:
        if not lang.lineage:  # a top-level node
            if lang.category.startswith('Pseudo '):
                print('Skipping {0}'.format(lang))
            else:
                families.append(lang)
        languoids[lang.id] = lang

    glob = []
    for family in families:
        newick = LABEL.sub(
            lambda m: m.groups()[0] + ':1', family.newick_node(nodes=languoids).newick)
        newick = "({0});".format(newick)
        tree = Tree(newick, format=3)
        glob.append(newick[:-1])

        if family.level.name == 'family':
            nleaves = len(tree.get_leaves())
            if nleaves < 3:
                print('Skipping family {0} with only {1} leaves'.format(family, nleaves))
            else:
                fname = '{0}.glotto.trees'.format(family.id)
                write_tree(tree, outdir.joinpath(fname))
                index.append([
                    fname,
                    '{0} ({1})'.format(family.name, title),
                    '{0} ({1})'.format(title, family.name),
                    year,
                    reference(title, year)])

    fname = 'global.glotto.trees'
    write_tree(
        Tree("({0});".format(','.join(glob)), format=3), outdir.joinpath(fname))
    index.append([
        fname,
        'Global Classification ({0})'.format(title),
        title,
        year,
        reference(title, year)])
    with UnicodeWriter(outdir.joinpath('index.csv')) as writer:
        writer.writerow(['id', 'name', 'author', 'year', 'reference'])
        writer.writerows(index)


def languoids(langs, outdir):
    with UnicodeWriter(outdir.joinpath('csv', 'glottolog.csv')) as writer:
        writer.writerow(['id', 'name', 'family_id', 'family_name', 'iso_code'])
        for lang in langs:
            writer.writerow([
                lang.id,
                lang.name,
                lang.lineage[0][1] if lang.lineage else '',
                lang.lineage[0][0] if lang.lineage else '',
                lang.iso or ''
            ])


def update(repos, gl_repos, year, title):
    langs = list(Glottolog(gl_repos).languoids())
    languoids(langs, repos.dir)
    trees(langs, repos.dir, year, title)
