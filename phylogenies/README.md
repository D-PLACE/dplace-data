Phylogenies
===========

Each directory within the phylogenies subdirectory *MUST* contain the following:

1. taxa.csv -- a csv file linking the taxon labels in `summary.trees` to their correct glottocodes and xd_ids and society ids:

    taxon	glottocode	xd_ids	soc_ids

2. summary.trees -- a single summary tree in nexus tree format.

And may contain other files including:

3. original/ -- a directory storing the original tree files. Note: For programmatically
   created phylogenies like the ones from Glottolog, this directory is not present.

4. posterior.trees -- a posterior probability distribution of the trees (if available) in nexus tree format.

5. Makefile -- a `Makefile` to generate summary.trees and posterior.trees from the original data.

Prerequisites:
--------------

If you want to run the Makefiles yourself then you will need to install the [python-nexus](https://pypi.python.org/pypi/python-nexus/) library for the nexus_treemanip.py program.

Notes on adding a new tree:
---------------------------

* the directory name should reflect the source of the tree (e.g. gray_et_al2009) rather than the language family (e.g. austronesian.trees) as we might have multiple trees for the same language family, or trees that span families.
* the directory should be lower case.
* each directory *must* be added to index.csv
