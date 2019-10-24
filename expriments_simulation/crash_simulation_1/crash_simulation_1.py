import json
import pickle
import csv
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import numpy as np
import math
from math import atan2,degrees

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
road_a = [(0,0),(30,0)] # add the coordinates of the road here
road_b = [(30,30),(30,0)] # add the cooridinates of the road here
road_c = [(60,0),(30,0)] # add the cooridinates of the road here
road_a_distance = 40
road_b_distance = 40
road_c_distance = 40


# load configuration of the simulations
def ReadJsonFile():
    with open("crash_simulation_1.json", "r") as read_file:
        data = json.load(read_file)
        return data


# csv file to save the results of the simulation
def Create_csv_file():
    csv_columns = ['case_id']
    csv_file = experimental_settings['crash_report_id'] + ".csv"
    try:
        with open(csv_file, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns, delimiter=',', lineterminator='\n')
            writer.writeheader()
    except IOError:
        print("I/O error")


# load the required roads trajectory for simulation
experimental_settings = ReadJsonFile()
filename = experimental_settings['crash_report_id']
map_ways_serialize = filename + '.ways.serialize'
map_nodes_serialize = filename + '.nodes.serialize'
map_beamng_serialize = filename + '.nodes.serialize.beamng'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
print("BeamNG Nodes Loaded")

# dictionary to save the data in csv file.
vehicle_crash_dict = {}

# Create CSV file.
Create_csv_file()

# Create BeamNG road Scenario
beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
scenario = Scenario('GridMap', 'crash_simulation_1')


# create vehicles
vehicleStriker = Vehicle('striker', model='etk800', licence='PYTHON', colour='White')
vehicleVictim = Vehicle('victim', model='etk800', licence='PYTHON', colour='White')


# Create required road for BeamNG
# graph_edges = graph.edges

# for sample in graph_edges:
#     road_a = Road('track_editor_C_center', looped=False)
#     point1 = list(beamng_dict[sample[0]])
#     point2 = list(beamng_dict[sample[1]])
#
#     nodes0 = [
#         (point1[0], point1[1], -4, 4), # method to get the road width from elastic search or number of lanes. (forward and backward)
#         (point2[0], point2[1], -4, 4)
#     ]
#
#     road_a.nodes.extend(nodes0)
#     scenario.add_road(road_a)

def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return degrees(atan2(changeInY,changeInX)) #remove degrees if you want your answer in radians

def getPolyLineCoordinates(node_a,node_b, distance,width):
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
    U = (float(-dy / L), float(dx / L))
    F = float(width)

    # Point on one side
    x2p = float(point2[0] + U[0] * F)
    y2p = float(point2[1] + U[1] * F)

    return x2p,y2p


def getDistance(node_a,node_b):
    dist = math.sqrt((node_a[1] - node_b[1]) ** 2 + (node_a[0] - node_b[0]) ** 2)
    return dist


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
        node_distance = getDistance(beamng_dict[node[0]],beamng_dict[node[1]])
        v1_poly_distance = v1_poly_distance - node_distance
        if v1_poly_distance < 0:
            v1_poly_distance = v1_poly_distance + node_distance
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
            v2_poly_distance = v2_poly_distance + node_distance
            #print("road found")
            beamng_pos = getPolyLineCoordinates(beamng_dict[node[0]],beamng_dict[node[1]], v2_poly_distance, width)
            break

    return beamng_pos





# genetic algorithm iteration with waypoints, velocity and collision point.
def generateRandomPopulation(N=10,Gene=14):
    print("random population")
    initial_population = [[np.random.randint(0,9) for i in range(Gene)] for j in range(N)]
    return initial_population


