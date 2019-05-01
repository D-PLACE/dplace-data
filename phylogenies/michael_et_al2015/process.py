#!/usr/bin/env python
#coding=utf-8

import ete3
from nexus import NexusReader

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        description='reroots and cleans Michael et al.'
    )
    parser.add_argument("input", help='filename')
    parser.add_argument("output", help='filename')
    args = parser.parse_args()
    
    nex = NexusReader(args.input)

    for i, tree in enumerate(nex.trees.trees):
        # make tree into newick for ete3
        tree = nex.trees.trees[i].split(" = ")[1].strip().lstrip()
        tree = tree.replace("[&U]", "")  # remove unrooted flag if present
        tree = ete3.Tree(tree, format=0)
        
        # reroot
        tree.set_outgroup('Mawe')
        nex.trees.trees[i] = 'tree tg_%d [&R] = %s' % (i, tree.write(format=5))
    
    with open(args.output, 'w') as out:
        out.write(nex.write())