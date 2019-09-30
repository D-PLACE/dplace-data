all: summary.trees posterior.trees

summary.trees: original/bantu_lexico_bin_M1P_cov2_burn40_all.mcct.trees
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/bantu_lexico_bin_M1P_cov2_burn40_all.trees.gz
	nexus_treemanip.py -t -c -n 1000 $< $@

