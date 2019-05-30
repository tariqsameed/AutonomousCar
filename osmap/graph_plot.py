import mplleaflet
import matplotlib.pyplot as plt

lats = [48.5706833,48.5705899, 48.5705161]
lons= [13.4587882,13.4588999, 13.4585069]

fig = plt.figure()    #This is missing in your code.
plt.plot(lons, lats, 'rs')

#And after this call the funtion:
mplleaflet.show(fig=fig)


from geopy import distance
point1 = (48.5706833, 13.4587882)
point2 = (48.5705899, 13.4588999)
print(distance.distance(point1, point2).km *1000)

# https://forum.openstreetmap.org/viewtopic.php?id=22752
# https://janakiev.com/blog/openstreetmap-with-python-and-overpass-api/

