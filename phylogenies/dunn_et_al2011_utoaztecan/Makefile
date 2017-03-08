
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/utoaztecan.mcct.trees
	$(NM) -t -c $< > $@

posterior.trees: original/utoaztecan-postburnin.trees.gz
	$(NM) -t -c $< $@
