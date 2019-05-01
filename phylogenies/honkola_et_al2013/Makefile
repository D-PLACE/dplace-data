

all: summary.trees posterior.trees

summary.trees: original/Ura100_beast.tre
	nexus_treemanip.py -c -t $< $@

posterior.trees: original/Ura100_beast_full.trees.gz
	nexus_treemanip.py -c -d 1-200 $< tmp
	nexus_treemanip.py -n 1000 tmp $@
	rm tmp
