# coding: utf8
from __future__ import unicode_literals, print_function, division
from collections import OrderedDict

import attr
from clldutils.dsv import reader, UnicodeWriter

from pydplace.api import Society


def read_win1252(fname, ignore_dataset=False):
    with open(fname, 'rb') as fp:
        c = fp.read()

    with open(fname, 'wb') as fp:
        fp.write(c.replace(b'\x9d', b''))

    for r in reader(fname, dicts=True, encoding='cp1252'):
        if ignore_dataset or (r.get('dataset') == 'SCCS') or (r.get('Dataset') == 'SCCS') or (r.get('Datset') == 'SCCS'):
            yield r


def main():
    socs = read_win1252('ALL_soc_ids_to_lang_wAltNames_sources_5Sept2017_win1252.csv')
    links = {r['soc_id']: r for r in read_win1252('ALL_soc_links_to_other_databases_30Aug2017_win1252.csv')}
    locations = {'SCCS' + r['soc_id']: r for r in reader('../../legacy/LatLong_data.csv', dicts=True)}
    for row in reader('../WNAI/DPLACE_RevisedLatLong_27April2017_inclWNAI_SCCS.csv', dicts=True):
        if row['Dataset'] == 'SCCS':
            locations[row['soc_id']]['Lat'] = row['soc.latitude']
            locations[row['soc_id']]['Long'] = row['soc.longitude']

    with UnicodeWriter('societies.csv') as w:
        w.writerow([f.name for f in attr.fields(Society)])
        for soc in socs:
            kw = {
                'id': soc['soc_id'],
                'glottocode': soc['glottolog_id'],
                'glottocode_comment': 'Lang_assignment_change_notes'}
            for col in [
                'xd_id',
                'pref_name_for_society',
                'ORIG_name_and_ID_in_this_dataset',
                'alt_names_by_society',
                'main_focal_year',
            ]:
                kw[col] = soc[col]

            for col in ['Lat', 'Long', 'origLat', 'origLong', 'Comment']:
                kw[col] = locations[soc['soc_id']][col]

            kw['HRAF_name_ID'] = links[soc['soc_id']]['HRAF_name_ID']
            kw['HRAF_link'] = links[soc['soc_id']]['HRAF_link']
            w.writerow(attr.astuple(Society(**kw)))

    with UnicodeWriter('societies_mapping.csv') as w:
        w.writerow(['id', 'related'])
        for sid, l in links.items():
            rels = []
            for dsid, suffix in [
                ('EA', '1'),
                ('EA', '2'),
                ('Binford', '1'),
                ('Binford', '2'),
                ('Binford', '3'),
                ('SCCS', ''),
                ('WNAI', '1'),
                ('WNAI', '2'),
                ('WNAI', '3'),
                ('WNAI', '4'),
                ('WNAI', '5'),
            ]:
                if dsid == 'SCCS':
                    label = l['{0}_society_equivalent{1}'.format(dsid, suffix)]
                else:
                    label = l['{0}_label_society_equivalent{1}'.format(dsid, suffix)]
                id = l['{0}_id_society_equivalent{1}'.format(dsid, suffix)]
                if label and id:
                    rels.append('{0}: {1} [{2}]'.format(dsid, label, id))
            w.writerow([sid, '; '.join(rels)])

    var_info = {r['source']: r['APA_reference'] for r in
                read_win1252('SCCS_variable_sources_bibtex_to_APA.csv', ignore_dataset=True)}

    with UnicodeWriter('variables.csv') as w:
        fm = OrderedDict([
            ('VarID', 'id'),
            ('Category', 'category'),
            ('VarTitle', 'title'),
            ('VarDefinition', 'definition'),
            ('VarType', 'type'),
            ('UserNotes', 'notes'),
            ('source', 'source'),
            ('VarTitleShort', 'changes'),
            ('Unit', 'units'),
        ])
        w.writerow(fm.values())
        for row in read_win1252('SCCS_Full_VariableList_12Sept2017_win1252.csv'):
            row['VarID'] = 'SCCS' + row['VarID']
            row['VarType'] = row['VarType'].capitalize()
            if row['VarDefinition']:
                row['VarDefinition'] += '\n\n'
            row['VarDefinition'] += var_info.get(row['source'], row['source'])
            w.writerow([row[f] for f in fm.keys()])

    with UnicodeWriter('codes.csv') as w:
        fm = OrderedDict([
            ('VarID', 'var_id'),
            ('Code', 'code'),
            ('CodeDescription', 'description'),
            ('ShortName', 'name'),
        ])
        w.writerow(fm.values())
        for row in read_win1252('SCCS_CodeDescriptions_12Sept2017_win1252.csv'):
            row['VarID'] = 'SCCS' + row['VarID']
            w.writerow([row[f] for f in fm.keys()])

    with UnicodeWriter('data.csv') as w:
        fm = OrderedDict([
            ('soc_id', 'soc_id'),
            ('SubCase', 'sub_case'),
            ('Year', 'year'),
            ('VarID', 'var_id'),
            ('Code', 'code'),
            ('EthnoReferences', 'references'),
            ('AdminComment', 'admin_comment'),
            ('UserComment', 'comment'),
            ('SourceCodedData', 'source_coded_data'),
        ])
        w.writerow(fm.values())
        for row in read_win1252('Full_SCCS_data_12Sept2017_FINAL_329451rows_win1252.csv'):
            row['VarID'] = 'SCCS' + row['VarID']
            w.writerow([row[f] for f in fm.keys()])

    #wnai = BibFile(Path('wnai.bib')).load()
    #sources = BibFile(Path('../sources.bib')).load()
    #m = {}
    #for k, e in wnai.items():
    #    m[e[1]['wnai_key']] = k
    #    if k not in sources:
    #        sources[k] = e
    #BibFile(Path('sources.bib'), sortkey='bibkey').save(sources)

    #source = defaultdict(set)
    #for rec in reader('data.csv', dicts=True):
    #    for r in rec['references'].split('; '):
    #        source[rec['soc_id']].add(r)


if __name__ == '__main__':
    main()
