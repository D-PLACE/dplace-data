# coding: utf8
from __future__ import unicode_literals, print_function, division

from ete3 import Tree
from ete3.parser.newick import NewickError

from clldutils.clilib import command, ParserError
from clldutils.path import write_text
from clldutils.markup import Table
from clldutils.jsonlib import update
from clldutils.dsv import UnicodeWriter

from pydplace import geo
from pydplace import glottolog


@command()
def bib(args):
    def visit(e):
        a, _, y = e.fields['key'].partition(', ')
        e.fields['key'] = '{0} ({1})'.format(a, y)

    args.repos.sources.visit(visit)


@command()
def readme(args):
    md = ['# Sources', '']
    for datatype in ['datasets', 'phylogenies']:
        md.append('\n## {0}\n'.format(datatype.capitalize()))
        t = Table('Name', 'Reference')
        for obj in getattr(args.repos, datatype):
            if not obj.id.startswith('glottolog_') or obj.id == 'glottolog_global':
                t.append([
                    '[{0}]({1}/{2})'.format(obj.name, datatype, obj.id),
                    obj.reference])
        md.append(t.render(condensed=False))
    write_text(args.repos.dir.joinpath('SOURCES.md'), '\n'.join(md))


@command()
def ls(args):
    t = Table('id', 'name', 'type', 'variables', 'societies')
    for ds in args.repos.datasets:
        t.append([ds.id, ds.name, ds.type, len(ds.variables), len(ds.societies)])
    print(t.render(condensed=False, verbose=True))


@command()
def check(args):
    glottolog = {l.id: l for l in
                 args.repos.read_csv('csv', 'glottolog.csv', namedtuples=True)}

    sources = set(e.key for e in args.repos.sources.iterentries())
    socids, xdids, varids = set(), set(), set()
    for ds in args.repos.datasets:
        for soc in ds.societies:
            if soc.id in socids:
                args.log.error('duplicate society ID: {0}'.format(soc.id))
            xdids.add(soc.xd_id)
            socids.add(soc.id)
            label = '{0} society {1}'.format(ds.id, soc)
            if soc.glottocode not in glottolog:
                args.log.warn('{0} without valid glottocode {1.glottocode}'.format(
                    label, soc))
            elif glottolog[soc.glottocode].family_name == 'Bookkeeping':
                args.log.warn('{0} mapped to Bookkeeping language: {1.glottocode}'.format(
                    label, soc))
        # are there duplicate variables?
        for var in ds.variables:
            if var.id in varids:
                args.log.error('duplicate variable ID: {0}'.format(var.id))
            varids.add(var.id)
        # are there undefined variables?
        undefined = set([r.var_id for r in ds.data if r.var_id not in varids])
        for u in undefined:
            args.log.error('undefined variable ID: {0}'.format(u))

        for d in ds.data:
            for ref in d.references:
                if ref.key not in sources:
                    args.log.error('undefined source key "{0}" referenced in {1}'.format(
                        ref.key, ds.id))

    for p in args.repos.phylogenies:
        for taxon in p.taxa:
            if taxon.glottocode and taxon.glottocode not in glottolog:
                args.log.error('{0}: invalid glottocode {1}'.format(p.id, taxon.glottocode))
            for socid in taxon.soc_ids:
                if socid not in socids:
                    args.log.error('{0}: invalid soc_id {1}'.format(p.id, socid))
            for xdid in taxon.xd_ids:
                if xdid not in xdids:
                    args.log.error('{0}: invalid xd_id {1}'.format(p.id, xdid))
        
        if not p.nexus:
            args.log.error('{0}: unable to load summary.trees'.format(p.id))
        
        try:
            Tree(p.newick, format=1)
        except NewickError as e:
            args.log.error('{0}: invalid newick tree from summary.trees: {1}'.format(p.id, e))


@command(name='glottolog')
def glottolog_(args):
    """Update data derived from Glottolog

    dplace glottolog PATH/TO/GLOTTOLOG/REPOS YEAR VERSION
    """
    if len(args.args) != 3:
        raise ParserError('not enough arguments')
    year, version = args.args[1:3]
    title = "Glottolog {0}".format(version)
    glottolog.update(args.repos, args.args[0], year, title)


