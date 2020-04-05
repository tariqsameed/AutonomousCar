import mplleaflet
import matplotlib.pyplot as plt
import pickle
import gmplot

filename = 'passau'
path = "../resources/osm/"

filename = 'munich4'
path = r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_6\\'

map_three_ways_coordinates_serialize = path + filename + '.three.intersection.coorindates.serialize'
map_four_ways_coordinates_serialize  = path + filename + '.four.intersection.coorindates.serialize'

three_way_coordinates = pickle.load(open(map_three_ways_coordinates_serialize, "rb"))
print("3 way coordinates Loaded")

four_way_coordinates = pickle.load(open(map_four_ways_coordinates_serialize, "rb"))
print("4 way coordinates Loaded")

three_lats =[]
three_lons = []
for intersect in three_way_coordinates:
    a, b = map(list, zip(*intersect))
    three_lats.extend(a)
    three_lons.extend(b)

print(three_lats)
print(three_lons)


four_lats =[]
four_lons = []

for intersect in four_way_coordinates:
    a, b = map(list, zip(*intersect))
    four_lats.extend(b)
    four_lons.extend(a)


print(four_lats)
print(four_lons)


fig = plt.figure()    #This is missing in your code.
plt.plot( three_lons, three_lats, 'rs')
plt.plot( four_lats, four_lons, 'bs')

mapfile = r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_6\osm'  + '.html'
#And after this call the funtion:
mplleaflet.show(path=mapfile,fig=fig)



# Google Map plot
gmap = gmplot.GoogleMapPlotter(three_way_coordinates[0][0][0], three_way_coordinates[0][0][1], 18)
gmap.scatter( three_lats, three_lons, '#FF0000', size = 2, marker = False )
# gmap = gmplot.GoogleMapPlotter(four_way_coordinates[0][0][0], four_way_coordinates[0][0][1], 18)
# gmap.scatter(four_lons, four_lats, '#FF0000', size = 2, marker = False )
gmap.draw(r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_6\google_map.html')


# from geopy import distance
# point1 = (48.5706833, 13.4587882)
# point2 = (48.5705899, 13.4588999)
# print(distance.distance(point1, point2).km *1000)

# https://forum.openstreetmap.org/viewtopic.php?id=22752
# https://janakiev.com/blog/openstreetmap-with-python-and-overpass-api/

