

all: summary.trees posterior.trees

summary.trees: original/kitchen2009.mcct.trees
	nexus_treemanip.py -c -t $< $@

posterior.trees: original/Semitic.Greenhill.trees.gz
	nexus_treemanip.py -c -d 1-200 $< tmp
	nexus_treemanip.py -n 1000 tmp $@
	rm tmp
