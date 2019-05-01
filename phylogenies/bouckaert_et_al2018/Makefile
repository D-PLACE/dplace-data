
all: summary.trees posterior.trees

summary.trees: original/41559_2018_489_MOESM4_ESM.txt
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/pny10.fixed.cov.ucln.bdsky.ba-sp.trees.gz
	nexus_treemanip.py -c -n 1000 $< $@