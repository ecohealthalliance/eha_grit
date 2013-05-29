import csv

Y = 100
MINOR = 25

def read(path):
    nodes = []
    #buffer = open (path, 'r').read ()
    #buffer = buffer.replace ('\r', '')
    #rows = buffer.split ('\n')
    rows = csv.reader (open (path, 'rU'))
    contrib = []
    for elem in rows.next ():
        if len (elem) > 0:
            contrib.append (True)
        else:
            contrib.append (False)
    keys = rows.next ()
    id = 0
    for row in iter (rows):
        #if len (row) == 0:
        #    continue
        pos = []
        attr = {}
        for key, value, include in zip (keys, row, contrib):
            #print ' '.join ([key, value, str (include)])
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

