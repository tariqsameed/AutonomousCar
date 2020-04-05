from __future__ import division
import math
import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import networkx as nx
import itertools
import numpy as np
import matplotlib.pyplot as plt

fig=plt.figure()
ax=fig.add_subplot(1,1,1)

filename = 'regensberg3'
path = "../experiments_simulation_modified/crash_simulation_3/"
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'
map_beamng_serialize = path + filename + '.nodes.serialize.beamng'
map_degree_serialize = path + filename + '.ways.degree.serialize'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
print("BeamNG Nodes Loaded")

graph_degree = pickle.load(open(map_degree_serialize, "rb"))
print("Graph Degree")


# genetic algorithm chromosome indexes.
V1_SPEED_INDEX = 0
V1_DISTANCE_INDEX_1 = 1
V1_DISTANCE_INDEX_2 = 2
V1_WIDTH_INDEX = 3
V2_SPEED_INDEX = 4
V2_DISTANCE_INDEX_1 = 5
V2_DISTANCE_INDEX_2 = 6
V2_WIDTH_INDEX = 7
POINT_OF_IMPACT_RADIUS = 8
POINT_OF_IMPACT_ANGLE = 9
IMPACT_POSITION_X = 334
IMPACT_POSITION_Y = 165

# roads for striker and victim vehicle.
road_striker = [(292, 137),(334, 165)]
road_victim =  [(281, 179),(334, 165)]

road_a = [(292, 137),(334, 165)]
road_b =  [(281, 179),(334, 165)]

collision_point =[]
three_way = []
# 3 Way intersection
for tup in graph_degree:
    three_way_coordinate = []

    if tup[1] == 3:
        three_way_coordinate.append(node_dict[tup[0]])
        three_way_points = graph.neighbors(tup[0])
        #way_geo = (tup[0], node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]])
        #print(way_geo)
        print("collision point")
        print(beamng_dict[tup[0]])
        collision_point.append(beamng_dict[tup[0]])
        for node in three_way_points:
            #way_geo = (node, node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]], beamng_dict[node]) # node, coordinate, number of lanes , width
            #print(way_geo)
            pair=(tup[0],node)  # nodes connected to center or intersection point
            #print(pair)
            #print(beamng_dict[tup[0]],beamng_dict[node])
            three_way.append(pair)
            three_way_coordinate.append(node_dict[node]) # list of lat and long for map plot

#input('Press enter when done...')
# # Create required road for BeamNG
# graph_edges = graph.edges
#
road_a_plt = []
for sample in three_way:
    point1 = list(beamng_dict[sample[0]])
    point2 = list(beamng_dict[sample[1]])
    road_a_plt.append(point1)
    road_a_plt.append(point2)


plta1, plta2 = zip(*road_a_plt)
plt.plot(plta1,plta2,'k-')

road_a_distance = 15
road_b_distance = 15

def getDistance(node_a,node_b):
    dist = math.sqrt((node_a[1] - node_b[1]) ** 2 + (node_a[0] - node_b[0]) ** 2)
    return dist

def getPolyLineCoordinates1(node_a,node_b, distance,width):
    #print("get polyline coordinate")
    # Assumption. width from the center of the road.
    real_distance = getDistance(node_a,node_b)
    t = distance / real_distance

    if t == 0.0:
        t = 0.05

    point2 = (((1 - t) * node_a[0] + t * node_b[0]), ((1 - t) * node_a[1] + t * node_b[1]))

    dx = float(point2[0] - node_a[0])
    dy = float(point2[1] - node_a[1])

    L = float(math.sqrt(float(float(dx * dx) + float(dy * dy)))) # handle division by zero
    U = (float(dy / L), float(dx / L))
    F = float(width)

    # Point on one side
    x2p = float(point2[0] + U[0] * F)
    y2p = float(point2[1] + U[1] * F)

    return x2p,y2p


def getPolyLineCoordinates2(node_a,node_b, distance,width):
    #print("get polyline coordinate")
    # Assumption. width from the center of the road.
    real_distance = getDistance(node_a,node_b)
    t = distance / real_distance

    if t == 0.0:
        t = 0.05

    point2 = (((1 - t) * node_a[0] + t * node_b[0]), ((1 - t) * node_a[1] + t * node_b[1]))

    dx = float(point2[0] - node_a[0])
    dy = float(point2[1] - node_a[1])

    L = float(math.sqrt(float(float(dx * dx) + float(dy * dy)))) # handle division by zero
    U = (float(dy / L), float(dx / L))
    F = float(width)

    # Point on one side
    x2p = float(point2[0] - U[0] * F)
    y2p = float(point2[1] - U[1] * F)

    return x2p,y2p

def getV1BeamNGCoordinaes(total_distance_v1, width):
    global road_a
    v1_roads = road_a # coordinates of roads.
    v1_roads_distance = road_a_distance
    #print(v1_roads_distance)
    v1_road_max = float(total_distance_v1 * v1_roads_distance)
    #print(v1_road_max)
    beamng_pos = ""
    v1_poly_distance = v1_road_max
    for node in v1_roads:
        #node_distance = getDistance(beamng_dict[node[0]],beamng_dict[node[1]])
        node_distance = getDistance(v1_roads[0], v1_roads[1])
        v1_poly_distance = v1_poly_distance - node_distance
        if v1_poly_distance < 0:
            v1_poly_distance = v1_poly_distance + node_distance
            #print("road found")
            #beamng_pos =   getPolyLineCoordinates(beamng_dict[node[0]],beamng_dict[node[1]],v1_poly_distance,width)
            beamng_pos = getPolyLineCoordinates1(v1_roads[0], v1_roads[1], v1_poly_distance, width)
            break

    #print(beamng_pos)
    return beamng_pos




