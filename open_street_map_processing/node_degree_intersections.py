import pickle
import math
from geopy import distance
filename = 'passau'
path = "../resources/osm/"

filename = 'munich4'
path = r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_6\\'


map_degree_serialize = path + filename + '.ways.degree.serialize'
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'

map_lanes_serialize = path + filename + '.lanes'
map_width_serialize = path + filename + '.width'

map_three_ways_coordinates_serialize = path + filename + '.three.intersection.coorindates.serialize'
map_four_ways_coordinates_serialize  = path + filename + '.four.intersection.coorindates.serialize'

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

graph_degree = pickle.load(open(map_degree_serialize, "rb"))
print("Graph Degree")

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Node Dict") # tuples of lat and long

lane_dict = pickle.load(open(map_lanes_serialize, "rb"))
print("Lanes Loaded")

width_dict = pickle.load(open(map_width_serialize, "rb"))
print("Width Loaded") # tuples of lat and long


three_way_coordinates = []
four_way_coordinates = []

three_way_list = []
four_way_list = []

# 3 Way intersection
for tup in graph_degree:
    three_way_coordinate = []
    three_way = []
    if tup[1] == 3:
        three_way_coordinate.append(node_dict[tup[0]])
        three_way_points = graph.neighbors(tup[0])
        way_geo = (tup[0], node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]])
        print(way_geo)
        for node in three_way_points:
            way_geo = (node, node_dict[tup[0]], lane_dict[tup[0]], width_dict[tup[0]]) # node, coordinate, number of lanes , width
            print(way_geo)
            pair=(tup[0],node)  # nodes connected to center or intersection point
            three_way.append(pair)
            three_way_coordinate.append(node_dict[node]) # list of lat and long for map plot


    if three_way_coordinate:
        three_way_coordinates.append(three_way_coordinate) # list of lat and long for map plot (3 way)
        #print(three_way_coordinates)

    if three_way:
        three_way_list.append(three_way) # It is required for angle calculations and further reference required to query in graph
        #print(three_way_list)

pickle.dump(three_way_coordinates, open(map_three_ways_coordinates_serialize, "wb"))

# 4 Way intersection
for tup in graph_degree:
    four_way_coordinate = []
    four_way = []
    if tup[1] == 4:
        print(tup[0],tup[1])
        four_way_coordinate.append(node_dict[tup[0]])
        four_way_points = graph.neighbors(tup[0])
        for node in four_way_points:
            pair = (tup[0], node)
            four_way.append(pair)
            four_way_coordinate.append(node_dict[node])   # list of lat and long for map plot
            print(distance.distance(node_dict[tup[0]], node_dict[node]).km * 1000)

    if four_way_coordinate:
        four_way_coordinates.append(four_way_coordinate) # list of lat and long for map plot (4 way)
        print(four_way_coordinates)

    if four_way:
        four_way_list.append(four_way)    # It is required for angle calculations and further reference required to query in graph

pickle.dump(four_way_coordinates, open(map_four_ways_coordinates_serialize, "wb"))


# function to get angle between 3 coordinates , b should be common point between 2 lines
def getAngle(a, b, c):
    # anti clockwise angle is returned from the reference line
    # a = a[::-1]
    # b = b[::-1]
    # c = c[::-1]
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang + 360 if ang < 0 else ang


# 3 Way intersection Angle
# c , ref, p1,p2
for tup in graph_degree:
    if tup[1] == 3:
        referencePoint3 = None
        center = node_dict[tup[0]]
        three_way_points = graph.neighbors(tup[0])
        for (index, node) in enumerate(three_way_points):
            if index is 0:
               referencePoint3 = node_dict[node]
               continue

            angle = getAngle(referencePoint3,center,node_dict[node])
            angleTuple = (center, referencePoint3, node_dict[node], angle)
            #print(angleTuple)


# 4 Way intersection Angle
# c , ref, p1,p2,p3
for tup in graph_degree:
    if tup[1] == 4:
        referencePoint4 = None
        center = node_dict[tup[0]]
        four_way_points = graph.neighbors(tup[0])
        for (index, node) in enumerate(four_way_points):
            if index is 0:
               referencePoint4 = node_dict[node]
               continue

            angle = getAngle(referencePoint4,center,node_dict[node])
            angleTuple = (center, referencePoint4, node_dict[node], angle)
            #print(angleTuple)


# Distance Assumption
# It is assumed that road orientation does not change in the distance of 100m or 150m from the center point/intersection point.


# Extract road geometry from lanes and width dictionary.

