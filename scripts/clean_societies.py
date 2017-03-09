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
from clldutils.misc import slug
from pyglottolog.api import Glottolog


biome_map = {
    "Mediterranean Forests, Woodlands & Scrub":
        "Mediterranean forests, woodlands, and scrub or sclerophyll forests",
    "Temperate Conifer Forests":
        "Temperate coniferous forests",
    "Mangroves": "Mangrove",
    "Missing data": "NA",
}


def main(data_dir):
    codes = {}
    for var in ['Biome', 'EcoRegion']:
        codes[var] = {
            slug(biome_map.get(r['description'], r['description']).replace('&', 'and')): r
            for r in reader(data_dir.joinpath('datasets', 'TEOW', 'codes.csv'), dicts=True)
            if r['var_id'] == var}

    with UnicodeWriter(data_dir.joinpath('datasets', 'TEOW', 'data.csv')) as writer:
        writer.writerow('dataset, soc_id, sub_case, year, var_id, code, comment, references, source_coded_data, admin_comment'.split(', '))
        for r in reader(data_dir.joinpath('csv', 'environmental_data.csv'), dicts=True):
            if r['VarID'] in ['OlsonBiome', 'OlsonEcoRegion']:
                code = slug(r['Code'].replace('\xa0', ' ').strip())
                if code not in codes[r['VarID'].replace('Olson', '')]:
                    print(r)
                else:
                    writer.writerow([
                        r['Dataset'] if r['Dataset'] != 'Jorgensen' else 'WNAI',
                        r['soc_id'],
                        '',
                        '1988' if r['VarID'] == 'OlsonBiome' else '1981',
                        r['VarID'].replace('Olson', ''),
                        codes[r['VarID'].replace('Olson', '')][code]['code'],
                        r['Comment'],
                        '',
                        '',
                        ''
                    ])


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
