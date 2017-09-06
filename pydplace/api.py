# coding: utf8
from __future__ import unicode_literals, print_function, division
import re
from functools import partial
from itertools import groupby, chain

import attr
from clldutils.text import split_text
from clldutils.dsv import reader
from clldutils.path import Path, git_describe
from clldutils.misc import UnicodeMixin
from clldutils import jsonlib
from nexus import NexusReader
from pyglottolog.references import BibFile

comma_split = partial(split_text, separators=',', strip=True, brackets={})
semicolon_split = partial(split_text, separators=';', strip=True, brackets={})


def valid_enum_member(choices, instance, attribute, value):
    if value not in choices:
        raise ValueError(value)


def valid_range(min_, max_, instance, attribute, value):
    if value < min_ or value > max_:
        raise ValueError(value)


@attr.s
class Variable(object):
    category = attr.ib(convert=lambda s: [c.capitalize() for c in comma_split(s)])
    id = attr.ib()
    title = attr.ib()
    definition = attr.ib()
    type = attr.ib(
        validator=partial(valid_enum_member, ['Continuous', 'Categorical', 'Ordinal']))
    source = attr.ib()
    changes = attr.ib()
    notes = attr.ib()
    units = attr.ib(default='')
    codes = attr.ib(default=attr.Factory(list))


@attr.s
class Reference(UnicodeMixin):
    key = attr.ib()
    pages = attr.ib()

    def __unicode__(self):
        res = self.key
        if self.pages:
            res += ':{0}'.format(self.pages)
        return res

    @classmethod
    def from_string(cls, s):
        k, _, p = s.partition(':')
        return cls(k.strip(), p.strip())


@attr.s
class Data(object):
    soc_id = attr.ib()
    sub_case = attr.ib()
    year = attr.ib()
    var_id = attr.ib()
    code = attr.ib()
    comment = attr.ib()
    references = attr.ib(
        convert=lambda s: [Reference.from_string(ss) for ss in semicolon_split(s)])
    source_coded_data = attr.ib()
    admin_comment = attr.ib()


@attr.s
class ObjectWithSource(UnicodeMixin):
    id = attr.ib()
    name = attr.ib()
    year = attr.ib()
    author = attr.ib()
    reference = attr.ib()
    base_dir = attr.ib()
    url = attr.ib()

    @property
    def dir(self):
        return self.base_dir.joinpath(self.id)

    def __unicode__(self):
        return '{0.name} ({0.id})'.format(self)


@attr.s
class RelatedSociety(object):
    dataset = attr.ib(convert=lambda s: s.strip())
    name = attr.ib(convert=lambda s: s.strip())
    id = attr.ib(convert=lambda s: s.strip())

    @classmethod
    def from_string(cls, s):
        match = re.match('([A-Za-z]+):\s*([^\[]+)\[([^\]]+)\]$', s)
        if not match:
            raise ValueError(s)
        return cls(*match.groups())


@attr.s
class RelatedSocieties(object):
    id = attr.ib()
    related = attr.ib(convert=lambda s: [
        RelatedSociety.from_string(ss) for ss in semicolon_split(s)])


@attr.s
class Society(UnicodeMixin):
    id = attr.ib()
    xd_id = attr.ib()
    pref_name_for_society = attr.ib()
    glottocode = attr.ib()
    ORIG_name_and_ID_in_this_dataset = attr.ib()
    alt_names_by_society = attr.ib()
    main_focal_year = attr.ib()
    glottocode_comment = attr.ib()
    HRAF_name_ID = attr.ib()
    HRAF_link = attr.ib()
    origLat = attr.ib(convert=float, default=0)
    origLong = attr.ib(convert=float, default=0)
    Lat = attr.ib(convert=float, validator=partial(valid_range, -90, 90), default=0)
    Long = attr.ib(convert=float, validator=partial(valid_range, -180, 180), default=0)
    Comment = attr.ib(default=None)

    def __unicode__(self):
        return '{0.pref_name_for_society} ({0.id})'.format(self)


@attr.s
class Dataset(ObjectWithSource):
    type = attr.ib(validator=partial(valid_enum_member, ['cultural', 'environmental']))
    description = attr.ib()

    def _items(self, what, **kw):
        fname = self.dir.joinpath('{0}.csv'.format(what))
        return list(reader(fname, **kw)) if fname.exists() else []

    @property
    def data(self):
        return [Data(**d) for d in self._items('data', dicts=True)]

    @property
    def societies(self):
        return [Society(**d) for d in self._items('societies', dicts=True)]

    @property
    def society_relations(self):
        return [
            RelatedSocieties(**d) for d in self._items('societies_mapping', dicts=True)]

    @property
    def variables(self):
        codes = {vid: list(c) for vid, c in groupby(
            sorted(self._items('codes', namedtuples=True), key=lambda c: c.var_id),
            lambda c: c.var_id)}
        return [
            Variable(codes=codes.get(v['id'], []), **v)
            for v in self._items('variables', dicts=True)]


@attr.s
class Taxon(object):
    taxon = attr.ib()
    glottocode = attr.ib()
    xd_ids = attr.ib(convert=comma_split)
    soc_ids = attr.ib(convert=comma_split)


@attr.s
class Phylogeny(ObjectWithSource):
    scaling = attr.ib()

    @property
    def nexus(self):
        return NexusReader(self.trees.as_posix())

    @property
    def newick(self):
        nexus = self.nexus
        nexus.trees.detranslate()
        newick = re.sub(r'\[.*?\]', '', nexus.trees.trees[0])
        try:
            return newick[newick.index('=') + 1:]
        except ValueError:  # pragma: no cover
            return newick

    @property
    def is_glottolog(self):
        return self.id.startswith('glottolog_')

    @property
    def trees(self):
        return self.dir.joinpath('summary.trees')

    @property
    def taxa(self):
        return [Taxon(**d) for d in reader(self.dir.joinpath('taxa.csv'), dicts=True)]


class Repos(UnicodeMixin):
    def __init__(self, dir_):
        self.dir = Path(dir_)
        self.datasets = [
            Dataset(base_dir=self.dir.joinpath('datasets'), **r) for r in
            reader(self.dir.joinpath('datasets', 'index.csv'), dicts=True)]
        self.phylogenies = [
            Phylogeny(base_dir=self.dir.joinpath('phylogenies'), **r) for r in
            reader(self.dir.joinpath('phylogenies', 'index.csv'), dicts=True)]
        self.societies = {
            s.id: s for s in chain.from_iterable(d.societies for d in self.datasets)
        }
        self.variables = {
            v.id: v for v in chain.from_iterable(d.societies for d in self.datasets)
        }
        self.sources = BibFile(self.dir.joinpath('datasets', 'sources.bib'))

    def __unicode__(self):
        return '<D-PLACE data repos {0} at {1}>'.format(git_describe(self.dir), self.dir)

    def path(self, *comps):
        return self.dir.joinpath(*comps)

    def read_csv(self, *comps, **kw):
        return list(reader(self.path(*comps), **kw))

    def read_json(self, *comps):
        return jsonlib.load(self.path(*comps))
    
    def iter_data(self, datasets=None, variables=None, societies=None):
        for ds in self.datasets:
            if datasets and ds.id in datasets:
                for record in ds.data:
                    if variables and record.var_id not in variables:
                        continue
                    if societies and record.soc_id not in societies:
                        continue
                    yield record
