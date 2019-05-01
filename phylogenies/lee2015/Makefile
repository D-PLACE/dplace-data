

all: summary.trees posterior.trees

summary.trees: original/phylogeny_koreanic.tre
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/Koreanic_COV_UCLD.trees.gz
	# remove first 900 trees as burn-in
	nexus_treemanip.py -c -d 1-901 $< $@
