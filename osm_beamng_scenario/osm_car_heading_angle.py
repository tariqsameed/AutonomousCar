from math import atan2,degrees, cos, sin



def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return degrees(atan2(changeInY,changeInX)) #remove degrees if you want your answer in radians

alpha = AngleBtw2Points([5,5],[7,4])
print(alpha)


alpha = AngleBtw2Points((308.46771202670277, 39.318581604695254), (271.3365218368745, 48.091873711762084))
print(alpha)


alpha = AngleBtw2Points((308.46771202670277, 39.318581604695254) , (271.3365218368745, 48.091873711762084))
print(alpha)

# Kansas City: 39.099912, -94.581213
# St Louis: 38.627089, -90.200203


road_striker = [(303.3618974852293, 19.92615900347052),(308.46771202670277, 39.318581604695254)]
road_victim =  [(271.3365218368745, 48.091873711762084),(308.46771202670277, 39.318581604695254)]


# Striker angle
X =  cos(271.3365218368745) * sin(0)
Y =  cos(303.3618974852293) * sin(271.3365218368745) - sin(303.3618974852293) * cos(271.3365218368745) * cos(0)

beta = degrees(atan2(X,Y))
print(beta)






# victim angle
X =  cos(271.3365218368745) * sin(0)
Y =  cos(303.3618974852293) * sin(271.3365218368745) - sin(303.3618974852293) * cos(271.3365218368745) * cos(0)

beta = degrees(atan2(X,Y))
print(beta)



road_striker = [(303.3618974852293, 19.92615900347052),(308.46771202670277, 39.318581604695254)]
road_victim =  [(271.3365218368745, 48.091873711762084),(308.46771202670277, 39.318581604695254)]


# striker
from math import atan2, degrees, pi
dx = 308.46771202670277 - 303.3618974852293
dy = 39.318581604695254 - 19.92615900347052
rads = atan2(-dy,dx)
rads %= 2*pi
degs = degrees(rads)

print(degs)


# victim
dx = 308.46771202670277 - 271.3365218368745
dy = 39.318581604695254 - 48.091873711762084
rads = atan2(-dy,dx)
rads %= 2*pi
degs = degrees(rads)

print(degs)