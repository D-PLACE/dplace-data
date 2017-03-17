
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/Ura100_beast.tre
	$(NM) -c -t $< $@

posterior.trees: original/Ura100_beast_full.trees.gz
	$(NM) -c -d 1-200 $< tmp
	$(NM) -n 1000 tmp $@
	rm tmp
