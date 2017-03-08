#!/usr/bin/env Rscript

# Checks the saved trees can be loaded in R. Looks for errors like singleton nodes

library(ape)

FILES <- c(
    list.files('../trees', '*.trees', full.names=TRUE),
    list.files('../phylogenies/', '*.trees', recursive=TRUE, full.names=TRUE)
)
    

for (f in FILES) {
    tryCatch(read.nexus(f), error=function(cond) {
        cat(sprintf("Reading %s failed: \n%s\n", f, cond), sep="\n")
    })
}

