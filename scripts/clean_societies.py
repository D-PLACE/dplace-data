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
    envvars = sorted(
        reader(data_dir.joinpath('csv', 'environmentalVariableList.csv'), dicts=True),
        key=lambda d: d['source'])
    envdata = list(reader(data_dir.joinpath('csv', 'environmental_data.csv'), dicts=True))
    datasets = {r['id']: r for r in reader(data_dir.joinpath('datasets', 'index.csv'), dicts=True)}

    for src, vars in groupby(envvars, lambda d: d['source']):
        with UnicodeWriter(data_dir.joinpath('datasets', src, 'variables.csv')) as vwriter,\
                UnicodeWriter(data_dir.joinpath('datasets', src, 'data.csv')) as dwriter:
            vwriter.writerow('category,id,title,definition,type,units,source,changes,notes'.split(','))
            dwriter.writerow('dataset,soc_id,sub_case,year,var_id,code,comment,references,source_coded_data,admin_comment'.split(','))

            varids = []
            for var in vars:
                #VarID,Name,IndexCategory,VarType,Description,Units,CountOfNonMissingValues,source
                varids.append(var['VarID'])
                vwriter.writerow([
                    var['IndexCategory'],
                    var['VarID'],
                    var['Description'],
                    var['Description'],
                    var['VarType'],
                    var['Units'],
                    datasets[src]['name'],
                    '',
                    ''
                ])

            for r in envdata:
                #Dataset,soc_id,VarID,Code,Comment
                if r['VarID'] in varids:
                    dwriter.writerow([
                        r['Dataset'] if r['Dataset'] != 'Jorgensen' else 'WNAI',
                        r['soc_id'],
                        '',
                        datasets[src]['year'],
                        r['VarID'],
                        r['Code'],
                        r['Comment'],
                        '',
                        '',
                        ''
                    ])


if __name__ == "__main__":
    main(Path(__file__).parent.parent)
