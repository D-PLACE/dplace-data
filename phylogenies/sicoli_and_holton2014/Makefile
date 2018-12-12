
NM='nexus_treemanip.py'

all: summary.trees posterior.trees

summary.trees: original/phylogeny_deneyeniseian_24April2016.tre
	$(NM) -t -c $< $@

posterior.trees: original/DY-26Dec-strict-Hout-ConsensusNetwork-edited.t.nex.gz
	gunzip -c $< > tmp
	$(NM) -n 1000 -c tmp $@
	rm tmp