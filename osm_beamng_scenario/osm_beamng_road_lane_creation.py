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

def getRoadPolyLineLaneMarking(point1,point2, width):
#https://stackoverflow.com/questions/47040213/find-perpendicular-line-using-points-on-that-line

    #print(point1,point2, width)
    lane_adjustment = 0

    if width < 0:
        lane_adjustment = -0.2
    elif width > 0:
        lane_adjustment = 0.2


    dx = float(point2[0] - point1[0])
    dy = float(point2[1] - point1[1])

    L = float(math.sqrt(float(float(dx * dx) + float(dy * dy))))
    U = (float(-dy / L), float(dx / L))
    F = float(float(width / 2) - lane_adjustment)

# Point on one side
    x1p = float(point1[0] + U[0] * F)
    y1p = float(point1[1] + U[1] * F)


# Point on one side
    x2p = float(point2[0] + U[0] * F)
    y2p = float(point2[1] + U[1] * F)

    #print(x1p,y1p,x1n,y1n,x2p,y2p,x2n,y2n)

    return x1p,y1p,x2p,y2p



def getLanesAndWidth(width, lanes):
    #print("Lanes and Width")
# https://stackoverflow.com/questions/9926446/how-to-check-whether-a-strvariable-is-empty-or-not

    total_lanes = lanes
    total_width = width

    if width and lanes:
        #print("Width and Lanes")
        # used lane width data to compute each lane width
        total_lanes = lanes
        total_width = width


    if width and not lanes:
        #print("width only")
        # lanes based on the formula.
        number_of_lanes = float(width / 3.7)
        total_lanes = round(number_of_lanes)
        total_width = width


    if lanes and not width:
        #print("lanes only")
        # standard lane width 4
        total_lanes = lanes
        total_width = lanes * 4

    if not lanes and not width:
        total_lanes = 2
        total_width = 2 * 4

    return total_lanes, total_width


def getRoadLaneMarking(point1,point2, width, lanes):
    #print("Road Lane marking")
    lanesAndWidth = getLanesAndWidth(width,lanes)
    center = float(width/2)
    laneWidth = float(lanesAndWidth[1] / lanesAndWidth[0])
    lane_marking_all = []

    # calculate lane marking coordinates
    for i in range(lanesAndWidth[0] - 1):
        laneNumber = i + 1
        position_of_lane = laneNumber * laneWidth

        width = float(center - position_of_lane)
        # calculate polyline
        lane_marking = getRoadPolyLineLaneMarking(point1,point2, width)
        lane_marking_all.append(lane_marking)


    return lane_marking_all

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


def createBeamNGRoads():

    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
    scenario = Scenario('GridMap', 'road_test')

    print(graph.edges)

    graph_edges = graph.edges
    print(len(graph_edges))

    sample_list = []
    for sample in graph_edges:
        # road creation
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

        # road edge lane marking

        road_b = Road('track_editor_C_border', render_priority=10, looped=False)
        road_c = Road('track_editor_C_border', render_priority=10, looped=False)


        point1 = list(beamng_dict[sample[0]])
        point2 = list(beamng_dict[sample[1]])

        lane_marking_points = getRoadEndLaneMarking(point1, point2, 4)

        nodes0 = [
            (lane_marking_points[0], lane_marking_points[1], -0.05, 0.05),
            (lane_marking_points[4], lane_marking_points[5], -0.05, 0.05)
        ]

        nodes1 = [
            (lane_marking_points[2], lane_marking_points[3], -0.05, 0.05),
            (lane_marking_points[6], lane_marking_points[7], -0.05, 0.05)
        ]

        road_b.nodes.extend(nodes0)
        road_c.nodes.extend(nodes1)
        scenario.add_road(road_b)
        scenario.add_road(road_c)

        # road lane marking

        lane_marking_points = getRoadLaneMarking(point1, point2, 10, 3)

        # for loop iterate to put polylines.

        for polyline in lane_marking_points:
            #print(polyline)
            road_d = Road('track_editor_C_border', render_priority=10, looped=False)

            nodes0 = [
                (polyline[0], polyline[1], -0.05, 0.05),
                (polyline[2], polyline[3], -0.05, 0.05)
            ]

            road_d.nodes.extend(nodes0)
            scenario.add_road(road_d)


    scenario.make(beamng)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()

        input('Press enter when done...')

    finally:
        bng.close()



createBeamNGRoads()