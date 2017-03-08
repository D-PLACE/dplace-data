
all: summary.trees

summary.trees: original/phylogeny_tukanoan.tre
	echo "#NEXUS\nbegin trees;\n\t" > $@
	cat $< >> $@
	echo "\nend;\n" >> $@
