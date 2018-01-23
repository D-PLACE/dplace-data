#!/usr/bin/env python
# dplace_to_cldf.py - convert all dplace datasets to cldf copying from pydplace to pycldf

from __future__ import unicode_literals

import os
import copy
import argparse
import functools
import collections
try:
    from itertools import imap as map
except ImportError:
    map = map

import attr
import pycldf

import pydplace.api

SOURCE, TARGET = '..', '../cldf'

CONVERTERS = []


def register(cls):
    """Register an instance of the decorated converter class for execution.

    Args:
        cls (BaseConverter): class whose instances will be called.

    cls()(<pydplace.api.Dataset instance>) returns a (filename, add_component_args, items) tuple.
    """
    assert issubclass(cls, BaseConverter)
    inst = cls()
    assert callable(inst)
    CONVERTERS.append(inst)
    return cls


class lazyproperty(object):

    def __init__(self, fget):
        self.fget = fget
        for attr in ('__module__', '__name__', '__doc__'):
            setattr(self, attr, getattr(fget, attr))

    def __get__(self, instance, owner):
        if instance is None:
            return self
        result = instance.__dict__[self.__name__] = self.fget(instance)
        return result


class BaseConverter(object):

    def skip(self, dataset):
        return False

    @lazyproperty
    def component(self):
        result = {'url': self.filename}
        result.update(self._component)
        return result


class SkipMixin(object):

    @classmethod
    def skip(cls, dataset, _sentinel=object()):
        return next(iter(cls.iterdata(dataset)), _sentinel) is _sentinel


class Converter(BaseConverter):

    _columns_extra = []

    @staticmethod
    def _column_info(field, convert):
        """Return (name, transform_fuc, target_name, column_spec) for attrs.field, or None to omit."""
        if field.name in convert:
            spec = convert[field.name]
            if spec is None:
                return None
            target = spec.setdefault('name', field.name)
        else:
            target, spec = field.name, {'name': field.name}

        transform_func = lambda x: x
        if 'separator' in spec:
            sep, split = spec['separator']
            spec['separator'] = sep
            if split:
                transform_func = lambda x: x.split(sep)

        if 'datatype' not in spec and field.convert is float:
            spec['datatype'] = 'float'

        return field.name, transform_func, target, spec

    @lazyproperty
    def columns(self):
        fields = attr.fields(self.source_cls)
        columns = (self._column_info(f, self._convert) for f in fields)
        return [c for c in columns if c is not None] + self._columns_extra

    @lazyproperty
    def add_component_args(self):
        return [self.component] + [col_spec for _, _, _, col_spec in self.columns]

    def items(self, dataset):
        for d in self.iterdata(dataset):
            yield {target: transform(getattr(d, name)) for name, transform, target, _ in self.columns}

    def __call__(self, dataset):
        return self.filename, self.add_component_args, self.items(dataset)


Separator = collections.namedtuple('Separator', ['sep', 'split'])


class Cldf(object):

    base = 'http://cldf.clld.org/v1.0/terms.rdf#'

    def __getattr__(self, term):
        return self.base + term


cldf = Cldf()


