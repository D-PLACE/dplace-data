
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/grollemund.mcct.trees
	$(NM) -t -c $< $@

posterior.trees: original/BP425_M1P_100_cv2_relaxed_YP_runs_1_2_4_5_thinned.trees.gz
	gunzip -c $< > $@
