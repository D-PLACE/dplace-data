
NM='nexus_treemanip.py'

all: summary.trees

temp.trees: original/MICHAEL.tupiguarani_phylogeny.tre
	$(NM) -t -c $< $@

summary.trees: temp.trees
	python process.py $< $@
	rm $<