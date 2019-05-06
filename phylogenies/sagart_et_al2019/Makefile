

all: summary.trees posterior.trees

summary.trees: original/sinotibetan-beast-covarion-relaxed-fbd.mcct.trees
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/sinotibetan-march-beast-covarion-relaxed-fbd.trees.gz
	# remove 1000 (10%), sample 1000
	nexus_treemanip.py -c -d 1-1000 -n 1000 $< $@
