import math
from geopy.distance import great_circle
import pickle
import networkx as nx
import matplotlib.pyplot as plt
import sys

filename = 'passau'
path = "../resources/osm/"
map_ways_serialize = path + filename + '.ways.serialize'
map_nodes_serialize = path + filename + '.nodes.serialize'
map_beamng_serialize = path + filename + '.nodes.serialize.beamng'

node_dict = pickle.load(open(map_nodes_serialize, "rb"))
print("Nodes Loaded")

graph = pickle.load(open(map_ways_serialize, "rb"))
print("Graph Loaded")

# create dictionary of beamng nodes.
# plot on mat plot
# iterate dfs to plot the graph with lines.



# convert long, lat to cartesian coordination
def getCartesianCooridinatoin(lon, lat):
    R = 6731000
    x = R * math.cos(lat) * math.cos(lon)
    y = R * math.cos(lat) * math.sin(lon)
    print(x,y)
    return x,y

#get Distance between lon,lat.
def getDistanceBetweenTwoNodes(startingPointX,startingPointY, destinationPointX, destinationPointY):
    startingNode = (startingPointX, startingPointY)
    endingNode = (destinationPointX, destinationPointY)
    distance = great_circle(startingNode, endingNode).m
    return distance

# get coordinates on BeamNG in meters
def getNormalizedBeamNGCoordinates(startingPointX,startingPointY, lonCartesian, latCartesian):
    xComponent = getDistanceBetweenTwoNodes(startingPointX,startingPointY,lonCartesian,startingPointY)
    yComponent = getDistanceBetweenTwoNodes(startingPointX,startingPointY,startingPointX,latCartesian)
    return  xComponent,yComponent

# get coordinates (substracting minimum from coordinates)
def getNormalizedOSMCoordinates(startingPointX,startingPointY, lonCartesian, latCartesian):

    gridx = lonCartesian - startingPointX
    gridy = latCartesian - startingPointY
    print(gridx, gridy)
    return gridx,gridy



def findMaxLonLat(lat_lon_list):
    #print("Max")
    maxLon = max(lat_lon_list, key=lambda t: t[0])
    maxLat = max(lat_lon_list, key=lambda t: t[1])
    #print(maxLon[0], maxLat[1])
    return  maxLon[0], maxLat[1]

def findMinLonLat(lat_lon_list):
    #print("Min")
    minLon = min(lat_lon_list, key=lambda t: t[0])
    minLat = min(lat_lon_list, key=lambda t: t[1])
    #print(minLon[0],minLat[1])
    return  minLon[0],minLat[1]

def findMinMaxLonLat(graph):

    lat_lon_list = []
    for element in graph:
        lat_lon_list.append(node_dict[element])

    minLon, minLat = findMinLonLat(lat_lon_list)
    maxLon, maxLat = findMaxLonLat(lat_lon_list)
    return minLon, minLat, maxLon, maxLat


def startRoadCreation():
    try:
        beamNG_coordintes =[]
        beamNG_lat_lon = {}

        #minLon, minLat, maxLon, maxLat = findMinMaxLonLat(graph)
        minMaxLonLat = findMinMaxLonLat(graph)
        print(minMaxLonLat)

        connected_edges_chuncks = nx.dfs_edges(graph)

        for sample in connected_edges_chuncks:

            for coordinate in sample:
                element = node_dict[coordinate]
                #gridOSMx, gridOSMy = getNormalizedOSMCoordinates(minMaxLonLat[0],minMaxLonLat[1], element[0], element[1])
                gridBeamNGx,gridBeamNGy = getNormalizedBeamNGCoordinates(minMaxLonLat[0], minMaxLonLat[1], element[0], element[1])
                beamNG_lat_lon[coordinate] = {gridBeamNGx,gridBeamNGy}
                beamNG_coordintes.append((gridBeamNGx,gridBeamNGy))



        print(beamNG_coordintes)

        x_val = [x[0] for x in beamNG_coordintes]
        y_val = [x[1] for x in beamNG_coordintes]

        plt.figure()
        #plt.plot(x_val, y_val)
        plt.plot(x_val, y_val, 'or')
        #plt.show()
        plt.savefig('osm_normalized_beamng.png')

        pickle.dump(beamNG_lat_lon, open(map_beamng_serialize, "wb"), protocol=4)
        print("Done")

    except IOError:
        print("Could not read file or file does not exist: ", map)
        sys.exit()


#a,b = getCartesianCooridinatoin(48.571847, 13.4607844)
#getNormalizedOSMCoordinates(-516275.24456013856, -4181695.6509210765,a,b )
#findMinMaxLonLat(graph)
#edges_list = nx.to_edgelist(graph)

startRoadCreation()


