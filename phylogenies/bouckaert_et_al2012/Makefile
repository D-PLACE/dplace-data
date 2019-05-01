

all: summary.trees posterior.trees

summary.trees: original/1219669IndoEuropean_2MCCtrees_annotated.tre
	nexus_treemanip.py -t -c -d 2 $< $@

posterior.trees: original/IE2011_RelaxedCovarion_AllSingletonsGeo_Combined.trees.gz
	# remove 1000 (10%), sample 1000
	nexus_treemanip.py -c -d 1-1000 $< tmp
	nexus_treemanip.py -n 1000 tmp $@
	rm tmp
