import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import time
from beamngpy.sensors import Electrics, Damage
import math
from expriments_simulation.crash_simulation_2.genetic_algorithm_helper import generateRandomPopulation, decoding_of_parameter
from expriments_simulation.crash_simulation_2.crash_simulation_helper import AngleBtw2Points, getDistance
from expriments_simulation.crash_simulation_2.vehicle_state_helper import DamageExtraction, DistanceExtraction, RotationExtraction

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
        (point1[0], point1[1], -4, 4), # method to get the road width from elastic search or number of lanes. (forward and backward)
        (point2[0], point2[1], -4, 4)
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
IMPACT_POSITION_X = 308.46771202670277
IMPACT_POSITION_Y = 39.318581604695254

# roads for striker and victim vehicle.
road_striker = [(303.3618974852293, 19.92615900347052),(308.46771202670277, 39.318581604695254)]
road_victim =  [(271.3365218368745, 48.091873711762084),(308.46771202670277, 39.318581604695254)]

actual_striker_damage = "L"
actual_victim_damage = "F"

# parameters for vehicle state extraction
positions = list()
directions = list()
damages = list()

populations_fitness = {} # fitness function to store fitness values of chromosomes.

#initial population
populations = generateRandomPopulation(5,14)
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
    print(beamng_parameters)
    striker_speeds.append(beamng_parameters[0])
    striker_points.append(beamng_parameters[1])
    victim_speeds.append(beamng_parameters[2])
    victim_points.append(beamng_parameters[3])
    collision_points.append(beamng_parameters[4])

    # create beamng scenario and run the simulation.
    # Add it to our scenario at this position and rotation

    # alpha = AngleBtw2Points([5,5],[7,4])
    striker_alpha = AngleBtw2Points(road_striker[0],road_striker[1])
    victim_alpha = AngleBtw2Points(road_victim[0],road_victim[1])

    print("striker angle")
    print(striker_alpha)
    print("victim angle")
    print(victim_alpha)


    scenario.add_vehicle(vehicleStriker, pos=(striker_points[0][0], striker_points[0][1], 0), rot=(0, 0, 192)) # get car heading angle
    scenario.add_vehicle(vehicleVictim, pos=(victim_points[0][0], victim_points[0][1], 0), rot=(0, 0, -85))


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
            time.sleep(0.25)

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

                break


        bng.stop_scenario()

    finally:
        bng.close()