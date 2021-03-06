import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import time
from beamngpy.sensors import Electrics, Damage
import math
import random
import numpy as np
from experiments_simulation_modified.crash_simulation_2.crash_simulation_helper import getV1BeamNGCoordinaes, getV2BeamNGCoordinaes
from experiments_simulation_modified.crash_simulation_2.crash_simulation_helper import AngleBtw2Points, getDistance
from experiments_simulation_modified.crash_simulation_2.vehicle_state_helper import DamageExtraction, DistanceExtraction, RotationExtraction
import csv
import sys
sys.stdout = open('output.txt','w')

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
scenario = Scenario('GridMap', 'crash_simulation_2')

road_a = Road('custom_track_center', looped=False)

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
            way_geo = (node, node_dict[node], lane_dict[tup[0]], width_dict[tup[0]], beamng_dict[node]) # node, coordinate, number of lanes , width
            print(way_geo)
            pair=(tup[0],node)  # nodes connected to center or intersection point
            #print(pair)
            #print(beamng_dict[tup[0]],beamng_dict[node])
            three_way.append(pair)
            three_way_coordinate.append(node_dict[node]) # list of lat and long for map plot

# # Create required road for BeamNG
# graph_edges = graph.edges
#
for sample in three_way:
    print("3 way")
    road_a = Road('custom_track_center', looped=False)

    point1 = list(beamng_dict[sample[0]])
    point2 = list(beamng_dict[sample[1]])

    #print(getDistance(point1,point2))

    nodes0 = [
        (point1[0], point1[1], 0, 8), # method to get the road width from elastic search or number of lanes. (forward and backward)
        (point2[0], point2[1], 0, 8)
    ]

    road_a.nodes.extend(nodes0)
    scenario.add_road(road_a)



vehicleStriker = Vehicle('striker', model='etk800', licence='Striker', colour='Yellow')
damageStriker = Damage();
vehicleStriker.attach_sensor('damagesS', damageStriker);

vehicleVictim = Vehicle('victim', model='etk800', licence='Victim', colour='White')
damageVictim = Damage();
vehicleVictim.attach_sensor('damagesV', damageVictim);

# road creation  and vehicle initializatoin with sensors completed.-------------------------------------------

def getDistance(node_a,node_b):
    dist = math.sqrt((node_a[1] - node_b[1]) ** 2 + (node_a[0] - node_b[0]) ** 2)
    return dist


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
IMPACT_POSITION_X = 308.46771202670277
IMPACT_POSITION_Y = 39.318581604695254

# roads for striker and victim vehicle.
road_striker = [(303.3618974852293, 19.92615900347052),(308.46771202670277, 39.318581604695254)]
road_victim =  [(271.612527256231, 48.38151988796675),(308.46771202670277, 39.318581604695254)]

actual_striker_damage = "L"
actual_victim_damage = "F"

# parameters for vehicle state extraction
positions = list()
directions = list()
damages = list()

populations_fitness = {} # fitness function to store fitness values of chromosomes.

# ----------------------------- genetic algorithm helper --------------------
def generateRandomPopulation(N=5,Gene=10):
    print("random population")
    random_population = []
    random_population.append([1, 8, 1, 3, 1, 6, 8, 3, 3, 8, 1, 5, 6, 7])
    seed_population = [[np.random.randint(1,9) for i in range(Gene + 4)] for j in range(N - 1)]
    for i, val in enumerate(seed_population):
        random_population.append(val)

    print(random_population)
    initial_population = convertPopulation(random_population)
    return initial_population


def convertPopulation(random_population):
    print("convert population")
    converted_population = []
    for i, val in enumerate(random_population):
        merge_list = []
        merge_list.append(int(str(val[0]) + str(val[1])))
        merge_list.append(val[2])
        merge_list.append(val[3])
        merge_list.append(val[4])
        merge_list.append(int(str(val[5]) + str(val[6])))
        merge_list.append(val[7])
        merge_list.append(val[8])
        merge_list.append(val[9])
        merge_list.append(val[10])
        merge_list.append(int(str(val[11]) + str(val[12]) + str(val[13])))
        converted_population.append(merge_list)

    return converted_population


