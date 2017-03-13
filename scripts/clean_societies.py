# coding: utf8
"""
- add lat/lon to societies.csv per dataset
- split "*_society_equivalent*" into societies_mapping.json
"""
from __future__ import unicode_literals, print_function, division
import re
from itertools import groupby

from clldutils.path import Path
from clldutils.dsv import reader, UnicodeWriter
from clldutils.text import split_text
from clldutils.misc import slug
from pyglottolog.api import Glottolog


def main(data_dir):
    p = re.compile('J[0-9]+$')
    for ds in ['CRUTS', 'GSHHS', 'GTOPO30', 'Jenkins', 'Kreft', 'MODIS', 'TEOW']:
        data = list(reader(data_dir.joinpath('datasets', ds, 'data.csv')))
        with UnicodeWriter(data_dir.joinpath('datasets', ds, 'data.csv')) as w:
            for i, row in enumerate(data):
                if p.match(row[0]):
                    row[0] = 'WNAI' + row[0][1:]
                w.writerow(row)


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
