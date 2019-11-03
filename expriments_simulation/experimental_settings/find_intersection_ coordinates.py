import pickle

filename = 'passau3'
path = r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_2\\'

map_degree_serialize = path + filename + '.ways.degree.serialize'

graph_degree = pickle.load(open(map_degree_serialize, "rb"))
print("Graph Degree")

for tup in graph_degree:
    three_way_coordinate = []
    three_way = []
    if tup[1] == 3:
        print(tup)

    if tup[1] == 4:
        print(tup)