def shrinkChromosome(chromosome):
    merge_chromosome = []
    merge_chromosome.append(int(str(chromosome[0]) + str(chromosome[1])))
    merge_chromosome.append(chromosome[2])
    merge_chromosome.append(chromosome[3])
    merge_chromosome.append(chromosome[4])
    merge_chromosome.append(int(str(chromosome[5]) + str(chromosome[6])))
    merge_chromosome.append(chromosome[7])
    merge_chromosome.append(chromosome[8])
    merge_chromosome.append(chromosome[9])
    merge_chromosome.append(chromosome[10])
    merge_chromosome.append(int(str(chromosome[11]) + str(chromosome[12]) + str(chromosome[13])))
    return merge_chromosome


def expandChromosome(chromosome):
    expand_chromosome = []
    speed_striker = [int(d) for d in str(chromosome[0])]
    expand_chromosome.append(speed_striker[0])
    expand_chromosome.append(speed_striker[1])
    expand_chromosome.append(chromosome[1])
    expand_chromosome.append(chromosome[2])
    expand_chromosome.append(chromosome[3])
    speed_victim = [int(d) for d in str(chromosome[4])]
    expand_chromosome.append(speed_victim[0])
    expand_chromosome.append(speed_victim[1])
    expand_chromosome.append(chromosome[5])
    expand_chromosome.append(chromosome[6])
    expand_chromosome.append(chromosome[7])
    expand_chromosome.append(chromosome[8])
    angle = [int(d) for d in str(chromosome[9])]
    expand_chromosome.append(angle[0])
    expand_chromosome.append(angle[1])
    expand_chromosome.append(angle[2])
    return expand_chromosome


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


# --------------------------- genetic algorithm helper  ----------------------

#initial population
populations = generateRandomPopulation(5,14)
print('initial population')
print(populations)

