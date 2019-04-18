NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/41559_2018_489_MOESM4_ESM.txt
	$(NM) -t -c $< $@

posterior.trees: original/pny10.fixed.cov.ucln.bdsky.ba-sp.trees.gz
	$(NM) -c -n 1000 $< $@