def getV2BeamNGCoordinaes(total_distance_v2, width):
    global  road_b
    #print("beamng v2 coordinates")
    #print(total_distance_v2)
    v2_roads = road_b
    v2_roads_distance = road_b_distance
    v2_road_max = float(total_distance_v2 * v2_roads_distance)
    #print(v2_road_max)
    beamng_pos = ""
    v2_poly_distance = v2_road_max
    for node in v2_roads:
        #node_distance = getDistance(beamng_dict[node[0]],beamng_dict[node[1]])
        node_distance = getDistance(v2_roads[0], v2_roads[1])
        v2_poly_distance = v2_poly_distance - node_distance

        if v2_poly_distance < 0:
            v2_poly_distance = v2_poly_distance + node_distance
            #print("road found")
            #beamng_pos = getPolyLineCoordinates(beamng_dict[node[0]],beamng_dict[node[1]], v2_poly_distance, width)
            beamng_pos = getPolyLineCoordinates2(v2_roads[0], v2_roads[1], v2_poly_distance, width)
            break

    print(beamng_pos)
    return beamng_pos


# Decoding of population chromosome
def decoding_of_parameter(chromosome):
    print("decoding of parameters")

    # rotation of the car in beamng scenario

    # Speed
    v1_speed = int(str(chromosome[V1_SPEED_INDEX]))
    v2_speed = int(str(chromosome[V2_SPEED_INDEX]))

    # point of impact
    radius = chromosome[POINT_OF_IMPACT_RADIUS] % 1
    angle_str = str(chromosome[POINT_OF_IMPACT_ANGLE])
    angle = int(angle_str) % 360

    # point of impact (collision point  provided by user)
    # https://stackoverflow.com/questions/2912779/how-to-calculate-a-point-with-an-given-center-angle-and-radius

    point_of_impact_x = IMPACT_POSITION_X + radius * math.cos(math.radians(angle)) # radians
    point_of_impact_y = IMPACT_POSITION_Y + radius * math.sin(math.radians(angle))  # radians
    impact_point = (point_of_impact_x,point_of_impact_y)


    # position length
    total_distance_v1 = float(int(str(chromosome[V1_DISTANCE_INDEX_1]) + str(chromosome[V1_DISTANCE_INDEX_2])) / 50)
    v1_pos_bg = getV1BeamNGCoordinaes(total_distance_v1,  chromosome[V1_WIDTH_INDEX] % 4)  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint

    total_distance_v2 = float(int(str(chromosome[V2_DISTANCE_INDEX_1]) + str(chromosome[V2_DISTANCE_INDEX_2])) / 50)
    v2_pos_bg = getV2BeamNGCoordinaes(total_distance_v2, chromosome[V2_WIDTH_INDEX] % 4)  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint

    return v1_speed, v1_pos_bg, v2_speed, v2_pos_bg, impact_point

collision_points = []
striker_points = []
victim_points = []

initial_population = [[np.random.randint(1,9) for i in range(10)] for j in range(5)]

population_gen_1 = []
population_gen_1.append([18, 1, 3, 1, 68, 3, 3, 8, 1, 567])
population_gen_1.append([52, 4, 2, 8, 35, 4, 3, 5, 7, 434])
population_gen_1.append([77, 6, 4, 8, 64, 5, 3, 1, 8, 681])
population_gen_1.append([31, 5, 2, 8, 42, 5, 6, 4, 3, 554])
population_gen_1.append([48, 8, 1, 5, 56, 8, 2, 5, 3, 675])

population_gen_2 = []
population_gen_2.append([18, 1, 3, 1, 68, 3, 3, 8, 1, 567])
population_gen_2.append([31, 5, 2, 8, 42, 5, 6, 4, 3, 554])
population_gen_2.append([77, 6, 4, 8, 64, 5, 3, 1, 8, 681])
population_gen_2.append([52, 4, 2, 8, 35, 4, 3, 5, 7, 434])
population_gen_2.append([48, 8, 1, 5, 56, 8, 2, 5, 3, 675])

population_gen_20 = []
population_gen_20.append([18, 1, 3, 1, 68, 3, 3, 8, 1, 567])

for chromosome in population_gen_20:
    print(chromosome)
    beamng_parameters = decoding_of_parameter(chromosome)
    print(beamng_parameters)
    striker_points.append(beamng_parameters[1])
    victim_points.append(beamng_parameters[3])
    collision_points.append(beamng_parameters[4])

slist1, slist2 = zip(*striker_points)
clist1, clist2 = zip(*collision_points)
vlist1, vlist2 = zip(*victim_points)

plt.scatter(slist1, slist2, c='blue', alpha=0.5, label='striker')
plt.scatter(clist1, clist2, c='red', alpha=0.5, label='collision')
plt.scatter(vlist1, vlist2, c='green', alpha=0.5, label='victim')

plt.legend(loc='best')
plt.show()

