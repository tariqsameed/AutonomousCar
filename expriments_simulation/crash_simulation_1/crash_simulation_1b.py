import json
import pickle
import csv
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import numpy as np
import math
import time
from math import atan2,degrees
from beamngpy.sensors import Electrics, Damage
import random


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

populations_fitness = {} # fitness function to store fitness values of chromosomes.

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

# node_dict = pickle.load(open(map_nodes_serialize, "rb"))
# print("Nodes Loaded")
#
# graph = pickle.load(open(map_ways_serialize, "rb"))
# print("Graph Loaded")
#
# beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
# print("BeamNG Nodes Loaded")


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

electricsStriker = Electrics()
damageStriker = Damage();
vehicleStriker.attach_sensor('electricsS', electricsStriker);
vehicleStriker.attach_sensor('damagesS', damageStriker);

electricsVictim = Electrics()
damageVictim = Damage();
vehicleVictim.attach_sensor('electricsV', electricsVictim);
vehicleVictim.attach_sensor('damagesV', damageVictim);

positions = list()
directions = list()
wheel_speeds = list()
throttles = list()
brakes = list()
damages = list()

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

# Temporary road.
roads = Road('track_editor_C_center', looped=False)
nodesA = [(road_a[0][0],road_a[0][1], -4, 4),(road_a[1][0],road_a[1][1], -4, 4)]
nodesB = [(road_b[0][0],road_b[0][1], -4, 4),(road_b[1][0],road_b[1][1], -4, 4)]
nodesC = [(road_c[0][0],road_c[0][1], -4, 4),(road_c[1][0],road_c[1][1], -4, 4)]

roads.nodes.extend(nodesA)
roads.nodes.extend(nodesB)
roads.nodes.extend(nodesC)
scenario.add_road(roads)


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
        #node_distance = getDistance(beamng_dict[node[0]],beamng_dict[node[1]])
        node_distance = getDistance(v1_roads[0], v1_roads[1])
        v1_poly_distance = v1_poly_distance - node_distance
        if v1_poly_distance < 0:
            v1_poly_distance = v1_poly_distance + node_distance
            #print("road found")
            #beamng_pos =   getPolyLineCoordinates(beamng_dict[node[0]],beamng_dict[node[1]],v1_poly_distance,width)
            beamng_pos = getPolyLineCoordinates(v1_roads[0], v1_roads[1], v1_poly_distance, width)
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
            beamng_pos = getPolyLineCoordinates(v2_roads[0], v2_roads[1], v2_poly_distance, width)
            break

    print(beamng_pos)
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


def tournament_parent_selection(populations, n=2, tsize=4):
    global populations_fitness
    print('tournament selection')
    selected_candidates = []
    for i in range(n):
        fittest_population_in_tournament = None
        candidates = random.sample(populations, tsize) #tsize = 20% of population.
        print(candidates)
        current = None
        for candidate in candidates:
            if fittest_population_in_tournament is None:
                fittest_population_in_tournament = populations_fitness[tuple(candidate)] # assign the fitness of current chromosome.
                current = candidate

            if populations_fitness[tuple(candidate)] > fittest_population_in_tournament:
                current = candidate

        selected_candidates.append(current)

    print(selected_candidates)
    return selected_candidates # it becomes the matinn pool
    #https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35


def mutation(chromosome):
    print("mutation")
    chromosome[random.randint(0, len(chromosome) - 1)] = random.randint(min(chromosome), max(chromosome) - 1)
    return  chromosome


def crossover(chromosome1,chromosome2):
    print("crossover")
    crossover_point = random.randint(1, len(chromosome1) - 1)

    # Create children. np.hstack joins two arrays
    child_1 = np.hstack((chromosome1[0:crossover_point],
                         chromosome2[crossover_point:]))

    child_2 = np.hstack((chromosome2[0:crossover_point],
                         chromosome1[crossover_point:]))

    # Return children
    return child_1, child_2



def crossover_mutation(selected_parents):
    print("crossover mutation")
    # https://stackoverflow.com/questions/20161980/difference-between-exploration-and-exploitation-in-genetic-algorithm?rq=1
    population_next = []
    n = 2
    for i in range(int(len(selected_parents) / 2)):
        for j in range(n): # number of children
            chromosome1, chromosome2 = selected_parents[i], selected_parents[len(selected_parents) - 1 - i]
            childs = crossover(chromosome1,chromosome2)
            for child in childs:
                population_next.append(mutation(child.tolist()))


    print(population_next)
    return population_next



def multiObjectiveFitnessFunction(population, striker_damage, striker_distance, striker_rotation, victim_damage, victim_distance, victim_rotation):
    print("multiobjective fitness function")
    return 5.0

