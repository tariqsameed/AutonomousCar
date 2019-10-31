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



def RotationExtraction():
    print("rotation extraction")
    