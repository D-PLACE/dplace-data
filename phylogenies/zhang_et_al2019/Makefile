
all: summary.trees posterior.trees

summary.trees: original/109SinoTibetanLanguages.MCC.tree
	cp $< $@

posterior.trees: original/Sino-Tibetan\ Posterior\ tree\ distribution.trees.gz
	# remove 1000 (10%), sample 1000
	nexus_treemanip.py -c -d 1-1000 -n 1000 "$<" $@

