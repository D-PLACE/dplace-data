
all: summary.trees posterior.trees

summary.trees: original/MICHAEL.tupiguarani_phylogeny.tre
	nexus_treemanip.py -t -c $< tmp
	python process.py tmp $@
	rm tmp

posterior.trees: original/TGB9jNoApiakaTuriwaraMrBayes.nex.run1.t original/TGB9jNoApiakaTuriwaraMrBayes.nex.run2.t
	nexus_treemanip.py --detranslate --deltree 1-5001 $(word 1, $^) --random 500 1.tmp
	nexus_treemanip.py --detranslate --deltree 1-5001 $(word 2, $^) --random 500 2.tmp
	nexus_combine_nexus.py 1.tmp 2.tmp  # creates 'combined.nex'
	python process.py combined.nex $@
	rm -rf *.tmp combined.nex