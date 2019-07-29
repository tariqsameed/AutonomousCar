# Intersection of polylines
# Maximum distance from centriod to perpendicular line of the road.
# Genereate new lane marking based on updated coordinates of polyline
from __future__ import division
import math
import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import networkx as nx
import itertools

filename = 'passau'
path = "../resources/osm/"
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'
map_beamng_serialize = path + filename + '.nodes.serialize.beamng'
map_degree_serialize = path + filename + '.ways.degree.serialize'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
print("BeamNG Nodes Loaded")

graph_degree = pickle.load(open(map_degree_serialize, "rb"))
print("Graph Degree")

beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
scenario = Scenario('GridMap', 'road_test')

def getRoadEndLaneMarking(point1,point2, width):
#https://stackoverflow.com/questions/47040213/find-perpendicular-line-using-points-on-that-line

    dx = float(point2[0] - point1[0])
    dy = float(point2[1] - point1[1])

    L = float(math.sqrt(float(float(dx * dx) + float(dy * dy))))
    U = (float(-dy / L), float(dx / L))
    F = float(float(width/2) - 0.05)

# Point on one side
    x1p = float(point1[0] + U[0] * F)
    y1p = float(point1[1] + U[1] * F)

# Point on other side
    x1n = float(point1[0] - U[0] * F)
    y1n = float(point1[1] - U[1] * F)

# Point on one side
    x2p = float(point2[0] + U[0] * F)
    y2p = float(point2[1] + U[1] * F)

# Point on other side
    x2n = float(point2[0] - U[0] * F)
    y2n = float(point2[1] - U[1] * F)

    #print(x1p,y1p,x1n,y1n,x2p,y2p,x2n,y2n)

    return x1p,y1p,x1n,y1n,x2p,y2p,x2n,y2n


def calculateDistance(x1, y1, x2, y2):
    dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist



def IntersectionLaneMarking():

    print("Intersection Lane Marking")
    for tup in graph_degree:
        center = ''
        if tup[1] == 3:
            print(list(nx.dfs_edges(graph, source=tup[0], depth_limit=1)))
            way_3 = list(nx.dfs_edges(graph, source=tup[0], depth_limit=1))

            for sample in way_3:
                road_a = Road('track_editor_C_border', looped=False)
                road_b = Road('track_editor_C_border', looped=False)

                center = list(beamng_dict[sample[0]])
                point1 = list(beamng_dict[sample[1]])
                print(center)
                print(point1)
                # https://stackoverflow.com/questions/1250419/finding-points-on-a-line-with-a-given-distance
                road_width = 8/2 - 1
                real_distance = calculateDistance(center[0],center[1], point1[0], point1[1])

                t = road_width / real_distance

                point2 = (((1 - t) * center[0] + t * point1[0]), ((1 - t) * center[1] + t * point1[1]))
                print("new point")
                print(point2)

                # create new polylines and plot.
                lane_marking_points = getRoadEndLaneMarking(point1, point2, 4)

                nodes0 = [
                    (lane_marking_points[0], lane_marking_points[1], -0.05, 0.05),
                    (lane_marking_points[4], lane_marking_points[5], -0.05, 0.05)
                ]

                nodes1 = [
                    (lane_marking_points[2], lane_marking_points[3], -0.05, 0.05),
                    (lane_marking_points[6], lane_marking_points[7], -0.05, 0.05)
                ]

                road_a.nodes.extend(nodes0)
                road_b.nodes.extend(nodes1)
                scenario.add_road(road_a)
                scenario.add_road(road_b)

                road_c = Road('track_editor_C_center', looped=False)
                pointa = list(beamng_dict[sample[0]])
                pointb = list(beamng_dict[sample[1]])

                nodes0 = [
                    (pointa[0], pointa[1], -4, 4),
                    (pointb[0], pointb[1], -4, 4)
                ]

                road_c.nodes.extend(nodes0)
                #scenario.add_road(road_c)


    scenario.make(beamng)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()

        input('Press enter when done...')

    finally:
        bng.close()




def createBeamNGRoads():

    print(graph.edges)

    graph_edges = graph.edges
    print(len(graph_edges))

    sample_list = []
    for sample in graph_edges:
        road_a = Road('track_editor_C_center', looped=False)
        point1 = list(beamng_dict[sample[0]])
        point2 = list(beamng_dict[sample[1]])

        nodes0 = [
            (point1[0], point1[1], -4, 4),
            (point2[0], point2[1], -4, 4)
        ]

        road_a.nodes.extend(nodes0)
        scenario.add_road(road_a)

        sample_list.append(point1)
        sample_list.append(point2)






#createBeamNGRoads()
IntersectionLaneMarking()