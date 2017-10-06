from __future__ import unicode_literals

import os

import six
import attr
import pycldf.dataset

import pydplace.api

SRC = '..'
DST = '../cldf'


class Converter(object):

    def __init__(self, source):
        fields = attr.fields(self._source_cls)
        columns = list(self._itercols(fields, self._convert))

        self.add_component_args = ([self._component] +
                                   [args for _, _, args in columns])

        def extract(s, pairs=[(name, target) for name, target, _ in columns]):
            return {target: getattr(s, name) for name, target in pairs}

        self.write_kwargs = {self._component['dc:conformsTo']: map(extract, source)}

    @staticmethod
    def _itercols(fields, convert):
        for f in fields:
            name = f.name
            if name in convert:
                args = convert[name]
                if hasattr(args, 'setdefault'):
                    target = args.setdefault('name', name)
                else:
                    target = args
                    args = {'name': target}
            else:
                args = {'name': name}
                target = name
            if 'datatype' not in args:
                args['datatype'] = 'float' if f.convert is float else 'string'
            yield name, target, args


class LanguageTable(Converter):

    _source_cls = pydplace.api.Society

    _component = {
        'url': 'languages.csv',
        'dc:conformsTo': 'http://cldf.clld.org/v1.0/terms.rdf#LanguageTable',
        'tableSchema': {'primaryKey': ['id']},
    }

    _convert = {
        'id': {'propertyUrl': 'http://purl.org/dc/terms/identifier'},
        'pref_name_for_society': {},
        'Lat': {
            'propertyUrl': 'http://www.w3.org/2003/01/geo/wgs84_pos#lat',
            'datatype': {'base': 'decimal', 'minimum': -90, 'maximum': 90},
        },
        'Long': {
            'propertyUrl': 'http://www.w3.org/2003/01/geo/wgs84_pos#long',
            'datatype': {'base': 'decimal', 'minimum': -180, 'maximum': 180},
        },
    }


def main():
    repos = pydplace.api.Repos(SRC)
    if not os.path.exists(DST):
        os.mkdir(DST)

    for src in repos.datasets:
        dst_dir = os.path.join(DST, src.id)
        dst = pycldf.dataset.StructureDataset.in_dir(dst_dir)
        write_args = {}
        if src.societies:
            table = LanguageTable(src.societies)
            dst.add_component(*table.add_component_args)
            write_args.update(table.write_kwargs)
        dst.write(**write_args)


if __name__ == '__main__':
    main()
