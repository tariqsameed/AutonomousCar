import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import time
from beamngpy.sensors import Electrics, Damage
import math
import random
import numpy as np
from expriments_simulation.crash_simulation_2.crash_simulation_helper import getV1BeamNGCoordinaes, getV2BeamNGCoordinaes
from expriments_simulation.crash_simulation_2.crash_simulation_helper import AngleBtw2Points, getDistance
from expriments_simulation.crash_simulation_2.vehicle_state_helper import DamageExtraction, DistanceExtraction, RotationExtraction
import csv
import sys
sys.stdout = open('output.txt','w')

# create road geometry in beamng.
filename = 'regensberg3'
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
scenario = Scenario('GridMap', 'crash_simulation_3')

road_a = Road('track_editor_C_center', looped=False)

collision_point =[]
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
        collision_point.append(beamng_dict[tup[0]])
        for node in three_way_points:
            way_geo = (node, node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]]) # node, coordinate, number of lanes , width
            print(way_geo)
            pair=(tup[0],node)  # nodes connected to center or intersection point
            print(pair)
            print(beamng_dict[tup[0]],beamng_dict[node])
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

    print(getDistance(point1,point2))

    nodes0 = [
        (point1[0], point1[1], 0, 8), # method to get the road width from elastic search or number of lanes. (forward and backward)
        (point2[0], point2[1], 0, 8)
    ]

    road_a.nodes.extend(nodes0)
    scenario.add_road(road_a)


vehicleStriker = Vehicle('striker', model='etk800', licence='PYTHON', colour='White')
damageStriker = Damage();
vehicleStriker.attach_sensor('damagesS', damageStriker);

vehicleVictim = Vehicle('victim', model='etk800', licence='PYTHON', colour='White')
damageVictim = Damage();
vehicleVictim.attach_sensor('damagesV', damageVictim);

# road creation  and vehicle initializatoin with sensors completed.-------------------------------------------

def getDistance(node_a,node_b):
    dist = math.sqrt((node_a[1] - node_b[1]) ** 2 + (node_a[0] - node_b[0]) ** 2)
    return dist


# genetic algorithm chromosome indexes.
V1_SPEED_INDEX_1 = 0
V1_SPEED_INDEX_2 = 1
V1_DISTANCE_INDEX_1 = 2
V1_DISTANCE_INDEX_2 = 3
V1_WIDTH_INDEX = 4
V2_SPEED_INDEX_1 = 5
V2_SPEED_INDEX_2 = 6
V2_DISTANCE_INDEX_1 = 7
V2_DISTANCE_INDEX_2 = 8
V2_WIDTH_INDEX = 9
POINT_OF_IMPACT_RADIUS = 10
POINT_OF_IMPACT_ANGLE_1 = 11
POINT_OF_IMPACT_ANGLE_2 = 12
POINT_OF_IMPACT_ANGLE_3 = 13
IMPACT_POSITION_X = 334
IMPACT_POSITION_Y = 165

# roads for striker and victim vehicle.
road_striker = [(292, 137),(334, 165)]
road_victim =  [(281, 179),(334, 165)]


actual_striker_damage = "L"
actual_victim_damage = "F"

# parameters for vehicle state extraction
positions = list()
directions = list()
damages = list()

populations_fitness = {} # fitness function to store fitness values of chromosomes.



# scenario.make(beamng)
# bng = beamng.open(launch=True)
# try:
#     bng.load_scenario(scenario)
#     bng.start_scenario()
#
#     input('Press enter when done...')
# finally:
#     bng.close()