@command()
def tdwg(args):
    """
    Assign socities to TDWG regions
    """
    try:
        import fiona
        from shapely.geometry import Point
    except ImportError:
        args.log.error('fiona and shapely must be installed for this command')
        return

    def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
        return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

    with fiona.collection(
            args.repos.path("geo", "level2-shape/level2.shp").as_posix(), "r") as source:
        regions = [f for f in source]

    with update(
        args.repos.path("geo", "societies_tdwg.json"), default={}, indent=4
    ) as soc_tdwg:
        for ds in args.repos.datasets:
            for soc in ds.societies:
                spec = soc_tdwg.get(
                    soc.id, dict(lat=soc.Lat, lon=soc.Long, name=None, code=None))
                if isclose(spec['lat'], soc.Lat) \
                        and isclose(spec['lon'], soc.Long) \
                        and spec['code']:
                    continue

                region, dist = geo.match(Point(spec['lon'], spec['lat']), regions)
                spec['name'] = region['properties']['REGION_NAM']
                spec['code'] = region['properties']['TDWG_CODE']

                if dist == 0:
                    args.log.info('{0} contained in region {1}'.format(soc, spec['name']))
                else:
                    args.log.warn(
                        'assigning {0} to nearest region {1}, distance {2}'.format(
                            soc, region['properties']['REGION_NAM'], dist))

                soc_tdwg[soc.id] = spec


@command()
def extract(args):
    import argparse
    usage = """
    dplace %(prog)s - extracts subsets of data for further processing.
    
    To filter societies:
    
    > dplace %(prog)s --society Cj4,Cj5,Cj6 output.csv

    To filter societies on a given tree:
    
    > dplace %(prog)s --tree gray_et_al2009 output.csv
    
    To filter societies only from a given dataset:
    
    > dplace %(prog)s --dataset EA output.csv
    """
    parser = argparse.ArgumentParser(prog='extract', usage=usage)
    parser.add_argument('filename', help='filename', default=None)
    parser.add_argument('--society', help='restrict to these society ids (x,y,z)', default=None)
    parser.add_argument('--tree', help='restrict to this tree', default=None)
    parser.add_argument('--dataset', help='restrict to these datasets (x,y,z)', default=None)
    parser.add_argument('--variable', help='restrict to thes dataset (x,y,z)', default=None)
    xargs = parser.parse_args(args.args)
    
    datasets = xargs.dataset.split(",") if xargs.dataset else None
    variables = xargs.variable.split(",") if xargs.variable else None
    societies = xargs.society.split(",") if xargs.society else None
    
    # get tree if given
    if xargs.tree:
        # get trees
        trees = {t.id: t for t in args.repos.phylogenies}
        try:
            tree = trees.get(xargs.tree)
        except IndexError:
            raise SystemExit("Failed to find Tree %s" % xargs.tree)
        societies = [
            s for sublist in [t.soc_ids for t in tree.taxa] for s in sublist
        ]
    
    with UnicodeWriter(f=xargs.filename) as out:
        header = [
            'ID',
            'XD_ID',
            'Glottocode',
            'Name',
            'OriginalName',
            'FocalYear',
            'Latitude',
            'Longitude',
            'Variable',
            'Value'
        ]
        out.writerow(header)
        
        for record in args.repos.iter_data(
            datasets=datasets, variables=variables, societies=societies):
            
            s = args.repos.societies.get(record.soc_id, None)
            if s is None:
                # we get these warnings as we are currently missing the SCCS
                # and WNAI data
                args.log.warn("Missing society definition for %s" % record.soc_id)
                continue
            
            row = [
                s.id,
                s.xd_id,
                s.glottocode,
                s.pref_name_for_society,
                s.ORIG_name_and_ID_in_this_dataset,
                s.main_focal_year, 
                s.Lat,
                s.Long,
                record.var_id,
                record.code
            ]
            out.writerow(row)
