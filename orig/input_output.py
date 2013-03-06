import csv

import networkx as nx
from networkx.readwrite import json_graph

Y = 100
MINOR = 25

def read_table (path):
    nodes = []
    rows = csv.reader (open (path, 'r'))
    contrib = []
    # The first row contains a 1 or NULL that indicates if the field below contributes to the vector
    for elem in rows.next ():
        if len (elem) > 0:
            contrib.append (True)
        else:
            contrib.append (False)
    # The second row contains the headers
    keys = rows.next ()
    id = 0
    for row in iter (rows):
        pos = []
        attr = {}
        for key, value, include in zip (keys, row, contrib):
            # Cleanup the strings from the data
            if include:
                if value == 'y':
                    value = Y
                elif value == 'minor':
                    value = MINOR
                elif len (value) == 0:
                    value = 0
                pos.append (float (value))
            attr[key] = value
        item = {
            '_id': id,
            'pos': pos,
            'attr': attr
            }
        nodes.append (item)
        id += 1
    return nodes


def equal_weights (nodes):
    weights = []
    for i in range (0, len (nodes[0]['pos'])):
        weights.append (1.0)
    return weights


def make_graph (nodes, weights):
    G = nx.Graph ()
    for node in nodes:
        G.add_node (node['_id'], node)
    for i, first in enumerate (nodes):
        for j, second in enumerate (nodes):
            if j >= i:
                continue
            total = 0.0
            for w, f, s in zip (weights, first['pos'], second['pos']):
                total += w * ((f - s) / 100.0)
            if total > 0.0:
                G.add_edge (first['_id'], second['_id'], {'weight': total})
    return G
