all: summary.trees posterior.trees

summary.trees: original/pAP_beast_dollo-relaxed-clock.mcct.trees
	cp $< $@

posterior.trees: original/pAP_beast_dollo-relaxed-clock.trees.gz
	# remove 1000 (10%), sample 1000
	nexus_treemanip.py -c -d 1-1000 $< tmp
	nexus_treemanip.py -n 1000 tmp $@
	rm tmp
