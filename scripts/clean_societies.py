# coding: utf8
"""
- add lat/lon to societies.csv per dataset
- split "*_society_equivalent*" into societies_mapping.json
"""
from __future__ import unicode_literals, print_function, division
import re

from clldutils.path import Path
from clldutils.dsv import reader, UnicodeWriter
from clldutils.text import split_text
from pyglottolog.api import Glottolog


def main(data_dir):
    equiv_pattern = re.compile('(?P<dsid>[^_]+)_society_equivalent')
    locations = {
        r['soc_id']: r for r in reader(data_dir.joinpath('csv', 'LatLong_data.csv'), dicts=True)}
    xd2gc = {r['xd_id']: r['DialectLanguageGlottocode']
             for r in reader(data_dir.joinpath('csv', 'xd_id_to_language.csv'), dicts=True)}
    for d in data_dir.joinpath('datasets').iterdir():
        if d.name in ['EA', 'Binford']:
            rows = list(reader(d.joinpath('societies.csv'), dicts=True))
            for row in rows:
                if row['xd_id'] in xd2gc:
                    del xd2gc[row['xd_id']]

    for k, v in xd2gc.items():
        print(k, v)
    return

    if 1:
        if d.is_dir() and d.joinpath('societies.csv').exists():
            societies = list(reader(d.joinpath('societies.csv'), dicts=True))
            cols = list(societies[0].keys())
            equivalents = {i: equiv_pattern.match(n).group('dsid')
                           for i, n in enumerate(cols) if equiv_pattern.match(n)}
            header = [c for i, c in enumerate(cols) if i not in equivalents]
            loc_cols = 'origLat,origLong,Lat,Long,Comment'.split(',')
            header.extend(loc_cols)
            with UnicodeWriter(d.joinpath('societies.csv')) as writer, \
                    UnicodeWriter(d.joinpath('societies_mapping.csv')) as rwriter:
                writer.writerow(header[1:])
                rwriter.writerow(['id', 'related'])
                for soc in societies:
                    loc = locations.get(soc['soc_id'], {})
                    equivs = ['{0}:{1}'.format(ds, soc.values()[i])
                              for i, ds in equivalents.items() if soc.values()[i]]
                    rwriter.writerow([soc['soc_id'], ';'.join(equivs)])
                    row = [v for i, v in enumerate(soc.values()) if i not in equivalents][1:]
                    row.extend([loc.get(c) for c in loc_cols])
                    writer.writerow(row)


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
