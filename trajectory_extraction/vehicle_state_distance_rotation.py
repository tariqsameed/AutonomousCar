import math




def DistanceExtraction(striker_speed, striker_after_position, striker_collision_position, victim_speed, victim_after_position, victim_collision_position):
    print("Distance Extraction")

    distance_stiker = math.hypot(striker_collision_position[0] - striker_after_position[0], striker_collision_position[1] - striker_after_position[1])
    distance_victim = math.hypot(victim_collision_position[0] - victim_after_position[0], victim_collision_position[1] - victim_after_position[1])

    print(distance_stiker)
    print(distance_victim)

    # the fitness fucntion of distance eztraction is limited to the speed of 20 ms
    # range of speed for calculation.

    striker_distance_score = 0
    victim_distance_score = 0

    #---------------------------------------------------------------------------------------
    # striker distance for 25 ms
    if striker_speed > 22 and striker_speed < 28 and distance_stiker >= 11 and distance_stiker < 17:
        striker_distance_score = 0.7

    if striker_speed > 22 and striker_speed < 28 and distance_stiker >= 7 and distance_stiker < 11:
        striker_distance_score = 0.5

    if striker_speed > 22 and striker_speed < 28 and distance_stiker > 0 and distance_stiker < 7:
        striker_distance_score = 0.3


    # victim_distance for 25 ms
    if victim_speed > 22 and victim_speed < 28 and distance_victim >= 11 and distance_victim < 17:
        striker_distance_score = 0.7

    if victim_speed > 22 and victim_speed < 28 and distance_victim >= 7 and distance_victim < 11:
        striker_distance_score = 0.5

    if victim_speed > 22 and victim_speed < 28 and distance_victim > 0 and distance_victim < 7:
        striker_distance_score = 0.3
    # ---------------------------------------------------------------------------------------

    # striker distance for 20 ms
    if striker_speed > 17 and striker_speed <= 22 and distance_stiker >= 9 and distance_stiker < 14:
        striker_distance_score = 0.7

    if striker_speed > 17 and striker_speed <= 22 and distance_stiker >= 5 and distance_stiker < 9:
        striker_distance_score = 0.5

    if striker_speed > 17 and striker_speed <= 22 and distance_stiker > 0 and distance_stiker < 5:
        striker_distance_score = 0.3


    # victim_distance for 20 ms
    if victim_speed > 17 and victim_speed <= 22 and distance_victim >= 9 and distance_victim < 14:
        striker_distance_score = 0.7

    if victim_speed > 17 and victim_speed <= 22 and distance_victim >= 5 and distance_victim < 9:
        striker_distance_score = 0.5

    if victim_speed > 17 and victim_speed <= 22 and distance_victim > 0 and distance_victim < 5:
        striker_distance_score = 0.3


    # ---------------------------------------------------------------------------------------

    # striker distance for 15 ms
    if striker_speed > 11 and striker_speed <= 17 and distance_stiker >= 7 and distance_stiker < 11:
        striker_distance_score = 0.7

    if striker_speed > 11 and striker_speed <= 17 and distance_stiker >= 4 and distance_stiker < 7:
        striker_distance_score = 0.5

    if striker_speed > 11 and striker_speed <= 17 and distance_stiker > 0 and distance_stiker < 4:
        striker_distance_score = 0.3

    # victim_distance for 20 ms
    if victim_speed > 11 and victim_speed <= 17 and distance_victim >= 7 and distance_victim < 11:
        striker_distance_score = 0.7

    if victim_speed > 11 and victim_speed <= 17 and distance_victim >= 4 and distance_victim < 7:
        striker_distance_score = 0.5

    if victim_speed > 11 and victim_speed <= 17 and distance_victim > 0 and distance_victim < 4:
        striker_distance_score = 0.3

    # --------------------------------------------------------------------------------------------

    # striker distance for 15 ms
    if striker_speed >= 0 and striker_speed <= 11 and distance_stiker < 4:
        striker_distance_score = 0.7


    # victim_distance for 20 ms
    if victim_speed >= 0 and victim_speed <= 11 and distance_victim < 4 :
        striker_distance_score = 0.7

    # --------------------------------------------------------------------------------------------

    return striker_distance_score, victim_distance_score



from math import atan2,degrees

def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return degrees(atan2(changeInY,changeInX)) #remove degrees if you want your answer in radians

#alpha = AngleBtw2Points([5,5],[7,4])
#print(alpha)

# angle between 3 points
import math
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang




def RotationExtraction(striker_precrash_position, striker_collision_point, striker_post_crash_position, victim_precrash_position, victim_collision_point, victim_post_crash_position):
    print("rotation extraction")

    striker_alpha = getAngle(striker_precrash_position, striker_collision_point, striker_post_crash_position)
    victim_alpha = getAngle(victim_precrash_position, victim_collision_point, victim_post_crash_position)

    striker_heading = AngleBtw2Points(striker_precrash_position, striker_collision_point)
    victim_heading = AngleBtw2Points(victim_precrash_position, victim_collision_point)

    # print(striker_heading)
    # print(victim_heading)
    #
    # print(striker_alpha)
    # print(victim_alpha)
    #
    # print("Angle after collision")
    # print((striker_heading + striker_alpha) % 360)
    # print((victim_heading + victim_alpha) % 360)

    striker_deviation = (striker_heading + striker_alpha) % 360
    victim_deviation = (victim_heading + victim_alpha) % 360

    striker_deviaiton_score = 0
    victim_deviation_score = 0

    if striker_deviation > 0 and  striker_deviation <= 30:
        striker_deviaiton_score = 0.8

    if striker_deviation > 30 and  striker_deviation <= 45:
        striker_deviaiton_score = 0.5

    if striker_deviation > 45:
        striker_deviaiton_score = 0.3


    #---------------------------------------------------------

    if victim_deviation > 0 and victim_deviation <= 30:
        victim_deviaiton_score = 0.8

    if victim_deviation > 30 and victim_deviation <= 45:
        victim_deviaiton_score = 0.5

    if victim_deviation > 45:
        victim_deviaiton_score = 0.3


    print(striker_deviaiton_score)
    print(victim_deviaiton_score)

    return  striker_deviaiton_score,victim_deviation_score