@register
class LanguageTable(SkipMixin, Converter):

    filename = 'societies.csv'

    source_cls = pydplace.api.Society

    iterdata = staticmethod(lambda dataset: dataset.societies)

    _component = {
        'dc:conformsTo': cldf.LanguageTable,
        'tableSchema': {'primaryKey': ['id']},
    }

    _convert = {
        'id': {'propertyUrl': cldf.id, 'required': True},
        'xd_id': {'datatype': {'base': 'string', 'format': r'xd\d+'}, 'required': True},
        'pref_name_for_society': {'propertyUrl': cldf.name, 'required': True},
        'glottocode': {'propertyUrl': cldf.glottocode,'required': True},
        'ORIG_name_and_ID_in_this_dataset': {'required': True},
        'alt_names_by_society': {'separator': Separator(', ', split=True)},
        'main_focal_year': {'datatype': 'integer','null': 'NA'},
        'HRAF_name_ID': {'datatype': {'base': 'string', 'format': r'.+ \([^)]+\)'}},
        'HRAF_link': {'datatype': {'base': 'string', 'format': r'http://.+|in process'}},
        'origLat': {
            'datatype': {'base': 'decimal', 'minimum': -90, 'maximum': 90},
            'required': True,
        },
        'origLong': {
            # FIXME: EA/societies.csv:1279:11
            'datatype': {'base': 'decimal', 'minimum': -190, 'maximum': 180},
            'required': True,
        },
        'Lat': {
            'propertyUrl': cldf.latitude,
            'datatype': {'base': 'decimal', 'minimum': -90, 'maximum': 90},
            'required': True,
        },
        'Long': {
            'propertyUrl': cldf.longitude,
            'datatype': {'base': 'decimal', 'minimum': -180, 'maximum': 180},
            'required': True,
        },
        'Comment': {'propertyUrl': cldf.comment},
    }


@register
class LangugageRelatedTable(SkipMixin, Converter):

    filename = 'societies_mapping.csv'

    source_cls = pydplace.api.RelatedSocieties

    @staticmethod
    def iterdata(dataset, make_ns=argparse.Namespace):
        for r in dataset.society_relations:
            for rs in r.related:
                yield make_ns(id=r.id, related_dataset=rs.dataset, related_name=rs.name, related_id=rs.id)

    _component = {
        'tableSchema': {
            'foreignKeys': [
                {'columnReference': 'id',
                'reference': {'resource': 'societies.csv', 'columnReference': 'id'}},
            ],
        },
    }

    _convert = {
        'id': {'propertyUrl': cldf.languageReference, 'required': True},
        'related': None,
    }

    _columns_extra= [
        ('related_dataset', (lambda x: x), 'related_dataset', {'name': 'related_dataset', 'required': True}),
        ('related_name', (lambda x: x), 'related_name', {'name': 'related_name', 'required': True}),
        ('related_id', (lambda x: x), 'related_id', {'name': 'related_id', 'required': True}),
    ]


@register
class ParameterTable(Converter):

    filename = 'variables.csv'

    source_cls = pydplace.api.Variable

    iterdata = staticmethod(lambda dataset: dataset.variables)

    _component = {
        'dc:conformsTo': cldf.ParameterTable,
        'tableSchema': {'primaryKey': ['id']}
    }

    _convert = {
        'id': {'propertyUrl': cldf.id, 'required': True},
        'category': {'separator': Separator(', ', split=False), 'required': True},
        'title': {'propertyUrl': cldf.name,'required': True},
        'definition': {'propertyUrl': cldf.description},
        'type': {
            'datatype': {
                'base': 'string',
                'format': '|'.join(['Categorical', 'Ordinal', 'Continuous']),
            },
            'required': True,
        },
        'source': {'propertyUrl': cldf.source},
        'notes': {'propertyUrl': cldf.comment},
        'codes': None,
    }


@register
class CodeTable(SkipMixin, BaseConverter):

    filename = 'codes.csv'

    iterdata = staticmethod(lambda dataset: (c for v in dataset.variables for c in v.codes))

    _component = {
        'dc:conformsTo': cldf.CodeTable,
        'tableSchema': {
            'primaryKey': ['var_id', 'code'],
            'foreignKeys': [
                {'columnReference': 'var_id',
                'reference': {'resource': 'variables.csv', 'columnReference': 'id'}},
            ],
        },
    }

    _convert = {
        'var_id': {'propertyUrl': cldf.parameterReference, 'required': True},
        'code': {
            # FIXME: MODIS/data.csv:5884:6
            'datatype': {'base': 'string', 'format': r'-?\d+(?:.\d+)?(?:E[+-]\d+)?|NA'},
            'required': True,
        },
        'description': {'propertyUrl': cldf.description},
        'name': {'propertyUrl': cldf.name, 'required': True},
    }

    @staticmethod
    def _column_spec(fieldname, convert):
        try:
            spec = convert[fieldname]
        except KeyError:
            spec = {'name': fieldname}
        else:
            spec.setdefault('name', fieldname)
        return spec

    def column_specs(self, dataset):
        fieldnames = next(self.iterdata(dataset))._fields
        return [self._column_spec(f, self._convert) for f in fieldnames]

    def add_component_args(self, dataset):
        return [self.component] + self.column_specs(dataset)

    def items(self, dataset):
        for c in self.iterdata(dataset):
            yield c._asdict()

    def __call__(self, dataset):
        return self.filename, self.add_component_args(dataset), self.items(dataset)


