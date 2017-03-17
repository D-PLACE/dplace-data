Phylogenies
===========

Each directory within the phylogenies subdirectory contains the following:

1. original/ -- a directory storing the original tree files.

2. taxa.csv -- a csv file linking the taxon labels in original/ to their correct glottocodes and xd_ids and society ids:

    taxon	glottocode	xd_ids	soc_ids

3. summary.trees -- a single summary tree in nexus tree format.
4. posterior.trees -- a posterior probability distribution of the trees (if available) in nexus tree format.
5. Makefile -- a `Makefile` to generate summary.trees and posterior.trees from the original data.

Prerequisites:
--------------

If you want to run the Makefiles yourself then you will need to install the [python-nexus](https://pypi.python.org/pypi/python-nexus/) library
for the nexus_treemanip.py program.

Notes on adding a new tree:
---------------------------

* the directory name should reflect the source of the tree (e.g.
  gray_et_al2009) rather than the language family (e.g. austronesian.trees) as
  we might have multiple trees for the same language family, or trees that span
  families.
* the directory should be lower case.


