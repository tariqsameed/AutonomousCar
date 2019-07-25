import math
from geopy.distance import great_circle
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import sys
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging

filename = 'passau'
path = "../resources/osm/"
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'
map_beamng_serialize = path + filename + '.nodes.serialize.beamng'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
print("BeamNG Nodes Loaded")


def createBeamNGRoads():

    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
    scenario = Scenario('GridMap', 'road_test')

    print(graph.edges)

    graph_edges = graph.edges

    print(len(graph_edges))
    for sample in graph_edges:
        road_a = Road('custom_track_center', looped=False)
        point1 = list(beamng_dict[sample[0]])
        point2 = list(beamng_dict[sample[1]])

        nodes0 = [
            (point1[0], point1[1], -4, 4),
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



createBeamNGRoads()