# coding: utf8
"""
Recreate glottolog data files from the current version published at http://glottolog.org
"""
from __future__ import unicode_literals
import re
from itertools import groupby

from clldutils.dsv import UnicodeWriter, reader
from ete3 import Tree
from pyglottolog.api import Glottolog

NEXUS_TEMPLATE = """#NEXUS
Begin taxa;
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


def write_tree(tree, fname, taxa_in_dplace, societies_by_glottocode):
    if not fname.exists():
        fname.mkdir()
    tree.prune([n.encode('ascii') for n in taxa_in_dplace], preserve_branch_length=True)
    with fname.joinpath('summary.trees').open('w', encoding="utf-8") as handle:
        handle.write(NEXUS_TEMPLATE.format(
            '\n'.join(l.name for l in tree.traverse()), tree.write(format=3)))
    with UnicodeWriter(fname.joinpath('taxa.csv')) as writer:
        writer.writerow([
            'taxon',
            'glottocode',
            'xd_ids',
            'soc_ids'])
        for gc in sorted(taxa_in_dplace):
            socs = societies_by_glottocode[gc]
            writer.writerow([
                gc,
                gc,
                ', '.join(set(s.xd_id for s in socs)),
                ', '.join(s.id for s in socs)])
    return tree


def trees(societies_by_glottocode, langs, outdir, year, title):
    label_pattern = re.compile("'[^\[]+\[([a-z0-9]{4}[0-9]{4})[^']*'")

    def rename(n):
        n.name = label_pattern.match(n.name).groups()[0]
        n.length = 1

    glottocodes = set(societies_by_glottocode.keys())
    glottocodes_in_global_tree = set()
    index = {}
    outdir = outdir.joinpath('phylogenies')
    languoids = {}
    families = []
    for lang in langs:
        if not lang.lineage:  # a top-level node
            if not lang.category.startswith('Pseudo '):
                families.append(lang)
        languoids[lang.id] = lang

    glob = Tree()
    for family in families:
        node = family.newick_node(nodes=languoids)
        node.visit(rename)
        taxa_in_tree = set(n.name for n in node.walk())
        taxa_in_dplace = glottocodes.intersection(taxa_in_tree)
        if not taxa_in_dplace:
            continue

        newick = "({0});".format(node.newick)
        tree = Tree(newick, format=3)

        if family.level.name == 'family':
            fname = 'glottolog_{0}'.format(family.id)
            tree = write_tree(
                tree,
                outdir.joinpath(fname),
                taxa_in_dplace,
                societies_by_glottocode)
            glottocodes_in_global_tree = glottocodes_in_global_tree.union(
                set(n.name for n in tree.traverse()))
            index[fname] = dict(
                id=fname,
                name='{0} ({1})'.format(family.name, title),
                author='{0} ({1})'.format(title, family.name),
                year=year,
                scaling='',
                reference=reference(title, year),
                url='http://glottolog.org/resource/languoid/id/{}'.format(family.id))
                
        else:
            glottocodes_in_global_tree = glottocodes_in_global_tree.union(taxa_in_tree)
        glob.add_child(tree)

    fname = 'glottolog_global'
    
    write_tree(
        glob,
        outdir.joinpath(fname),
        glottocodes_in_global_tree.intersection(glottocodes),
        societies_by_glottocode)
    index[fname] = dict(
        id=fname,
        name='Global Classification ({0})'.format(title),
        author=title,
        year=year,
        scaling='',
        reference=reference(title, year),
        url='http://glottolog.org/')

    index_path = outdir.joinpath('index.csv')
    phylos = list(reader(index_path, dicts=True))
    with UnicodeWriter(index_path) as writer:
        header = list(phylos[0].keys())
        writer.writerow(header)
        for phylo in phylos:
            if phylo['id'] in index:
                writer.writerow([index[phylo['id']][k] for k in header])
                del index[phylo['id']]
            else:
                writer.writerow(phylo.values())

        for id_, spec in sorted(index.items()):
            writer.writerow([spec[k] for k in header])


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
    societies_by_glottocode = {
        gc: list(socs) for gc, socs in groupby(
            sorted(repos.societies.values(), key=lambda s: s.glottocode),
            lambda s: s.glottocode)}
    langs = list(Glottolog(gl_repos).languoids())
    languoids(langs, repos.dir)
    trees(societies_by_glottocode, langs, repos.dir, year, title)
