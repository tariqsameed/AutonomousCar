import math
import pickle
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging

filename = 'passau'
path = "../resources/osm/"
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'
map_beamng_serialize = path + filename + '.nodes.serialize.beamng'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

beamng_dict = pickle.load(open(map_beamng_serialize, "rb"))
print("BeamNG Nodes Loaded")


def getRoadEndLaneMarking(point1,point2, width):
    print("Road Lanes")
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



def createBeamNGLanes():

    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
    scenario = Scenario('GridMap', 'road_test')

    graph_edges = graph.edges

    for sample in graph_edges:
        road_a = Road('track_editor_C_border', looped=False)
        road_b= Road('track_editor_C_border', looped=False)

        point1 = list(beamng_dict[sample[0]])
        point2 = list(beamng_dict[sample[1]])


        lane_marking_points = getRoadEndLaneMarking(point1,point2,4)

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



    scenario.make(beamng)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()

        input('Press enter when done...')

    finally:
        bng.close()



createBeamNGLanes()
#getRoadEndLaneMarking((5,1),(5,9),4)