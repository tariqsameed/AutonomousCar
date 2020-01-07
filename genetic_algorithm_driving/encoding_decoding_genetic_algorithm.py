import random
import numpy as np
import math

V1_SPEED_INDEX_1 = 0
V1_SPEED_INDEX_2 = 1
V1_DISTANCE_INDEX_1 = 2
V1_DISTANCE_INDEX_2 = 3
V1_WIDTH_INDEX = 4
V2_SPEED_INDEX_1 = 5
V2_SPEED_INDEX_2 = 6
V2_DISTANCE_INDEX_1 = 7
V2_DISTANCE_INDEX_2 = 8
V2_WIDTH_INDEX = 9
POINT_OF_IMPACT_RADIUS = 10
POINT_OF_IMPACT_ANGLE_1 = 11
POINT_OF_IMPACT_ANGLE_2 = 12
POINT_OF_IMPACT_ANGLE_3 = 13
IMPACT_POSITION_X = 1
IMPACT_POSITION_Y = 2
V1_ROAD_ID = 123456
V2_ROAD_ID = 654321

def getPolyLineCoordinates(node_a,node_b, distance,width):
    print("get polyline coordinate")
    # Assumption. width from the center of the road.
    real_distance = getDistance(node_a,node_b)
    t = distance / real_distance

    point2 = (((1 - t) * node_a[0] + t * node_b[0]), ((1 - t) * node_a[1] + t * node_b[1]))

    print(node_a, point2, width)

    dx = float(point2[0] - node_a[0])
    dy = float(point2[1] - node_a[1])

    L = float(math.sqrt(float(float(dx * dx) + float(dy * dy))))
    U = (float(-dy / L), float(dx / L))
    F = float(float(width))

    # Point on one side
    x2p = float(point2[0] - U[0] * F)
    y2p = float(point2[1] - U[1] * F)

    return x2p,y2p


def getDistance(node_a,node_b):
    print("get distance")
    dist = math.sqrt((node_a[1] - node_b[1]) ** 2 + (node_a[0] - node_b[0]) ** 2)
    return dist



def getV1BeamNGCoordinaes(total_distance_v1, width):
    print("beamng v1 coordinates")
    v1_roads = [(1,2),(3,4),(5,6),(7,8)]
    v1_roads_distance = 120
    v1_road_max = total_distance_v1 * v1_roads_distance

    beamng_pos = ""
    for node in v1_roads:
        node_distance = getDistance(node[0],node[1])
        v1_poly_distance = v1_road_max
        v1_road_max = v1_road_max - node_distance

        if v1_road_max < 0:
           beamng_pos =   getPolyLineCoordinates(node[0],node[1],v1_poly_distance,width)
           break

    return beamng_pos




def getV2BeamNGCoordinaes(total_distance_v2, width):
    print("beamng v2 coordinates")
    print("beamng v1 coordinates")
    v1_roads = [(1, 2), (3, 4), (5, 6), (7, 8)]
    v2_roads_distance = 90
    v1_road_max = total_distance_v2 * v2_roads_distance

    v1_poly_distance = ""
    beamng_pos = ""
    for node in v1_roads:
        node_distance = getDistance(node[0], node[1])
        v1_poly_distance = v1_road_max
        v1_road_max = v1_road_max - node_distance

        if v1_road_max < 0:
            beamng_pos = getPolyLineCoordinates(node[0], node[1], v1_poly_distance, width)
            break

    return beamng_pos



def encoding_of_parameter(v1_speed, v1_pos, v2_speed, v2_pos, impact_pos):
    print("encoding of parameters")



def decoding_of_parameter(chromosome):
    print("decoding of parameters")

    # rotation of the car in beamng scenario

    # Speed
    v1_speed = int(str(chromosome[V1_SPEED_INDEX_1]) + str(chromosome[V1_SPEED_INDEX_2]))
    v2_speed = int(str(chromosome[V2_SPEED_INDEX_1]) + str(chromosome[V2_SPEED_INDEX_2]))

    # point of impact
    radius = chromosome[POINT_OF_IMPACT_RADIUS] % 4
    angle_str = str(chromosome[POINT_OF_IMPACT_ANGLE_1]) + str(chromosome[POINT_OF_IMPACT_ANGLE_2]) + str(chromosome[POINT_OF_IMPACT_ANGLE_3])
    angle = int(angle_str) % 360

    # point of impact (collision point  provided by user)
    # https://stackoverflow.com/questions/2912779/how-to-calculate-a-point-with-an-given-center-angle-and-radius

    point_of_impact_x = IMPACT_POSITION_X + radius * math.cos(math.radians(angle)) # radians
    point_of_impact_y = IMPACT_POSITION_Y + radius * math.sin(math.radians(angle))  # radians
    impact_point = (point_of_impact_x,point_of_impact_y)


    # position length
    total_distance_v1 = float(int(str(chromosome[V1_DISTANCE_INDEX_1]) + str(chromosome[V1_DISTANCE_INDEX_2])) / 50)
    v1_pos_bg = getV1BeamNGCoordinaes(total_distance_v1,  chromosome[V1_WIDTH_INDEX])  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint

    total_distance_v2 = float(int(str(chromosome[V2_DISTANCE_INDEX_1]) + str(chromosome[V2_DISTANCE_INDEX_2])) / 50)
    v2_pos_bg = getV2BeamNGCoordinaes(total_distance_v2, chromosome[V2_WIDTH_INDEX])  # get beamng coordinates (polyline coordinate). it will be always calculated from center - joint

    return v1_speed, v1_pos_bg, v2_speed, v2_pos_bg, impact_point




def generateRandomPopulation(N=10,Gene=14):
    print("random population")
    print([[np.random.randint(0,9) for i in range(Gene)] for j in range(N)])
    initial_population = [[np.random.randint(0,9) for i in range(Gene)] for j in range(N)]
    return initial_population


generateRandomPopulation(10)
print(math.sin(math.radians(45)))