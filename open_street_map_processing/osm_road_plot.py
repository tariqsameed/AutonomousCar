import mplleaflet
import matplotlib.pyplot as plt
import pickle
import networkx as nx

filename = 'passau'
path = "../resources/osm/"
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

lat_lon_list = []
for node in graph:
    element = node_dict[node]
    lat_lon_list.append(element)



lats = [x[0] for x in lat_lon_list]
lons = [x[1] for x in lat_lon_list]


fig = plt.figure()    #This is missing in your code.
plt.plot( lons, lats, 'rs')

mapfile = "osm_graph"  + '.html'
#And after this call the funtion:
mplleaflet.show(path=mapfile,fig=fig)