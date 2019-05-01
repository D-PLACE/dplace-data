

all: summary.trees posterior.trees

summary.trees: original/phylogeny_deneyeniseian_24April2016.tre
	nexus_treemanip.py -t -c $< $@

posterior.trees: original/DY-26Dec-strict-Hout-ConsensusNetwork-edited.t.nex.gz
	gunzip -c $< > tmp
	nexus_treemanip.py -n 1000 -c tmp $@
	rm tmp