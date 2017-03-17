# coding: utf8
from __future__ import unicode_literals, print_function, division

from clldutils.clilib import command
from clldutils.markup import Table


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
    for ds in args.repos.datasets:
        for soc in ds.societies:
            label = '{0} society {1}'.format(ds.id, soc)
            if soc.glottocode not in glottolog:
                args.log.warn('{0} without valid glottocode {1.glottocode}'.format(
                    label, soc))
            elif glottolog[soc.glottocode].family_name == 'Bookkeeping':
                args.log.warn('{0} mapped to Bookkeeping language: {1.glottocode}'.format(
                    label, soc))
