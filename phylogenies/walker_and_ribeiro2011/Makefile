
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/aruakout
	$(NM) -t -c $< $@

posterior.trees: original/Aruakrrw.trees.txt.zip
	unzip -c $< > tmp
	$(NM) -n 1000 -c tmp $@
	rm tmp