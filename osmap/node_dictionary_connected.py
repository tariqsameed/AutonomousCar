import networkx as nx
import pickle

filename = 'passau'
known_connected_node_passau = '60631519'
path = "../resources/osm/"

map_nodes_serialize = path + filename + '.nodes.serialize'
map_nodes_connected_serialize = path + filename + '.nodes.connected.serialize'
map_ways_serialize = path + filename + '.ways.serialize'
connected_nodes_dict = {}

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

#degrees = [val for (node, val) in graph.degree()]
#print(graph.degree())

connected_nodes = nx.node_connected_component(graph, known_connected_node_passau)

for node in connected_nodes:
    connected_nodes_dict[node] = node_dict[node]

pickle.dump(connected_nodes_dict, open(map_nodes_connected_serialize, "wb"))

print("Done")