

all: summary.trees posterior.trees

summary.trees: original/a400-m1pcv-time.mcct.trees.gz
	gunzip -c $< > tmp
	nexus_treemanip.py -c -t tmp $@
	rm tmp

posterior.trees: original/a400-m1pcv-time.trees.gz
	# remove 1000 (10%), sample 1000
	nexus_treemanip.py -c -d 1-1000 $< tmp
	nexus_treemanip.py -n 1000 tmp $@
	rm tmp
