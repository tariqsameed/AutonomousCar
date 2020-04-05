import re
import random
import numpy as np


pf = {}
a = [[1,2],[2,3],[3,4]]

for n in a:
    pf[tuple(n)] = 1

t = [1,2]
print(pf)
print (pf[tuple(t)])



# summary = "The film Pulp Fiction was released in year 1994"
# word_to_replace = r"Pulp Fiction"
# summary = re.sub(word_to_replace, "V1", summary)
# word_to_replace = r"Pulp Fiction2"
# summary = re.sub(word_to_replace, "V2", summary)
#
#
# result = re.sub('[^0-9a-zA-Z]+', '', 'h^&ell`.,|o w]{+orld')
# print(result)
#
#
# def mutation(chromosome):
#     print("mutation")
#     chromosome[random.randint(0, len(chromosome) - 1)] = random.randint(min(chromosome), max(chromosome) - 1)
#     return  chromosome
#
#
# def crossover(chromosome1,chromosome2):
#     print("crossover")
#     crossover_point = random.randint(1, len(chromosome1) - 1)
#
#     # Create children. np.hstack joins two arrays
#     child_1 = np.hstack((chromosome1[0:crossover_point],
#                          chromosome2[crossover_point:]))
#
#     child_2 = np.hstack((chromosome2[0:crossover_point],
#                          chromosome1[crossover_point:]))
#
#
#
#     # Return children
#     return child_1, child_2
#
#
# def crossover_mutation(selected_parents):
#     print("crossover mutation")
#     # https://stackoverflow.com/questions/20161980/difference-between-exploration-and-exploitation-in-genetic-algorithm?rq=1
#     population_next = []
#     n = 2
#     for i in range(int(len(selected_parents) / 2)):
#         for j in range(n): # number of children
#             chromosome1, chromosome2 = selected_parents[i], selected_parents[len(selected_parents) - 1 - i]
#             childs = crossover(chromosome1,chromosome2)
#             for child in childs:
#                 population_next.append(mutation(child.tolist()))
#
#     print(population_next)
#     return population_next
#
#
# crossover_mutation(selected_parents=[[4,8,7,5,6,5,5,6,0,8,4,1,8,0],[1,3,5,8,6,5,9,6,0,6,4,1,2,0]])