import random
import numpy as np

populations_fitness = {}

def setPopulationFitness(population):
    print("set initial fitness")
    for chromosome in population:
        populations_fitness[tuple(chromosome)] = random.randint(1,10)

    print(populations_fitness)



def generateRandomPopulation(N=10,Gene=14):
    print("random population")
    initial_population = [[np.random.randint(0,9) for i in range(Gene)] for j in range(N)]
    print(initial_population)
    return initial_population


populations = generateRandomPopulation(10,14)
setPopulationFitness(populations)
# update the dictonary with new generation.
populations_fitness_tuples = sorted(populations_fitness.items(), key=lambda x: x[1],  reverse=True)
populations_fitness = dict((x, y) for x, y in populations_fitness_tuples)
print(populations_fitness)
print(len(populations_fitness))
populations_fitness.popitem()
populations_fitness.popitem()
print(len(populations_fitness))
print(populations_fitness)
# convert dictionary keys to population.