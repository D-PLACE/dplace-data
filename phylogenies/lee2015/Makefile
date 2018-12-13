
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/phylogeny_koreanic.tre
	$(NM) -t -c $< $@

posterior.trees: original/Koreanic_COV_UCLD.trees.gz
	# remove first 900 trees as burn-in
	$(NM) -c -d 1-901 $< $@
