import numpy as np
import random

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


def tournament_parent_selection(populations, n=2, tsize=3):
    global populations_fitness
    print('tournament selection')
    selected_candidates = []
    for i in range(n):
        fittest_population_in_tournament = None
        candidates = random.sample(populations, tsize)  # tsize = 20% of population.
        print(candidates)
        current = None
        for candidate in candidates:
            if fittest_population_in_tournament is None:
                fittest_population_in_tournament = populations_fitness[tuple(candidate)]  # assign the fitness of current chromosome.
                current = candidate

            if populations_fitness[tuple(candidate)] > fittest_population_in_tournament:
                current = candidate

        selected_candidates.append(current)

    print(selected_candidates)
    return selected_candidates  # it becomes the matinn pool
    # https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35


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
            print("crossover child")
            print(childs)
            # childs = mutation(childs)
            # for child in childs:
            #     population_next.append(mutation(child.tolist()))
            population_next.append(mutation(childs))

    print(population_next)
    return population_next


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

def generateRandomPopulation(N=5,Gene=10):
    print("random population")
    random_population = [[np.random.randint(1,9) for i in range(Gene + 4)] for j in range(N - 1)]
    random_population.append([8, 1, 5, 3, 3, 7, 3, 8, 8, 4, 1, 6, 2, 1])
    initial_population = convertPopulation(random_population)
    return initial_population


populations = generateRandomPopulation(5 ,10)
print('initial population')
print(populations)

for _ in range(20): # Number of Generations to be Iterated.
    print("genetic algorithm simulation")
    selected_parents = [[13, 3, 8, 7, 67, 4, 1, 5, 4, 248], [81, 5, 3, 3, 73, 8, 8, 4, 1, 621]]
    print("selected parents " + str(selected_parents))
    next_population = crossover_mutation(selected_parents=selected_parents)