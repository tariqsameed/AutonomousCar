import math
from geopy.distance import great_circle

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





a,b = getCartesianCooridinatoin(48.571847, 13.4607844)
getNormalizedOSMCoordinates(-516275.24456013856, -4181695.6509210765,a,b )