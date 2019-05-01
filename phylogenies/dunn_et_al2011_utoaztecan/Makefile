

all: summary.trees posterior.trees

summary.trees: original/utoaztecan.mcct.trees
	nexus_treemanip.py -t -c $< > $@

posterior.trees: original/utoaztecan-postburnin.trees.gz
	nexus_treemanip.py -t -c $< $@
