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
        self._map = {f.name: f.name for f in fields}
        self._map.update(self._rename)

        self.add_component_args = [self.__class__.__name__] + list(self._itercols(fields))

        def extract(s, pairs=list(six.iteritems(self._map))):
            return {v: getattr(s, k) for k, v in pairs}

        self.write_kwargs = {self.__class__.__name__: map(extract, source)}

    def _itercols(self, fields):
        for f in fields:
            t_name = self._rename.get(f.name, f.name)
            if t_name not in self._component_cols:
                col_args = {'name': t_name}
                if f.convert is float:
                    col_args['datatype'] = 'float'
                yield col_args


class LanguageTable(Converter):

    _component_cols = {'ID', 'Name', 'Latitude', 'Longitude'}

    _source_cls = pydplace.api.Society

    _rename = {
        'id': 'ID',
        'pref_name_for_society': 'Name',
        'Lat': 'Latitude',
        'Long': 'Longitude',
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
