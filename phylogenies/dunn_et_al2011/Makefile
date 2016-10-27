
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/utoaztecan.mcct.trees
	$(NM) -c $< > $@

posterior.trees: original/utoaztecan-postburnin.trees.gz
	$(NM) -c $< $@
