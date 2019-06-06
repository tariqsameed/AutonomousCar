import pickle
import networkx as nx

filename = 'passau'
path = "../resources/osm/"

map_degree_serialize = path + filename + '.ways.degree.serialize'
map_ways_serialize = path + filename + '.ways.serialize'

graph_degree = pickle.load(open(map_degree_serialize, "rb"))
print("Graph Degree")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

# Files declare to store routing path
route_path = "../resources/routes/"


# 3 Way intersection
for tup in graph_degree:
    way_exist = False
    route_list = []
    center = ''
    if tup[1] == 3:
        way_exist = True
        print(list(nx.dfs_edges(graph, source=tup[0], depth_limit=4)))
        way_3 = list(nx.dfs_edges(graph, source=tup[0], depth_limit=4))
        center = way_3[0][0]
        previous_index = 0
        single_route = []
        for idx, val in enumerate(way_3):
            if(val[0] == center and idx != 0):
                route_list.append(single_route)
                single_route = []
                single_route.append(val)
            else:
                single_route.append(val)

        if len(single_route) > 0:
            route_list.append(single_route)
            single_route = []

    if way_exist:
        print(center)
        print(route_list)
        print(center)
        print(route_list)
        route_path_serialize = route_path + center + '.route.serialize'
        pickle.dump(route_list, open(route_path_serialize, "wb"))
        route_list = []
        center = ''
        way_exist = False


# 4 Way intersection
for tup in graph_degree:
    way_exist = False
    route_list = []
    center = ''
    if tup[1] == 4:
        print(list(nx.dfs_edges(graph, source=tup[0], depth_limit=4)))
        way_exist = True
        print(list(nx.dfs_edges(graph, source=tup[0], depth_limit=4)))
        way_4 = list(nx.dfs_edges(graph, source=tup[0], depth_limit=4))
        center = way_4[0][0]
        previous_index = 0
        single_route = []
        for idx, val in enumerate(way_4):
            if (val[0] == center and idx != 0):
                route_list.append(single_route)
                single_route = []
                single_route.append(val)
            else:
                single_route.append(val)

        if len(single_route) > 0:
            route_list.append(single_route)
            single_route = []

    if way_exist:
        print(center)
        print(route_list)
        route_path_serialize = route_path + center + '.route.serialize'
        pickle.dump(route_list, open(route_path_serialize, "wb"))
        route_list = []
        center = ''
        way_exist = False


# Get distance between two nodes
print(graph.get_edge_data('595019','3278295187'))