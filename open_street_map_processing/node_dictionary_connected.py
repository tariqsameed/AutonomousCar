import networkx as nx
import pickle

filename = 'passau'
known_connected_node_passau = '27479770' #'50376711'
path = "../resources/osm/"

filename = 'munich4'
path = r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_6\\'


map_nodes_serialize = path + filename + '.nodes.serialize'
map_nodes_connected_serialize = path + filename + '.nodes.connected.serialize'
map_ways_serialize = path + filename + '.ways.serialize'
map_degree_serialize = path + filename + '.ways.degree.serialize'
connected_nodes_dict = {}

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

degrees = [val for (node, val) in graph.degree()]
print(graph.degree())

pickle.dump(graph.degree(), open(map_degree_serialize, "wb"))

# Remove buildings and gardens that are not connected to roads.
connected_nodes = nx.node_connected_component(graph, known_connected_node_passau)

for node in connected_nodes:
    connected_nodes_dict[node] = node_dict[node]

pickle.dump(connected_nodes_dict, open(map_nodes_connected_serialize, "wb"))

print("Done")