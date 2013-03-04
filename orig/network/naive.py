from sys import argv
import math
from random import random
from copy import copy

import networkx as nx

from io import read_table
from louvian import community

def equal_weights (nodes):
    weights = []
    denom = float (len (nodes[0]['pos']))
    for i in range (0, len (nodes[0]['pos'])):
        weights.append (1.0 / denom)
    return weights

def jitter_weights (weights):
    new_weights = copy (weights)
    i = int (math.floor (random () * len (weights)))
    j = int (math.floor (random () * len (weights)))
    MAX = min (weights[i], weights[j])
    epsilon = (random () * MAX) - MAX / 2.0
    new_weights[i] += epsilon
    new_weights[j] -= epsilon
    '''if new_weights[i] < 0 or new_weights[j] < 0:
        return weights
    else:
        return new_weights'''
    return new_weights

def make_graph_limit (nodes, weights, limit):
    G = nx.Graph ()
    for node in nodes:
        G.add_node (node['_id'], node)
    for i, first in enumerate (nodes):
        edges = []
        for j, second in enumerate (nodes):
            total = 0.0
            for w, f, s in zip (weights, first['pos'], second['pos']):
                if f and s:
                    total += w * ((f - s) / 100.0)
            edges.append ((second['_id'], total))
        edges.sort (key = lambda x: x[1])
        edges.reverse ()
        for k in range (0, limit):
            G.add_edge (first['_id'], edges[k][0], {'weight': edges[k][1]})
    return G


if __name__ == '__main__':
    nodes = read_table (argv[1])
    weights = equal_weights (nodes)
    mod = -.5
    part = {}
    for node in nodes:
        part[node['_id']] = node['attr']['Disease']
    while True:
        new_weights = jitter_weights (weights)
        G = make_graph_limit (nodes, new_weights, 4)
        new_mod = community.modularity (part, G)
        if new_mod > mod:
            mod = new_mod
        print mod
        
