import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import time
from beamngpy.sensors import Electrics, Damage
import math
import random
import numpy as np
#from expriments_simulation.crash_simulation_4.crash_simulation_helper import getV1BeamNGCoordinaes, getV2BeamNGCoordinaes
from expriments_simulation.crash_simulation_4.crash_simulation_helper import AngleBtw2Points, getDistance
#from expriments_simulation.crash_simulation_4.vehicle_state_helper import DamageExtraction, DistanceExtraction, RotationExtraction
import csv
import sys
#sys.stdout = open('output.txt','w')

# create road geometry in beamng.
filename = 'munich4'
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


# ---------------------------- save genetic algorithm iteration-----------------------------------------
f= open("genetic_algorithm_iteration.csv","w+")
# ----------------------------- create csv file --------------------------
pos_crash_dict = {}

csv_columns = ['chromosome','v1_speed', 'v1_waypoint', 'v2_speed','v2_waypoint', 'striker_damage', 'victim_damage',
               'striker_distance', 'victim_distance', 'striker_rotation', 'victim_rotation', 'fitness_value']
csv_file = "pos_crash_analysis.csv"
try:
    with open(csv_file, 'w', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
        writer.writeheader()
except IOError:
    print("I/O error")
# -------------------------------------------------------------------------

def saveDictionaryToCsvFile():
    csv_columns = ['chromosome', 'v1_speed', 'v1_waypoint', 'v2_speed', 'v2_waypoint', 'striker_damage',
                   'victim_damage', 'striker_distance', 'victim_distance', 'striker_rotation', 'victim_rotation',
                   'fitness_value']
    csv_file = "pos_crash_analysis.csv"
    try:
        with open(csv_file, 'a', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
            writer.writerow(pos_crash_dict)
    except IOError:
        print("I/O error")

# -------------------------------------------------------------------------

beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
scenario = Scenario('GridMap', 'crash_simulation_1')

road_a = Road('track_editor_C_center', looped=False)

collision_point =[]
four_way = []

# 4 Way intersection
for tup in graph_degree:
    four_way_coordinate = []

    if tup[1] == 4:
        print(tup[0],tup[1])
        four_way_coordinate.append(node_dict[tup[0]])
        four_way_points = graph.neighbors(tup[0])
        print(four_way_points)
        print("collision point")
        print(beamng_dict[tup[0]])
        collision_point.append(beamng_dict[tup[0]])
        for node in four_way_points:
            way_geo = (node, node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]])  # node, coordinate, number of lanes , width
            print(way_geo)
            pair = (tup[0], node)
            four_way.append(pair)
            four_way_coordinate.append(node_dict[node])


print(four_way)
for sample in four_way:
    print("4 way")
    road_a = Road('track_editor_C_center', looped=False)

    point1 = list(beamng_dict[sample[0]])
    point2 = list(beamng_dict[sample[1]])

    print(point1, point2)
    print(getDistance(point1,point2))

    nodes0 = [
        (point1[0], point1[1], 0, 16), # method to get the road width from elastic search or number of lanes. (forward and backward)
        (point2[0], point2[1], 0, 16)
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