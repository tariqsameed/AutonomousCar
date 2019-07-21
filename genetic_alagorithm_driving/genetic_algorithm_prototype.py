import random
import numpy.random as npr

# Inputs of the equation.
equation_inputs = [30,-50,3,50,4,45] # speedx, x1, x2 , speedy, y1, y2

# Defining the population size
sol_per_pop = 100

# Generate initial population randomly
speed_striker = []
pos_one_striker = []
pos_two_striker = []
speed_victim = []
pos_one_victim = []
pos_two_victim = []

for i in range(0,sol_per_pop):
    speed_striker.append(random.randint(0,100))

for i in range(0, sol_per_pop):
    pos_one_striker.append(random.randint(-200, 10))

for i in range(0, sol_per_pop):
    pos_two_striker.append(random.randint(-4, 4))

for i in range(0, sol_per_pop):
    speed_victim.append(random.randint(0, 100))

for i in range(0, sol_per_pop):
    pos_one_victim.append(random.randint(-4, 4))

for i in range(0, sol_per_pop):
    pos_two_victim.append(random.randint(-10, 200))

#Creating the initial population
populations = list(zip(speed_striker, pos_one_striker,pos_two_striker,speed_victim,pos_one_victim,pos_two_victim))
#print(populations)

# evaluate current population
fitness_value = 75 #(100/8 = 12.5) - Max 2 errors
populations_fitness = {}
# fitness function
def simulation_fitness_calculation(striker_impact, striker_rotation, striker_distance, striker_facing, victim_impact, victim_rotation, victim_distance, victim_facing ):
    print('fitness function')
# each correct attribute has score 12.5, Correct attribute value is 1 and False is 0
    score_per_attribute = 12.5
    striker_fitness_simulation = (score_per_attribute * striker_impact) + (score_per_attribute * striker_rotation) + (score_per_attribute * striker_distance) + (score_per_attribute * striker_facing)
    victim_fitness_simulation = (score_per_attribute * victim_impact)  + (score_per_attribute * victim_rotation) + (score_per_attribute * victim_distance) + (score_per_attribute * victim_facing)
    fitness_simulation_value = striker_fitness_simulation + victim_fitness_simulation
    return  fitness_simulation_value


def roullete_wheel_selection(populations):
    print('Roullete Wheel Selection')
    max = sum([populations_fitness[sample] for sample in populations])
    selection_probs = [populations_fitness[sample] / max for sample in populations]
    print(selection_probs)
    selection = populations[npr.choice(len(populations), p=selection_probs)]
    # Selection to return list of population.
    # Make sure to transfer elitism to next generation.
    # https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
    # https://medium.com/datadriveninvestor/genetic-algorithms-selection-5634cfc45d78
    return selection


# Use many tournaments to get parents
def tournament_parent_selection(populations, n=2, tsize=5):
    print('tournament selection')
    selected_candidates = []
    for i in range(n):
        fittest_population_in_tournament = None
        candidates = random.sample(populations, tsize)
        print(candidates)
        current = None
        for can in candidates:
            if fittest_population_in_tournament is None:
                fittest_population_in_tournament = populations_fitness[can]
                current = can

            if populations_fitness[can] > fittest_population_in_tournament:
                current = can

        selected_candidates.append(current)

    print(selected_candidates)
    #https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35


def crossover_and_mutation(selected_candidates):
#   https://stackoverflow.com/questions/37021934/how-to-crossover-the-parents-when-using-a-value-encoding-method-in-genetic-algor
#   https://towardsdatascience.com/evolution-of-a-salesman-a-complete-genetic-algorithm-tutorial-for-python-6fe5d2b3ca35
    print('crossover and mutation')
    print('Evaluation of Children')
    print('survival and replacement')







def crash_evaluation(population):
    print('crash evaluation')
    population_key = population
    #our current fitness function is based on the crash impact for now
    striker_impact, striker_rotation, striker_distance, striker_facing, victim_impact, victim_rotation, victim_distance, victim_facing = [0,0,0,0,0,0,0,0]
    population = list(population)
    print(population)
    striker = population[:len(population) // 2]
    victim = population[len(population) // 2:]
    # Assuming distance is same from point of impact for now
    # t = d/s the range from 0.6 to 0.9

    try:
        striker_time = abs(striker[1] - 0) / float(striker[0])
    except ZeroDivisionError:
        striker_time = 0

    try:
        victim_time = abs(victim[2] - 0) / float(victim[0])
    except ZeroDivisionError:
        victim_time = 0

    difference = abs(striker_time - victim_time)
#    print(difference)
    if int(difference) in range(0,1):
        print('difference')
        striker_impact = 1
        victim_impact = 1

    fitness_simulation_value = simulation_fitness_calculation(striker_impact, striker_rotation, striker_distance, striker_facing,victim_impact, victim_rotation, victim_distance, victim_facing)
#    print(fitness_simulation_value)
    populations_fitness[population_key] = fitness_simulation_value


for sample in populations:
    crash_evaluation(sample)
#selection = roullete_wheel_selection(populations)
#print(selection)

tournament_parent_selection(populations)