# Decoding of population chromosome
def decoding_of_parameter(chromosome):
    print("decoding of parameters")

    # rotation of the car in beamng scenario

    # Speed
    v1_speed = int(str(chromosome[V1_SPEED_INDEX_1]) + str(chromosome[V1_SPEED_INDEX_2]))
    v2_speed = int(str(chromosome[V2_SPEED_INDEX_1]) + str(chromosome[V2_SPEED_INDEX_2]))

    # point of impact
    radius = chromosome[POINT_OF_IMPACT_RADIUS] % 4
    angle_str = str(chromosome[POINT_OF_IMPACT_ANGLE_1]) + str(chromosome[POINT_OF_IMPACT_ANGLE_2]) + str(chromosome[POINT_OF_IMPACT_ANGLE_3])
    angle = int(angle_str) % 360

    # point of impact (collision point  provided by user)
    # https://stackoverflow.com/questions/2912779/how-to-calculate-a-point-with-an-given-center-angle-and-radius

    point_of_impact_x = IMPACT_POSITION_X + radius * math.cos(math.radians(angle)) # radians
    point_of_impact_y = IMPACT_POSITION_Y + radius * math.sin(math.radians(angle))  # radians
    impact_point = (point_of_impact_x,point_of_impact_y)


    # position length
    total_distance_v1 = float(int(str(chromosome[V1_DISTANCE_INDEX_1]) + str(chromosome[V1_DISTANCE_INDEX_2])) / 50)
    v1_pos_bg = getV1BeamNGCoordinaes(total_distance_v1,  chromosome[V1_WIDTH_INDEX])  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint

    total_distance_v2 = float(int(str(chromosome[V2_DISTANCE_INDEX_1]) + str(chromosome[V2_DISTANCE_INDEX_2])) / 50)
    v2_pos_bg = getV2BeamNGCoordinaes(total_distance_v2, chromosome[V2_WIDTH_INDEX])  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint

    return v1_speed, v1_pos_bg, v2_speed, v2_pos_bg, impact_point


#initial population
populations = generateRandomPopulation(5,14)

# code to run the simulation and set the fitness of the function.
for population in populations:
    print(population)
    collision_points = []
    striker_points = []
    victim_points = []
    striker_speeds = []
    victim_speeds = []

    beamng_parameters = decoding_of_parameter(population)

    striker_speeds.append(beamng_parameters[0])
    striker_points.append(beamng_parameters[1])
    victim_speeds.append(beamng_parameters[2])
    victim_points.append(beamng_parameters[3])
    collision_points.append(beamng_parameters[4])

    # create beamng scenario and run the simulation.
    # Add it to our scenario at this position and rotation

    # alpha = AngleBtw2Points([5,5],[7,4])
    striker_alpha = AngleBtw2Points(road_a[0],road_a[1])
    victim_alpha = AngleBtw2Points(road_b[0],road_b[1])
    scenario.add_vehicle(vehicleStriker, pos=(striker_points[0][0], striker_points[0][1], 0), rot=(0, 0, striker_alpha)) # get car heading angle
    scenario.add_vehicle(vehicleVictim, pos=(victim_points[0][0], victim_points[0][1], 0), rot=(0, 0, victim_alpha)) # get car heading anlge


    # fit it in the genetic algorithm.
    scenario.make(beamng)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()

        # path for striker vehicle
        node0 = {
            'pos': (striker_points[0][0], striker_points[0][1], 0),
            'speed': 0,
        }

        node1 = {
            'pos': (collision_points[0][0], collision_points[0][1], 0),
            'speed': striker_speeds[0],
        }

        script = list()
        script.append(node0)
        script.append(node1)

        vehicleStriker.ai_set_line(script)


        # path for victim vehicle
        node2 = {
            'pos': (victim_points[0][0], victim_points[0][1], 0),
            'speed': 0,
        }

        node3 = {
            'pos': (collision_points[0][0], collision_points[0][1], 0),
            'speed': victim_speeds[0],
        }

        script = list()
        script.append(node2)
        script.append(node3)

        vehicleVictim.ai_set_line(script)

        input('Press enter when done...')

        bng.stop_scenario()

    finally:
        bng.close()






# Genetic algorithm
# run the simulations
# vehicle state extraction
# save data in csv file.














