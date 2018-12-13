
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/phylogeny_japonic.tre
	$(NM) -t -c $< $@

posterior.trees: original/Japonic_COV_UCLD.trees.gz
	gunzip -c $< > tmp
	$(NM) -n 1000 -c tmp $@
	rm tmp