# Genetic Algorithm Simulation Start from here.

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
    print(beamng_parameters)
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

    print(striker_alpha)
    print(victim_alpha)

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

        #vehicle state extraction and fitness function here
        for _ in range(15):
            print("vehicle state extraction")
            time.sleep(1.0)


        # striker vehhicle state extraction
        vehicleStriker.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
        sensorsStriker = bng.poll_sensors(vehicleStriker)  # Polls the data of all sensors attached to the vehicle
        striker_position = vehicleStriker.state['pos']
        striker_direction = vehicleStriker.state['dir']
        striker_damage = sensorsStriker['damagesS']

        # victim vehicle state extraction
        vehicleVictim.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
        sensorsVictim = bng.poll_sensors(vehicleVictim)  # Polls the data of all sensors attached to the vehicle
        victim_position = vehicleVictim.state['pos']
        victim_direction = vehicleVictim.state['dir']
        victim_damage = sensorsVictim['damagesV']

        print("multiobjective fitness function")
        score = multiObjectiveFitnessFunction(population, striker_damage, striker_position, striker_direction,
                                              victim_damage, victim_position, victim_direction)
        populations_fitness[tuple(population)] = score
        #input('Press enter when done...')
        bng.stop_scenario()

    finally:
        bng.close()

# start here -  genetic algorithm simulation.

for _ in range(5): # Number of Generations to be Iterated.
    print("genetic algorithm simulation")
    selected_parents = tournament_parent_selection(populations)
    next_population = crossover_mutation(selected_parents=selected_parents)

    for children in next_population:
        print("iteration of children")
        collision_points = []
        striker_points = []
        victim_points = []
        striker_speeds = []
        victim_speeds = []

        beamng_parameters = decoding_of_parameter(population)
        print(beamng_parameters)
        striker_speeds.append(beamng_parameters[0])
        striker_points.append(beamng_parameters[1])
        victim_speeds.append(beamng_parameters[2])
        victim_points.append(beamng_parameters[3])
        collision_points.append(beamng_parameters[4])

        # create beamng scenario and run the simulation.
        # Add it to our scenario at this position and rotation

        # alpha = AngleBtw2Points([5,5],[7,4])
        striker_alpha = AngleBtw2Points(road_a[0], road_a[1])
        victim_alpha = AngleBtw2Points(road_b[0], road_b[1])

        print(striker_alpha)
        print(victim_alpha)

        scenario.add_vehicle(vehicleStriker, pos=(striker_points[0][0], striker_points[0][1], 0),
                             rot=(0, 0, striker_alpha))  # get car heading angle
        scenario.add_vehicle(vehicleVictim, pos=(victim_points[0][0], victim_points[0][1], 0),
                             rot=(0, 0, victim_alpha))  # get car heading anlge

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

            # vehicle state extraction and fitness function here
            for _ in range(15):
                print("vehicle state extraction")
                time.sleep(1.0)

                # striker vehhicle state extraction
                vehicleStriker.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                sensorsStriker = bng.poll_sensors(vehicleStriker)  # Polls the data of all sensors attached to the vehicle
                striker_position = vehicleStriker.state['pos']
                striker_direction = vehicleStriker.state['dir']
                striker_damage = sensorsStriker['damages']

                # victim vehicle state extraction
                vehicleVictim.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                sensorsVictim = bng.poll_sensors(vehicleVictim)  # Polls the data of all sensors attached to the vehicle
                victim_position = vehicleVictim.state['pos']
                victim_direction = vehicleVictim.state['dir']
                victim_damage = sensorsVictim['damages']

                print("multiobjective fitness function")
                score = multiObjectiveFitnessFunction(children, striker_damage, striker_position, striker_direction, victim_damage,
                                                      victim_position, victim_direction)
                populations_fitness[tuple(population)] = score

            # input('Press enter when done...')
            bng.stop_scenario()


        finally:
            bng.close()

        if children not in populations:
            populations.append(children)

        temporary_fitness_dict = {}

        for pop in populations:
            temporary_fitness_dict[tuple(pop)] = populations_fitness[tuple(pop)]


        populations_fitness_tuples = sorted(temporary_fitness_dict.items(), key=lambda x: x[1], reverse=True)
        populations_fitness = dict((x, y) for x, y in populations_fitness_tuples)
        print(populations_fitness)
        populations_fitness.popitem()
        print(len(populations_fitness))
        populations = list(populations_fitness.keys())


    # order the iteration with respect to fitness function for the next generation.
    # create a temporary fitness dictionary.
    # make sure 10 sample in population.


# Genetic algorithm
# run the simulations
# vehicle state extraction
# save data in csv file.














