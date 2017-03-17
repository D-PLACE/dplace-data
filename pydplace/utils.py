# coding: utf8
from __future__ import unicode_literals, print_function, division

import codecs

def check_language_file(filename='languages.csv'):
    """
    Sanity checks a languages.csv file.
    
    Raises `ValueError` if an error/malformatted file is found.
    """
    with codecs.open(filename, 'r', encoding="utf8") as handle:
        content = handle.read()
    if not content.startswith('Taxon,ISOCode,GlottoCode\n'):
        raise ValueError("Header incorrect")
    if "\t" in content:
        raise ValueError("Should be a csv not tab-delimited")
    return True
