# coding: utf8
"""
- add lat/lon to societies.csv per dataset
- split "*_society_equivalent*" into societies_mapping.json
"""
from __future__ import unicode_literals, print_function, division
import re
from collections import Counter

from clldutils.path import Path
from clldutils.dsv import reader, UnicodeWriter
from clldutils.text import split_text
from clldutils.misc import slug
from pyglottolog.api import Glottolog


def main(data_dir):
    p = re.compile('J[0-9]+$')
    c = Counter()
    for ds, prefix in [('EA', 'EA'), ('Binford', 'B')]:
        data = list(reader(data_dir.joinpath('datasets', ds, 'societies_mapping.csv')))
        with UnicodeWriter(data_dir.joinpath('datasets', ds, 'societies_mapping.csv')) as w:
            for i, row in enumerate(data):
                if i > 0:
                    if row[1]:
                        rels = []
                        for m in row[1].split(';'):
                            assert '[' not in m
                            assert m.endswith(')')
                            parts = m.split('(')
                            assert len(parts) > 1
                            sid = parts[-1][:-1]
                            rem = '('.join(parts[:-1]).strip()
                            assert ':' in rem
                            ds, name = rem.split(':', 1)
                            name = name.strip()
                            c.update([ds])
                            if ds == 'WNAI':
                                assert p.match(sid)
                                sid = sid.replace('J', 'WNAI')
                            elif ds == 'CHIRILA':
                                assert int(sid)
                                sid = 'CHIRILA' + sid
                            rels.append('{0}: {1} [{2}]'.format(ds, name, sid))
                        row[1] = '; '.join(rels)
                w.writerow(row)
    print(c)


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