# code to run the simulation and set the fitness of the function.
for population in populations:
    print(population)
    collision_points = []
    striker_points = []
    victim_points = []
    striker_speeds = []
    victim_speeds = []

    beamng_parameters = decoding_of_parameter(population)
    print('beamng parameters')
    print(beamng_parameters)
    striker_speeds.append(beamng_parameters[0])
    striker_points.append(beamng_parameters[1])
    victim_speeds.append(beamng_parameters[2])
    victim_points.append(beamng_parameters[3])
    collision_points.append(beamng_parameters[4])

    # create beamng scenario and run the simulation.
    # Add it to our scenario at this position and rotation

    # alpha = AngleBtw2Points([5,5],[7,4])
    striker_alpha = AngleBtw2Points(road_striker[1], road_striker[0])
    victim_alpha = AngleBtw2Points(road_victim[1], road_victim[0])

    # print("striker angle")
    # print(striker_alpha)
    # print("victim angle")
    # print(victim_alpha)

    scenario.add_vehicle(vehicleVictim, pos=(victim_points[0][0], victim_points[0][1], 0), rot=(0, 0, -80))
    scenario.add_vehicle(vehicleStriker, pos=(striker_points[0][0], striker_points[0][1], 0), rot=(0, 0, 192)) # get car heading angle


    # save values to dictionary
    pos_crash_dict["chromosome"] = population
    pos_crash_dict["v1_speed"]  = striker_speeds[0]
    pos_crash_dict["v1_waypoint"] = striker_points[0]
    pos_crash_dict["v2_speed"] = victim_speeds[0]
    pos_crash_dict["v2_waypoint"] = victim_points[0]

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

        for number in range(60):
            time.sleep(0.20)

            vehicleStriker.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
            sensors = bng.poll_sensors(vehicleStriker)  # Polls the data of all sensors attached to the vehicle
            #print(vehicleStriker.state['pos'])
            if vehicleStriker.state['pos'][0] > 306 and vehicleStriker.state['pos'][1] > 39:
                # print('free state')
                vehicleStriker.control(throttle=0, steering=0, brake=0, parkingbrake=0)
                vehicleStriker.update_vehicle()



            vehicleVictim.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
            sensors = bng.poll_sensors(vehicleVictim)  # Polls the data of all sensors attached to the vehicle
            #print(vehicleStriker.state['pos'])
            if vehicleVictim.state['pos'][0] > 306 and vehicleVictim.state['pos'][1] > 39:
                #print('free state')
                vehicleVictim.control(throttle=0, steering=0, brake=0, parkingbrake=0)
                vehicleVictim.update_vehicle()


            if number > 58:

                # striker vehhicle state extraction
                striker_damage = {}
                vehicleStriker.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                sensorsStriker = bng.poll_sensors(vehicleStriker)  # Polls the data of all sensors attached to the vehicle
                striker_position = vehicleStriker.state['pos']
                striker_direction = vehicleStriker.state['dir']
                if 'damagesS' in sensorsStriker:
                    striker_damage = sensorsStriker['damagesS']


                # victim vehicle state extraction
                victim_damage = {}
                vehicleVictim.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                sensorsVictim = bng.poll_sensors(vehicleVictim)  # Polls the data of all sensors attached to the vehicle
                victim_position = vehicleVictim.state['pos']
                victim_direction = vehicleVictim.state['dir']
                if 'damagesV' in sensorsVictim:
                    victim_damage = sensorsVictim['damagesV']


                # multiobjective fitness function.
                multiObjectiveFitnessScore = 0
                critical_damage_score = DamageExtraction(striker_damage, victim_damage, actual_striker_damage, actual_victim_damage)
                distance_score = DistanceExtraction(striker_speeds[0],striker_position,collision_points[0], victim_speeds[0],victim_position, collision_points[0])
                rotation_score = RotationExtraction(striker_points[0], collision_points[0], striker_position, victim_points[0], collision_points[0], victim_position)

                print("multiObjectiveFitnessScore")
                print(critical_damage_score)
                print(distance_score)
                print(rotation_score)

                multiObjectiveFitnessScore = critical_damage_score[0] + critical_damage_score[1]
                multiObjectiveFitnessScore = multiObjectiveFitnessScore + distance_score[0] + distance_score[1]
                multiObjectiveFitnessScore = multiObjectiveFitnessScore + rotation_score[0] + rotation_score[1]
                print(multiObjectiveFitnessScore)

                # set the fitness function value
                populations_fitness[tuple(population)] = multiObjectiveFitnessScore

                # save value to dictionary.

                pos_crash_dict["striker_damage"] = critical_damage_score[0]
                pos_crash_dict["victim_damage"] = critical_damage_score[1]
                pos_crash_dict["striker_distance"] = distance_score[0]
                pos_crash_dict["victim_distance"] = distance_score[1]
                pos_crash_dict["striker_rotation"] = rotation_score[0]
                pos_crash_dict["victim_rotation"] = rotation_score[1]
                pos_crash_dict["fitness_value"] = multiObjectiveFitnessScore

                if critical_damage_score[0] > 0.0 or critical_damage_score[1] > 0.0:
                    print("critical scenario")
                    saveDictionaryToCsvFile()

                break


        bng.stop_scenario()
        pos_crash_dict = {}

    finally:
        bng.close()

# -------------- save genetic algorithm iterator -------------------------------------
lines = ""
for k, v in populations_fitness.items():
    lines = lines + str(k) + ',' + str(v) + ','

lines = lines[:-1]
f.writelines(lines + '\n')

## -------------------------------- genetic algorithm helper --------------------------

def tournament_parent_selection(populations, n=2, tsize=3):
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
    chromosome = expandChromosome(chromosome)
    chromosome[random.randint(0, len(chromosome) - 1)] = random.randint(min(chromosome), max(chromosome) - 1)
    random.shuffle(chromosome)
    return shrinkChromosome(chromosome)


