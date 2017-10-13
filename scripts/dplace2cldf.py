from __future__ import unicode_literals

import os
from collections import OrderedDict

from six.moves import map

import attr
import pycldf.dataset

import pydplace.api

SRC = '..'
DST = '../cldf'


def registered(cls):
    assert issubclass(cls, BaseConverter)
    try:
        seen = registered.converters
    except AttributeError:
        seen = registered.converters = []
    seen.append(cls)
    return cls


class BaseConverter(object):

    def skip(self, repos):
        return False


class Converter(BaseConverter):

    def __init__(self):
        fields = attr.fields(self._source_cls)
        columns = list(self._itercols(fields, self._convert))

        def extract(s, pairs=[(name, target) for name, target, _ in columns]):
            return {target: getattr(s, name) for name, target in pairs}

        self._extract = extract
        self._add_component_args = ([self._component] +
                                    [args for _, _, args in columns])
    @staticmethod
    def _itercols(fields, convert):
        for f in fields:
            name = f.name
            if name in convert:
                args = convert[name]
                if args is None:
                    continue
                elif hasattr(args, 'setdefault'):
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

    def __call__(self, repos):
        items = map(self._extract, self._iterdata(repos))
        write_kwargs = {self._component['dc:conformsTo']: items}
        return self._add_component_args, write_kwargs


class SkipMixin(object):

    def skip(self, repos, _sentinel=object()):
        return next(iter(self._iterdata(repos)), _sentinel) is _sentinel


@registered
class LanguageTable(SkipMixin, Converter):

    _source_cls = pydplace.api.Society

    _iterdata = staticmethod(lambda repos: repos.societies)

    _component = {
        'url': 'societies.csv',
        'dc:conformsTo': 'http://cldf.clld.org/v1.0/terms.rdf#LanguageTable',
        'tableSchema': {'primaryKey': ['id']},
    }

    _convert = {
        'id': {
            'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#id',
            'datatype': {'base': 'string', 'format': 'B[1-9][0-9]*'},
            'required': True,
        },
        'pref_name_for_society': {
            'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#name',
            'required': True,
        },
        'glottolode': {
            'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#glottocode',
            'required': True,
        },
        'alt_names_by_society': {'separator': ', '},
        'Lat': {
            'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#latitude',
            'datatype': {'base': 'decimal', 'minimum': -90, 'maximum': 90},
        },
        'Long': {
            'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#longitude',
            'datatype': {'base': 'decimal', 'minimum': -180, 'maximum': 180},
        },
    }


@registered
class ParameterTable(Converter):

    _source_cls = pydplace.api.Variable

    _iterdata = staticmethod(lambda repos: repos.variables)

    _component = {
        'url': 'variables.csv',
        'dc:conformsTo': 'http://cldf.clld.org/v1.0/terms.rdf#ParameterTable',
        'tableSchema': {'primaryKey': ['id']}
    }

    _convert = {
        'id': {
            'propertyUrl': 'http://cldf.clld.org/v1.0/terms.rdf#id',
            'required': True
        },
        'category': {'separator': ', '},
        'codes': None,
    }


@registered
class CodeTable(SkipMixin, BaseConverter):

    _component = {
        'url': 'codes.csv',
        'dc:conformsTo': 'http://cldf.clld.org/v1.0/terms.rdf#CodeTable',
        'tableSchema': {'primaryKey': ['var_id', 'code']}
    }

    _convert = {
        'code': {'name': 'code', 'datatype': 'string'},
    }

    _iterdata = staticmethod(lambda repos: (c for v in repos.variables for c in v.codes))

    def __call__(self, repos):
        codes = list(self._iterdata(repos))
        add_component_args = ([self._component] +
                              [self._convert.get(f, f) for f in codes[0]._fields])
        items = (c._asdict() for c in codes)
        write_kwargs = {self._component['dc:conformsTo']: items}
        return add_component_args, write_kwargs


def main():
    repos = pydplace.api.Repos(SRC)
    if not os.path.exists(DST):
        os.mkdir(DST)

    converters = [cls() for cls in registered.converters]
    for src in repos.datasets:
        dst_dir = os.path.join(DST, src.id)
        dst = pycldf.dataset.StructureDataset.in_dir(dst_dir)
        write_args = {}
        for conv in converters:
            if not conv.skip(src):
                add_args, write_kwargs = conv(src)
                dst.add_component(*add_args)
                write_args.update(write_kwargs)
        dst.write(**write_args)


if __name__ == '__main__':
    main()
