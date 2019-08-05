# Intersection of polylines
# Maximum distance from centriod to perpendicular line of the road.
# Genereate new lane marking based on updated coordinates of polyline
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

filename = 'passau'
path = "../resources/osm/"
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
IMPACT_POSITION_X = 1
IMPACT_POSITION_Y = 2
V1_ROAD_ID = 123456
V2_ROAD_ID = 654321
road_a = ''
road_b = ''
road_c = ''
road_a_distance = 18.545010801854016
road_b_distance = 82.41788560240022
road_c_distance = 47.37948935299994


def getPolyLineCoordinates(node_a,node_b, distance,width):
    #print("get polyline coordinate")
    # Assumption. width from the center of the road.
    real_distance = getDistance(node_a,node_b)
    t = distance / real_distance

    point2 = (((1 - t) * node_a[0] + t * node_b[0]), ((1 - t) * node_a[1] + t * node_b[1]))

    #print(node_a, point2, width)

    dx = float(point2[0] - node_a[0])
    dy = float(point2[1] - node_a[1])

    L = float(math.sqrt(float(float(dx * dx) + float(dy * dy))))
    U = (float(-dy / L), float(dx / L))
    F = float(float(width))

    # Point on one side
    x2p = float(point2[0] - U[0] * F)
    y2p = float(point2[1] - U[1] * F)

    return x2p,y2p


def getDistance(node_a,node_b):
    #print("get distance")
    #print(node_a)
    #print(node_b)
    dist = math.sqrt((node_a[1] - node_b[1]) ** 2 + (node_a[0] - node_b[0]) ** 2)
    return dist


def getV1BeamNGCoordinaes(total_distance_v1, width):
    global road_a
    #print("beamng v1 coordinates")
    #print(total_distance_v1)
    v1_roads = road_a
    v1_roads_distance = road_a_distance
    #print(v1_roads_distance)
    v1_road_max = float(total_distance_v1 * v1_roads_distance)
    #print(v1_road_max)
    beamng_pos = ""
    v1_poly_distance = v1_road_max
    for node in v1_roads:
        node_distance = getDistance(beamng_dict[node[0]],beamng_dict[node[1]])
        v1_poly_distance = v1_poly_distance - node_distance

        if v1_poly_distance < 0:
            #print("road found")
            beamng_pos =   getPolyLineCoordinates(beamng_dict[node[0]],beamng_dict[node[1]],v1_poly_distance,width)
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
        node_distance = getDistance(beamng_dict[node[0]],beamng_dict[node[1]])
        v2_poly_distance = v2_poly_distance - node_distance
        if v2_poly_distance < 0:
            #print("road found")
            beamng_pos = getPolyLineCoordinates(beamng_dict[node[0]],beamng_dict[node[1]], v2_poly_distance, width)
            break

    print(beamng_pos)
    return beamng_pos



def decoding_of_parameter(chromosome):
    #print("decoding of parameters")
    # Speed
    v1_speed = int(str(chromosome[V1_SPEED_INDEX_1]) + str(chromosome[V1_SPEED_INDEX_2]))
    v2_speed = int(str(chromosome[V2_SPEED_INDEX_1]) + str(chromosome[V2_SPEED_INDEX_2]))

    #print (v1_speed)
    #print(v2_speed)
    # point of impact
    radius = chromosome[POINT_OF_IMPACT_RADIUS] % 3
    angle_str = str(chromosome[POINT_OF_IMPACT_ANGLE_1]) + str(chromosome[POINT_OF_IMPACT_ANGLE_2]) + str(chromosome[POINT_OF_IMPACT_ANGLE_3])
    angle = int(angle_str) % 360

    #print(radius)
    #print(angle)
    # point of impact (collision point  provided by user)
    # https://stackoverflow.com/questions/2912779/how-to-calculate-a-point-with-an-given-center-angle-and-radius

    point_of_impact_x = IMPACT_POSITION_X + radius * math.cos(math.radians(angle)) # radians
    point_of_impact_y = IMPACT_POSITION_Y + radius * math.sin(math.radians(angle))  # radians
    impact_point = (point_of_impact_x,point_of_impact_y)
    #print(impact_point)

    # position length
    total_distance_v1 = float(int(str(chromosome[V1_DISTANCE_INDEX_1]) + str(chromosome[V1_DISTANCE_INDEX_2])) / 100)
    v1_pos_bg = getV1BeamNGCoordinaes(total_distance_v1,  chromosome[V1_WIDTH_INDEX])  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint
    #print(v1_pos_bg)

    total_distance_v2 = float(int(str(chromosome[V2_DISTANCE_INDEX_1]) + str(chromosome[V2_DISTANCE_INDEX_2])) / 100)
    v2_pos_bg = getV2BeamNGCoordinaes(total_distance_v2, chromosome[V2_WIDTH_INDEX])  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint
    #print(v2_pos_bg)

    return v1_speed, v1_pos_bg, v2_speed, v2_pos_bg, impact_point


def generateRandomPopulation(N=10,Gene=14):
    #print("random population")
    #print([[np.random.randint(0,9) for i in range(Gene)] for j in range(N)])
    initial_population = [[np.random.randint(0,9) for i in range(Gene)] for j in range(N)]
    return initial_population


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


def getImpactPoint(road):
    point = road[0]
    point = beamng_dict[point[0]]
    return point

def getRoadDistance(road):
    #print("get road distance")
    distance = 0
    for edge in road:
        point1 = beamng_dict[edge[0]]
        point2 = beamng_dict[edge[1]]
        distance = distance + calculateDistance(point1[0],point1[1], point2[0], point2[1])

    return distance

def geneticAlgorithmSimulation():

    global IMPACT_POSITION_X
    global IMPACT_POSITION_Y
    global road_a
    global road_b
    global road_c
    global road_a_distance
    global road_b_distance
    global road_c_distance

    print("Genetic Algorithm Simulation")
    for tup in graph_degree:
        if tup[1] == 3:
            n = 3
            #print(list(nx.dfs_edges(graph, source=tup[0], depth_limit=n)))
            way_3 = list(nx.dfs_edges(graph, source=tup[0], depth_limit=n))

            l = way_3
            way_3 =[l[i:i + n] for i in range(0, len(l), n)]
            road_a = way_3[0]
            road_b = way_3[1]
            road_c = way_3[2]


    road_a_distance = getRoadDistance(road_a)
    road_b_distance = getRoadDistance(road_b)
    road_c_distance = getRoadDistance(road_c)

    impact_point = getImpactPoint(road_a)
    IMPACT_POSITION_X = impact_point[0]
    IMPACT_POSITION_Y = impact_point[1]

    initial_population =  generateRandomPopulation(20)

    collision_points = []
    striker_points = []
    victim_points = []

    for chromosome in initial_population:
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

    road_a = [i[0] for i in road_a]
    road_a_plt = []
    for node in road_a:
        road_a_plt.append(beamng_dict[node])

    plta1, plta2 = zip(*road_a_plt)
    plt.plot(plta1,plta2,'k--')

    road_b = [i[0] for i in road_b]
    road_b_plt = []
    for node in road_b:
        road_b_plt.append(beamng_dict[node])

    pltb1, pltb2 = zip(*road_b_plt)
    plt.plot(pltb1, pltb2, 'k--')

    road_c = [i[0] for i in road_c]
    road_c_plt = []
    for node in road_c:
        road_c_plt.append(beamng_dict[node])

    pltc1, pltc2 = zip(*road_c_plt)
    plt.plot(pltc1, pltc2, 'k--')



    plt.legend(loc='best')
    plt.show()



geneticAlgorithmSimulation()

