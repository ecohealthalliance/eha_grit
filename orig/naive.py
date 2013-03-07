from sys import argv
import math
from random import random
from copy import copy

import networkx as nx
import matplotlib.pyplot as plt

from input_output import read_table
from louvian import community

import numpy as np
from scipy.optimize import anneal

def equal_weights (nodes, value):
    weights = []
    #denom = float (len (nodes[0]['pos']))
    for i in range (0, len (nodes[0]['pos'])):
        weights.append (value)
        #weights.append (1.0 / denom)
    return weights


def jitter_weights (weights):
    # The original way of moving around the space
    new_weights = copy (weights)
    i = int (math.floor (random () * len (weights)))
    j = int (math.floor (random () * len (weights)))
    epsilon = random ()
    if (new_weights[j] - epsilon) >= 0:
        new_weights[i] += epsilon
        new_weights[j] -= epsilon
    return new_weights
    '''# A less contstrained way of moving around the space
    new_weights = copy (weights)
    i = int (math.floor (random () * len (weights)))
    epsilon = 2.0 * random () - 1.0
    if (new_weights[i] + epsilon) >= 0:
        new_weights[i] += epsilon
    return new_weights'''


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
            if i == j:
                continue
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
            if not G.has_edge (edges[k][0], first['_id']):
                G.add_edge (first['_id'], edges[k][0], {'weight': edges[k][1]})
        #for edge in edges:
        #    G.add_edge (first['_id'], edge[0], {'weight': edge[1]})
    return G


# Step is just a counter so we can see where we are in the optimization
step = 0

def f (weights, nodes, limit):
    # scipy does not check limits
    if np.amax (weights) > 1.0 or np.amin (weights) < 0.0:
        return float ('inf')

    G = make_graph (nodes, weights, limit)
    # Find the best partition possible and get the modularity of it
    part = community.best_partition (G)
    modularity = community.modularity (part, G)

    # Print out the status of the algorithm
    global step
    print "Step %d: %f" % (step, modularity)
    step += 1

    # Technically, simulated annaling looks for a minimum, so to invert modularity
    return -modularity


# argv[1] is a csv file to read data from
if __name__ == '__main__':
    if len (argv) != 2:
        print "Usage: python naive.py <INPUT>"
        exit (1)
    data = read_table (argv[1])

    # Run N times, exclude one data point each time
    for i in range (0, len (data)):
        train = []
        # Build the training set and test point
        for j, node in enumerate (data):
            if i == j:
                test = node
            else:
                train.append (node)

        initial_weights = equal_weights (train, .5)
        min_weights = equal_weights (train, 0.0)
        max_weights = equal_weights (train, 1.0)
        
        weights = anneal (f, initial_weights, args = [train, 4], lower = min_weights, upper = max_weights, maxiter = 1)[0]

        print test['attr']['Disease']
        percents = classify_node (train, test, weights)
        print percents
        print ''

        exit (0)
