
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/kitchen2009.mcct.trees
	$(NM) -c $< $@

posterior.trees: original/Semitic.Greenhill.trees.gz
	$(NM) -c -d 1-200 $< tmp
	$(NM) -n 1000 tmp $@
	rm tmp
