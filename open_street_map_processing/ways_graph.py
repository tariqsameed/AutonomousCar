import networkx as nx
import sys
import xml.etree.ElementTree as ET
import pickle
from geopy.distance import great_circle

filename = 'passau'
path = "../resources/osm/"

map_ways = path + filename + '.ways'
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'

try:
    node_dict = pickle.load(open(map_nodes_serialize, "rb"))
    print("Nodes Loaded")

    mapWaysFile = open(map_ways, 'r', encoding="utf8")
    graph = nx.Graph()
    wayBegin = False
    nodeCounter = 0
    prevNode = 0
    nextNode = 0
    lineCounter = 0
    for line in mapWaysFile:
        lineCounter = lineCounter + 1
        if (lineCounter % 10000) == 1:
            print(lineCounter)
        if line.startswith('  <way') and wayBegin == False:
            wayBegin = True
            continue
        elif line.startswith('  </way') and wayBegin == True:
            wayBegin = False
            nodeCounter = 0
        elif line.startswith('    <nd ref'):
            nodeCounter = nodeCounter + 1
            node = ET.fromstring(line)
            if nodeCounter == 1:
                prevNode = node.attrib['ref']
            elif nodeCounter > 1:
                nextNode = node.attrib['ref']
                # do not add edge weight (all edges have weight 1)
                # add edge weight: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
                distance = great_circle(node_dict[nextNode], node_dict[prevNode]).m
                print(distance)
                graph.add_edge(prevNode, nextNode, weight=distance)
                prevNode = nextNode
        else:
            print ("Faulty File")
    mapWaysFile.close()
    # According to https://docs.python.org/3/library/pickle.html
    # protocol version 4 added in Python 3.4 adds support for very large objects. (not backward compatible)
    pickle.dump(graph, open(map_ways_serialize, "wb"), protocol=4)
    print("Done")
except IOError:
    print ("Could not read file or file does not exist: ", map)
    sys.exit()