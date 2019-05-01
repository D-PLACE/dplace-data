

all: summary.trees posterior.trees

summary.trees: original/grollemund.mcct.trees
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/BP425_M1P_100_cv2_relaxed_YP_runs_1_2_4_5_thinned-fixed.trees.gz
	gunzip -c $< > $@
