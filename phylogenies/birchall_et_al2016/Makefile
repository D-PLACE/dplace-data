all: summary.trees posterior.trees

summary.trees: original/relaxed-binary-simple.time.mcct.trees
	cp $< $@

posterior.trees: original/relaxed-binary-simple.time.trees.gz
	# remove 10000 (50%), sample 1000 from remainder
	gunzip -c $< > tmp
	nexus_treemanip.py -c -d 1-10000 tmp tmp2
	nexus_treemanip.py -n 1000 tmp2 $@
	rm tmp tmp2
