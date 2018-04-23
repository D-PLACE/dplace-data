
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/rsos171504supp5.trees
	$(NM) -t -c $< > $@

posterior.trees: original/drav_cov_est_ucln_yule_no_burnin.trees.gz
	# remove 1000 (10%), sample 1000
	$(NM) -c -d 1-1000 $< tmp
	$(NM) -n 1000 tmp $@
	rm tmp
