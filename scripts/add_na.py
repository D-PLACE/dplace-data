# coding: utf8
from __future__ import unicode_literals, print_function, division
from collections import defaultdict, OrderedDict
from itertools import groupby
from io import open

from clldutils.dsv import UnicodeWriter, reader


def fill(data, societies):
    lines_old = set(open(data, encoding='utf8').readlines())
    res = defaultdict(list)
    for item in reader(data, dicts=True):
        res[(item['Dataset'], item['VarID'], item['soc_id'])].append(item)
        keys = list(item.keys())
        dataset = item['Dataset']

    societies = {s['soc_id']: s['xd_id'] for s in societies}
    socids = set(societies.keys())
    print(dataset, len(socids), 'societies')

    for var_id, socs in groupby(sorted(res.keys(), key=lambda t: t[1]), key=lambda t: t[1]):
        for soc_id in socids.difference(set(s[2] for s in socs)):
            rec = OrderedDict()
            for key in keys:
                rec[key] = ''
            rec.update(soc_id=soc_id, Dataset=dataset, Code='NA', VarID=var_id)
            if 'xd_id' in keys:
                rec['xd_id'] = societies[soc_id]
            res[(dataset, var_id, soc_id)].append(rec)
        assert sum(len(v) for k, v in res.items() if k[1] == var_id) >= len(socids)

    with UnicodeWriter(data) as fp:
        fp.writerow(keys)
        for key in sorted(res.keys()):
            fp.writerows(row.values() for row in res[key])

    # fix line endings:
    with open(data, encoding='utf8') as fp:
        c = fp.read()

    with open(data, 'w', encoding='utf8') as fp:
        fp.write(c.replace('\r\n', '\n'))

    lines_new = set(open(data, encoding='utf8').readlines())
    assert lines_old.issubset(lines_new)
    print(len(lines_new.difference(lines_old)), 'NA values added')


if __name__ == '__main__':
    for socs, data in [
        ('../csv/EA_header_data_24Feb2016.csv', '../csv/EA_DATA_Stacked.csv'),
        ('../csv/Binford_header_data_24Feb2016.csv', '../csv/Binford_DATA_stacked.csv'),
    ]:
        fill(data, reader(socs, dicts=True))
