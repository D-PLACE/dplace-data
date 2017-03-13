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
    for ds, prefix in [('EA', 'EA'), ('Binford', 'B')]:
        data = list(reader(data_dir.joinpath('datasets', ds, 'codes.csv')))
        with UnicodeWriter(data_dir.joinpath('datasets', ds, 'codes.csv')) as w:
            for i, row in enumerate(data):
                if i > 0:
                    row[0] = prefix + row[0].zfill(3)
                w.writerow(row)


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
