# coding: utf8
from __future__ import unicode_literals, print_function, division
from collections import defaultdict, OrderedDict
from itertools import groupby
from io import open

from clldutils.dsv import UnicodeWriter, reader


def fill(dataset, data, socids):
    lines_old = set(open(data, encoding='utf8').readlines())
    res = defaultdict(list)
    for item in reader(data, dicts=True):
        res[(item['Dataset'], item['VarID'], item['soc_id'])].append(item)
        keys = list(item.keys())

    print(dataset, len(socids), 'societies')

    for var_id, socs in groupby(sorted(res.keys(), key=lambda t: t[1]), key=lambda t: t[1]):
        for soc_id in socids.difference(set(s[2] for s in socs)):
            rec = OrderedDict()
            for key in keys:
                rec[key] = ''
            rec.update(soc_id=soc_id, Dataset=dataset, Code='NA', VarID=var_id)
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
    all_socs = set()
    for dataset in ['EA', 'Binford']:
        socids = set(soc['soc_id'] for
                     soc in reader('../csv/%s_societies.csv' % dataset, dicts=True))
        all_socs = all_socs.union(socids)
        fill(dataset, '../csv/%s_data.csv' % dataset, socids)
    fill('environmental', '../csv/environmental_data.csv', all_socs)