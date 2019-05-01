

all: summary.trees posterior.trees

summary.trees: original/phylogeny_japonic.tre
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/Japonic_COV_UCLD.trees.gz
	gunzip -c $< > tmp
	nexus_treemanip.py -n 1000 -c tmp $@
	rm tmp