
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/Ainu_SDollo_GRW.mcct.trees
	cp $< $@

posterior.trees: original/Ainu_SDollo_GRW.trees.gz
	$(NM) -c -n 1000 $< $@
