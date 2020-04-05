import numpy as np

def generateRandomPopulation(N=5,Gene=10):
    print("random population")
    random_population = [[np.random.randint(1,9) for i in range(Gene + 4)] for j in range(N)]
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
    print("shrink")
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
    print("expand")
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


population = generateRandomPopulation()
print(population)
print(expandChromosome([77, 6, 1, 5, 12, 4, 7, 7, 2, 481]))
print(shrinkChromosome([7, 7, 6, 1, 5, 1, 2, 4, 7, 7, 2, 4, 8, 1]))