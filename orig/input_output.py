import csv

import networkx as nx
from networkx.readwrite import json_graph

import pdb

class IO:

    Y = 100
    MINOR = 25

    def read_table (self,path):
        self.vectorLength = 0
        nodes = []
        rows = csv.reader (open (path, 'r'))
        contrib = []
        # The first row contains a 1 or NULL that indicates if the field below contributes to the vector
        for elem in rows.next ():
            if len (elem) > 0:
                contrib.append (True)
                self.vectorLength += 1
            else:
                contrib.append (False)

        # The second row contains the headers
        keys = rows.next ()
        id = 0
        for row in iter (rows):
            # pos is the position vector in zack speak
            # its a hash because its sparse, not recording empty values
            pos = {}
            attr = {}
            i = 0
            for key, value, include in zip (keys, row, contrib):
                # Cleanup the strings from the data
                if include and len(value) > 0:
                    if value == 'y':
                        value = IO.Y
                    elif value == 'minor':
                        value = IO.MINOR
                    pos[i] = (float(value))
                    if include:
                        i += 1
                attr[key] = value
            item = {
                '_id': id,
                'pos': pos,
                'attr': attr
                }
            nodes.append (item)
            id += 1
        return nodes
