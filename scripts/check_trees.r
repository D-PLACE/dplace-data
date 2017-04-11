#!/usr/bin/env Rscript

# Checks the saved trees can be loaded in R. Looks for errors like singleton nodes

library(ape)

treefiles <- list.files('../phylogenies', 'summary.trees', recursive=TRUE, full.names=TRUE)

for (filename in treefiles) {
    tryCatch(tree <- read.nexus(filename), error=function(cond) {
        cat(sprintf("%40s: Read failed: \n\t%s\n", filename, cond), sep="\n")
    })
    
    if (Ntip(tree) <= 2) {
        # pass
    } else if (any(tabulate(tree$edge[, 1]) == 1)) {
        cat(sprintf("%40s: Singleton nodes", filename), sep="\n")
    }
}

