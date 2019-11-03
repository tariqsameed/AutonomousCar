import numpy as np
import math
import random

from expriments_simulation.crash_simulation_2.crash_simulation_helper import getV1BeamNGCoordinaes, getV2BeamNGCoordinaes


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
    radius = chromosome[POINT_OF_IMPACT_RADIUS] % 1
    angle_str = str(chromosome[POINT_OF_IMPACT_ANGLE_1]) + str(chromosome[POINT_OF_IMPACT_ANGLE_2]) + str(chromosome[POINT_OF_IMPACT_ANGLE_3])
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
