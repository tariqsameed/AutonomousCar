import random
import numpy as np

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


populations_fitness = {}

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
    return population_next[:2]



def tournament_parent_selection(populations, n=2, tsize=5):
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
                fittest_population_in_tournament = random.randint(1,10) # assign the fitness of current chromosome.
                current = candidate

            if populations_fitness[tuple(candidate)] > fittest_population_in_tournament:
                current = candidate

        selected_candidates.append(current)

    print(selected_candidates)
    return selected_candidates # it becomes the matinn pool
    #https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35


def setPopulationFitness(population):
    print("set initial fitness")
    for chromosome in population:
        populations_fitness[tuple(chromosome)] = random.randint(1,10)

    print(populations_fitness)



def generateRandomPopulation(N=10,Gene=14):
    print("random population")
    initial_population = [[np.random.randint(0,9) for i in range(Gene)] for j in range(N)]
    return initial_population


populations = generateRandomPopulation(10,14)
setPopulationFitness(populations)
selected_parents = tournament_parent_selection(populations)
next_population = crossover_mutation(selected_parents=selected_parents)
setPopulationFitness(populations)
#populations_fitness = sorted(populations_fitness.items(), key=lambda x: x[1], reverse=True)
print(len(populations_fitness))
# Elitism.
# https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35

#https://stackoverflow.com/questions/2582138/finding-and-replacing-elements-in-a-list
#https://thispointer.com/python-how-to-sort-a-dictionary-by-key-or-value/
