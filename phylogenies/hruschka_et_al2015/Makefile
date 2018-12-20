
NM='nexus_treemanip.py'
TREES=original/bp-noF-AS-noReg-Relaxed-cS_v2_t1.trees

all: summary.trees posterior.trees

posterior.trees: original/bp-noF-AS-reg-Relaxed-cS_t8.trees
	perl -pe 's/\|[0-9]*\.?[0-9]+//g' $(TREES) > $@

summary.trees: posterior.trees
	# use BEAST's `treeannotator` program to create the MCC tree.
	treeannotator -burnin 10 -heights median $< $@
