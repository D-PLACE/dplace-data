# coding: utf8
from __future__ import unicode_literals, print_function, division

import fiona
from shapely.geometry import Point

from clldutils.clilib import command
from clldutils.markup import Table
from clldutils.jsonlib import update

from pydplace import geo
from pydplace.utils import check_language_file

@command()
def ls(args):
    t = Table('id', 'name', 'type')
    for ds in args.repos.datasets:
        t.append([ds.id, ds.name, ds.type])
    print(t.render(condensed=False, verbose=True))


@command()
def check(args):
    glottolog = {l.id: l for l in
                 args.repos.read_csv('csv', 'glottolog.csv', namedtuples=True)}
    # check datasets
    for ds in args.repos.datasets:
        for soc in ds.societies:
            label = '{0} society {1}'.format(ds.id, soc)
            if soc.glottocode not in glottolog:
                args.log.warn('{0} without valid glottocode {1.glottocode}'.format(
                    label, soc))
            elif glottolog[soc.glottocode].family_name == 'Bookkeeping':
                args.log.warn('{0} mapped to Bookkeeping language: {1.glottocode}'.format(
                    label, soc))
    
    # check phylogenies
    for p in args.repos.phylogenies:
        label = 'Phylogeny {0}'.format(p.id)
        for filename in ('languages.csv', 'source.bib', 'Makefile', 'summary.trees'):
            f = p.dir.joinpath(filename)
            if not f.exists():
                args.log.warn('{0} is missing {1}'.format(label, filename))
            elif filename == 'languages.csv':
                try:
                    check_language_file(f.as_posix())
                except Exception as e:
                    args.log.warn('{0} - languages.csv: {1}'.format(label, e))

@command()
def tdwg(args):
    """
    Assign socities to
    """
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
