

all: summary.trees posterior.trees

summary.trees: original/aruakout
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/Aruakrrw.trees.txt.zip
	unzip -c $< > tmp
	nexus_treemanip.py -n 1000 -c tmp $@
	rm tmp