@register
class ValueTable(Converter):

    filename = 'data.csv'

    source_cls = pydplace.api.Data

    @staticmethod
    def iterdata(dataset, make_dict=functools.partial(attr.asdict, recurse=False), make_ns=argparse.Namespace):
        for d in dataset.data:
            d = make_ns(**make_dict(d))
            d.references = [str(r) for r in d.references]
            yield d

    _component = {
        'dc:conformsTo': cldf.ValueTable,
        'tableSchema': {
            'primaryKey': 'id',  # ['soc_id', 'sub_case', 'year', 'var_id', 'code', 'references']
            'foreignKeys': [
                {'columnReference': 'soc_id',
                'reference': {'resource': 'societies.csv', 'columnReference': 'id'}},
                # NOTE: code is only a reference for catgorical variables
                # TODO: consider putting raw values in a 'value' column
                #{'columnReference': ['var_id', 'code'],
                #'reference': {'resource': 'codes.csv', 'columnReference': ['var_id', 'code']}},
            ],
        },
    }

    _component_extra = [{'name': 'id', 'propertyUrl': cldf.id, 'required': True}]

    _convert = {
        'soc_id': {'propertyUrl': cldf.languageReference, 'required': True},
        'sub_case': {'null': None, 'required': True},
        'year': {
            'datatype': {'base': 'string', 'format': r'-?\d+(?:-\d+)?|(?:NA)?'},
            'null': None,
            'required': True,
        },
        'var_id': {'propertyUrl': cldf.parameterReference, 'required': True},
        'code': {
            'propertyUrl': cldf.codeReference,
            'datatype': CodeTable._convert['code']['datatype'],
            'required': True,
        },
        'comment': {'propertyUrl': cldf.comment},
        'references': {
            'propertyUrl': cldf.source,
            'separator': Separator('; ', split=False),
            'null': None,
            'required': True,
        },
    }

    def items(self, dataset):
        for i, d in enumerate(super(ValueTable, self).items(dataset), 1):
            d['id'] = i
            yield d

    def __call__(self, dataset):
        component = self.add_component_args[0]
        if LanguageTable.skip(dataset):
            # drop data.csv fks to societies.csv if there is none
            component = copy.deepcopy(component)
            reduced = [f for f in component['tableSchema']['foreignKeys']
                       if f['reference']['resource'] != LanguageTable.filename]
            component['tableSchema']['foreignKeys'] = reduced
        add_component_args = [component] + self._component_extra + self.add_component_args[1:]
        return self.filename, add_component_args, self.items(dataset)


def main(source_dir=SOURCE, target_dir=TARGET):
    """Write pydplace.api.Datasets from ``source_dir`` to pycldf.StructureDatasets under ``target_dir``."""
    if not os.path.exists(target_dir):
        os.mkdir(target_dir)

    repo = pydplace.api.Repos(source_dir)
    for source_ds in repo.datasets:
        print(source_ds)
        convert(source_ds, target_dir=os.path.join(target_dir, source_ds.id))


def convert(source_ds, target_dir, converters=CONVERTERS):
    target_ds = pycldf.StructureDataset.in_dir(target_dir, empty_tables=True)
    for c in converters:
        if not c.skip(source_ds):
            filename, add_args, items = c(source_ds)
            target_ds.add_component(*add_args)
            target_ds[filename].write(items)
    target_ds.write_metadata()
    target_ds.validate()


if __name__ == '__main__':
    main()
