from sys import argv
import math
from random import random
from copy import copy

import networkx as nx
import matplotlib.pyplot as plt

from input_output import read_table
from louvian import community

def equal_weights (nodes):
    weights = []
    #denom = float (len (nodes[0]['pos']))
    for i in range (0, len (nodes[0]['pos'])):
        weights.append (1.0)
        #weights.append (1.0 / denom)
    return weights

def jitter_weights (weights):
    new_weights = copy (weights)
    i = int (math.floor (random () * len (weights)))
    j = int (math.floor (random () * len (weights)))
    #MAX = min (weights[i], weights[j])
    #epsilon = (random () * MAX) - MAX / 2.0
    epsilon = random ()
    if (new_weights[j] - epsilon) >= 0:
        new_weights[i] += epsilon
        new_weights[j] -= epsilon
    '''if new_weights[i] < 0 or new_weights[j] < 0:
        return weights
    else:
        return new_weights'''
    return new_weights


def classify_node (train, test, weights): 
    nodes = train + [test]
    
    classify_graph = make_graph (nodes, weights, 4)

    communities = community.best_partition (classify_graph)

    # Get the community that the test point belongs to and then find the diseases in the same community
    disease_group = communities[test['_id']]
    # filter out diseases not in the community
    related_diseases = filter (lambda node_id: (communities[node_id] == disease_group) and (node_id != test['_id']), communities)

    node_lookup = {}
    for node in nodes:
        node_lookup[node['_id']] = node

    diseases = map (lambda node_id: node_lookup[node_id]['attr']['Disease'], related_diseases)
    percents = {}
    for disease in diseases:
        if not percents.has_key (disease):
            percents[disease] = 1
        else:
            percents[disease] += 1
    for disease in percents:
        percents[disease] /= float (len (diseases))
    return percents
        

def make_graph (nodes, weights, limit):
    # limit is the number of edges to keep for each node
    G = nx.Graph ()
    for node in nodes:
        G.add_node (node['_id'], node)
    for i, first in enumerate (nodes):
        edges = []
        for j, second in enumerate (nodes):
            total = 0.0
            for w, f, s in zip (weights, first['pos'], second['pos']):
                if f and s:
                    # Calculate similiarity
                    # Optimal similiarity is 0, divide by 100 to normalize
                    total += (2.0 - 2.0 * w * (abs (f - s) / 100.0))
            edges.append ((second['_id'], total))
        edges.sort (key = lambda x: x[1])
        edges.reverse ()
        for k in range (0, limit):
            G.add_edge (first['_id'], edges[k][0], {'weight': edges[k][1]})
    return G


# csv file passed in as param
if __name__ == '__main__':
    if len (argv) != 2:
        print "Usage: python naive.py <INPUT>"
        exit (1)
    data = read_table (argv[1])

    for i in range (0, len (data)):
        nodes = []
        for j, node in enumerate (data):
            if i == j:
                test = node
            else:
                nodes.append (node)


        # Optimize modularity (mod) using weights and the graph
        mod = -.5
        weights = equal_weights (nodes)
        
        step = 1

        # For now, stop after 100 iterations
        while step < 100:
            new_weights = jitter_weights (weights)
            G = make_graph (nodes, new_weights, 4)

            part = community.best_partition (G)
            new_mod = community.modularity (part, G)
            if new_mod > mod:
                mod = new_mod
                weights = new_weights
            step += 1

        print test['attr']['Disease']
        percents = classify_node (nodes, test, weights)
        print percents
        print ''
