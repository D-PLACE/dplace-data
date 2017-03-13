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
    for ds in ['CRUTS', 'GSHHS', 'GTOPO30', 'Jenkins', 'Kreft', 'MODIS', 'TEOW']:
        data = list(reader(data_dir.joinpath('datasets', ds, 'data.csv')))
        with UnicodeWriter(data_dir.joinpath('datasets', ds, 'data.csv')) as w:
            for i, row in enumerate(data):
                if i == 0:
                    w.writerow(row[1:])
                else:
                    dsid = row.pop(0)
                    if dsid not in ['EA', 'Binford']:
                        try:
                            socid = int(row[0])
                            row[0] = '{0}{1}'.format(dsid, socid)
                        except ValueError:
                            pass
                    w.writerow(row)


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
