import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import time

# create road geometry in beamng.
filename = 'passau3'
map_ways_serialize = filename + '.ways.serialize'
map_nodes_serialize = filename + '.nodes.serialize'
map_beamng_serialize = filename + '.nodes.serialize.beamng'
map_degree_serialize = filename + '.ways.degree.serialize'
map_lanes_serialize = filename + '.lanes'
map_width_serialize = filename + '.width'


node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
print("BeamNG Nodes Loaded")

graph_degree = pickle.load(open(map_degree_serialize, "rb"))
print("Graph Degree")

lane_dict = pickle.load(open(map_lanes_serialize, "rb"))
print("Lanes Loaded")

width_dict = pickle.load(open(map_width_serialize, "rb"))
print("Width Loaded") # tuples of lat and long

beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
scenario = Scenario('GridMap', 'crash_simulation_2')

road_a = Road('track_editor_C_center', looped=False)

three_way = []
# 3 Way intersection
for tup in graph_degree:
    three_way_coordinate = []

    if tup[1] == 3:
        three_way_coordinate.append(node_dict[tup[0]])
        three_way_points = graph.neighbors(tup[0])
        way_geo = (tup[0], node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]])
        print(way_geo)
        print("collision point")
        print(beamng_dict[tup[0]])
        for node in three_way_points:
            way_geo = (node, node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]]) # node, coordinate, number of lanes , width
            print(way_geo)
            pair=(tup[0],node)  # nodes connected to center or intersection point
            print(pair)
            three_way.append(pair)
            three_way_coordinate.append(node_dict[node]) # list of lat and long for map plot





# # Create required road for BeamNG
# graph_edges = graph.edges
#
for sample in three_way:
    print("3 way")
    road_a = Road('track_editor_C_center', looped=False)

    point1 = list(beamng_dict[sample[0]])
    point2 = list(beamng_dict[sample[1]])

    nodes0 = [
        (point1[0], point1[1], -4, 4), # method to get the road width from elastic search or number of lanes. (forward and backward)
        (point2[0], point2[1], -4, 4)
    ]

    road_a.nodes.extend(nodes0)
    scenario.add_road(road_a)


scenario.make(beamng)
bng = beamng.open(launch=True)
try:
    bng.load_scenario(scenario)
    bng.start_scenario()

    input('Press enter when done...')

finally:
    bng.close()