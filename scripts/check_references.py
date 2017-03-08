#!/usr/bin/env python
#coding=utf-8
"""..."""
__author__ = 'Simon J. Greenhill <simon@simon.net.nz>'
__copyright__ = 'Copyright (c) 2016 Simon J. Greenhill'
__license__ = 'New-style BSD'

import re
import csv
import codecs
import Levenshtein
from collections import defaultdict

def csv_dict_reader(fname):
    with codecs.open(fname, 'r', encoding="utf8") as fp:
        for dict_row in csv.DictReader(fp, dialect="excel"):
            for k in dict_row:
                if dict_row[k] is None:
                    continue
                dict_row[k] = dict_row[k].strip()
            yield dict_row


def nopage(k):
    return k.split(":")[0]

def check1(refs):
    # check 1 :: check competing refs
    errors = 0
    for r in sorted(refs):
        if len(refs[r]) > 1:
            print("%s\t%d" % (r.ljust(50), len(refs[r])))
            for var in refs[r]:
                #out = "\n".join(
                #    textwrap.wrap(
                #        var, initial_indent="  ", subsequent_indent='    '
                #    )
                #)
                print("    %s" % var)
                errors += 1
            print("")


    print("")
    print(len(refs))
    print("ERRORS", errors)

def check2(refs, threshold=0.9):
    errors = 0
    is_year = re.compile(r"""\d{4}[\w{1}]?""")
    
    def check_year(ref1, ref2):
        return is_year.findall(ref1) == is_year.findall(ref2)

    for ref in sorted(refs):
        simil = [r for r in refs if r != ref]
        # check distance
        simil = [
            r for r in simil if Levenshtein.ratio(ref, r) > threshold
        ]
        # check years
        simil = [r for r in simil if check_year(ref, r)]
        
        # check years
        if len(simil):
            print(ref)
            for s in simil:
                print("\t%s" % s)
            print("")
            errors += 1

    print("Errors: %d" % errors)
    return

if __name__ == '__main__':

    refs = defaultdict(set)
    for r in csv_dict_reader('BinfordReferenceMapping_3Mar2016_utf8.csv'):
        short = nopage(r['ShortRef_w_AND_wout_pp'])
        refs[short].add(r['LongRef'])
    
    for r in csv_dict_reader('ReferenceMapping_1Mar2016.csv'):
        refs[r['ReferenceShort']].add(r['ReferenceComplete'])
    
    #check1(refs)
    check2(refs)