def crossover(chromosome1, chromosome2):
    print("crossover")
    crossover_point = random.randint(1, len(expandChromosome(chromosome1)) - 1)

    chromosome1 = expandChromosome(chromosome1)
    chromosome2 = expandChromosome(chromosome2)
    # Create children. np.hstack joins two arrays
    child = np.hstack((chromosome1[0:crossover_point],
                         chromosome2[crossover_point:]))
    return shrinkChromosome(child)


def crossover_mutation(selected_parents):
    print("crossover mutation")
    # https://stackoverflow.com/questions/20161980/difference-between-exploration-and-exploitation-in-genetic-algorithm?rq=1
    population_next = []
    n = 1
    for i in range(int(len(selected_parents) / 2)):
        for j in range(n):  # number of children
            chromosome1, chromosome2 = selected_parents[i], selected_parents[len(selected_parents) - 1 - i]
            childs = crossover(chromosome1, chromosome2)
            population_next.append(mutation(childs))

    print(population_next)
    return population_next

## -------------------------------- genetic algorithm helper --------------------------

# iteration of genetic algorithm.
for _ in range(20): # Number of Generations to be Iterated.
    print("genetic algorithm simulation")
    selected_parents = tournament_parent_selection(populations)
    next_population = crossover_mutation(selected_parents=selected_parents)
    print("population")
    print(populations)
    print("selected parents")
    print(selected_parents)
    print("next population")
    print(next_population)

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

        striker_alpha = AngleBtw2Points(road_striker[0], road_striker[1])
        victim_alpha = AngleBtw2Points(road_victim[0], road_victim[1])

        scenario.add_vehicle(vehicleStriker, pos=(striker_points[0][0], striker_points[0][1], 0),
                             rot=(0, 0, 192))  # get car heading angle
        scenario.add_vehicle(vehicleVictim, pos=(victim_points[0][0], victim_points[0][1], 0),
                             rot=(0, 0, -90))  # get car heading anlge

        # save values to dictionary
        pos_crash_dict["chromosome"] = children
        pos_crash_dict["v1_speed"] = striker_speeds[0]
        pos_crash_dict["v1_waypoint"] = striker_points[0]
        pos_crash_dict["v2_speed"] = victim_speeds[0]
        pos_crash_dict["v2_waypoint"] = victim_points[0]


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
            for number in range(60):
                time.sleep(0.20)

                vehicleStriker.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                sensors = bng.poll_sensors(vehicleStriker)  # Polls the data of all sensors attached to the vehicle
                # print(vehicleStriker.state['pos'])
                if vehicleStriker.state['pos'][0] > 306 and vehicleStriker.state['pos'][1] > 39:
                    # print('free state')
                    vehicleStriker.control(throttle=0, steering=0, brake=0, parkingbrake=0)
                    vehicleStriker.update_vehicle()

                vehicleVictim.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                sensors = bng.poll_sensors(vehicleVictim)  # Polls the data of all sensors attached to the vehicle
                # print(vehicleStriker.state['pos'])
                if vehicleVictim.state['pos'][0] > 306 and vehicleVictim.state['pos'][1] > 39:
                    # print('free state')
                    vehicleVictim.control(throttle=0, steering=0, brake=0, parkingbrake=0)
                    vehicleVictim.update_vehicle()

                if number > 58:

                    # striker vehhicle state extraction
                    striker_damage = {}
                    vehicleStriker.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                    sensorsStriker = bng.poll_sensors(
                        vehicleStriker)  # Polls the data of all sensors attached to the vehicle
                    striker_position = vehicleStriker.state['pos']
                    striker_direction = vehicleStriker.state['dir']
                    if 'damagesS' in sensorsStriker:
                        striker_damage = sensorsStriker['damagesS']

                    # victim vehicle state extraction
                    victim_damage = {}
                    vehicleVictim.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
                    sensorsVictim = bng.poll_sensors(
                        vehicleVictim)  # Polls the data of all sensors attached to the vehicle
                    victim_position = vehicleVictim.state['pos']
                    victim_direction = vehicleVictim.state['dir']
                    if 'damagesV' in sensorsVictim:
                        victim_damage = sensorsVictim['damagesV']

                    # multiobjective fitness function.
                    multiObjectiveFitnessScore = 0
                    critical_damage_score = DamageExtraction(striker_damage, victim_damage, actual_striker_damage,
                                                             actual_victim_damage)
                    distance_score = DistanceExtraction(striker_speeds[0], striker_position, collision_points[0],
                                                        victim_speeds[0], victim_position, collision_points[0])
                    rotation_score = RotationExtraction(striker_points[0], collision_points[0], striker_position,
                                                        victim_points[0], collision_points[0], victim_position)

                    print("multiObjectiveFitnessScore")
                    print(critical_damage_score)
                    print(distance_score)
                    print(rotation_score)

                    multiObjectiveFitnessScore = critical_damage_score[0] + critical_damage_score[1]
                    multiObjectiveFitnessScore = multiObjectiveFitnessScore + distance_score[0] + distance_score[1]
                    multiObjectiveFitnessScore = multiObjectiveFitnessScore + rotation_score[0] + rotation_score[1]
                    print(multiObjectiveFitnessScore)

                    # set the fitness function value
                    populations_fitness[tuple(children)] = multiObjectiveFitnessScore

                    # save value to dictionary.

                    pos_crash_dict["striker_damage"] = critical_damage_score[0]
                    pos_crash_dict["victim_damage"] = critical_damage_score[1]
                    pos_crash_dict["striker_distance"] = distance_score[0]
                    pos_crash_dict["victim_distance"] = distance_score[1]
                    pos_crash_dict["striker_rotation"] = rotation_score[0]
                    pos_crash_dict["victim_rotation"] = rotation_score[1]
                    pos_crash_dict["fitness_value"] = multiObjectiveFitnessScore

                    if critical_damage_score[0] > 0 or critical_damage_score[1] > 0:
                        saveDictionaryToCsvFile()

                    break

            # input('Press enter when done...')
            bng.stop_scenario()


        finally:
            bng.close()

        print("adding children")
        print(populations_fitness)
        # add children to population
        # if children not in populations:
        #     populations.append(children)
        #
        #
        #
        #temporary_fitness_dict = {}
        #
        # for pop in populations:
        #     temporary_fitness_dict[tuple(pop)] = populations_fitness[tuple(pop)]


        populations_fitness_tuples = sorted(populations_fitness.items(), key=lambda x: x[1], reverse=True)
        populations_fitness = dict((x, y) for x, y in populations_fitness_tuples)
        print(populations_fitness)
        populations_fitness.popitem()
        print("length")
        print(len(populations_fitness))
        populations = list(populations_fitness.keys())

        # -------------- save genetic algorithm iterator -------------------------------------
        lines = ""
        for k, v in populations_fitness.items():
            lines = lines + str(k) + ',' + str(v) + ','

        lines = lines[:-1]
        f.writelines(lines + '\n')

        ## -------------------------------- genetic algorithm helper --------------------------

        # iteratoin of genetic algorithm finished.





# scenario.make(beamng)
# bng = beamng.open(launch=True)
# try:
#     bng.load_scenario(scenario)
#     bng.start_scenario()
#
#     input('Press enter when done...')
# finally:
#     bng.close()

# [[2, 7, 3, 0, 2, 3, 0, 4, 7, 5, 0, 5, 6, 1], [4, 3, 1, 4, 6, 1, 5, 4, 1, 4, 6, 4, 1, 6], [8, 5, 8, 8, 6, 0, 4, 5, 2, 6, 7, 5, 0, 1], [1, 3, 4, 5, 7, 1, 2, 7, 7, 2, 2, 6, 8, 4], [7, 4, 3, 5, 3, 4, 6, 4, 6, 3, 5, 2, 3, 3]]
