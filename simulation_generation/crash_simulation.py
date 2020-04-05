import time
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
from beamngpy.sensors import Damage


from math import atan2,degrees


def AngleBtw2Points(pointA, pointB):
  changeInX = pointB[0] - pointA[0]
  changeInY = pointB[1] - pointA[1]
  return degrees(atan2(changeInY,changeInX)) #remove degrees if you want your answer in radians

alpha = AngleBtw2Points([5,5],[7,4])
print(alpha)

# angle between 3 points
import math
def getAngle(a, b, c):
    ang = math.degrees(math.atan2(c[1] - b[1], c[0] - b[0]) - math.atan2(a[1] - b[1], a[0] - b[0]))
    return ang


print(getAngle((5, 0), (0, 0), (0, 5)))


#dist = math.hypot(x2-x1, y2-y1)


def multiObjectiveFitnessFunction(chromosome,strikerDamage, strikerPosition, strikerColliisonPosition,
                                  victimDamage, victimPosition, victimColliisonPosition):
    print("multiobjective_fitnessfunction")
    population_chromosome = chromosome
    striker_Damage = strikerDamage
    victim_Damage = victimDamage

    distance_stiker = math.hypot(strikerColliisonPosition[0] - strikerPosition[0], strikerColliisonPosition[1] - strikerPosition[1])
    distance_victim = math.hypot(victimColliisonPosition[0] - victimPosition[0], victimColliisonPosition[1] - victimPosition[1])

    print(distance_stiker)
    print(distance_victim)

    striker_alpha = getAngle((30,0), strikerColliisonPosition, strikerPosition)
    victim_alpha = getAngle((0,30), victimColliisonPosition, victimPosition)

    striker_heading = AngleBtw2Points((30,0), strikerColliisonPosition)

    victim_heading = AngleBtw2Points((0,30), victimColliisonPosition)

    print(striker_heading)
    print(victim_heading)

    print(striker_alpha)
    print(victim_alpha)

    print("Angle after collision")
    print((striker_heading + striker_alpha) % 360)
    print((victim_heading + victim_alpha) % 360)







def createCrashSimulation():
    print("Crash Simulation")

    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
    scenario = Scenario('GridMap', 'road_crash_simulation')

    road_a = Road('track_editor_C_center', looped=False)
    road_b = Road('track_editor_C_center', looped=False)

    nodesa = [
        (30, 0, -4, 4),
        (0, 0, -4, 4)
    ]

    nodesb = [
        (0, 30, -4, 4),
        (0, 0, -4, 4)
   ]

    road_a.nodes.extend(nodesa)
    road_b.nodes.extend(nodesb)

    # Create an ETK800 with the licence plate 'PYTHON'
    vehicleA = Vehicle('ego_vehicleA', model='etk800', licence='PYTHON')
    # Add it to our scenario at this position and rotation

    damageS = Damage();
    vehicleA.attach_sensor('damagesS', damageS);

    scenario.add_vehicle(vehicleA, pos=(30, 0, 0), rot=(0, 0, 90))

    # Create an ETK800 with the licence plate 'PYTHON'
    vehicleB = Vehicle('ego_vehicleB', model='etk800', licence='PYTHON')
    # Add it to our scenario at this position and rotation

    damageV = Damage();
    vehicleB.attach_sensor('damagesV', damageV);

    scenario.add_vehicle(vehicleB, pos=(0, 30, 0), rot=(0, 0, 0))


    scenario.add_road(road_a)
    scenario.add_road(road_b)

    scenario.make(beamng)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()

        node0 = {
            'pos': (30, 0, 0),
            'speed': 0,
        }

        node1 = {
            'pos': (0, 0, 0),
            'speed': 20,
        }

        script = list()
        script.append(node0)
        script.append(node1)

        vehicleA.ai_set_line(script)

        node3 = {
            'pos': (0, 30, 0),
            'speed': 0,
        }

        node4 = {
            'pos': (0, 0, 0),
            'speed': 20,
        }

        script = list()
        script.append(node3)
        script.append(node4)

        vehicleB.ai_set_line(script)

        time.sleep(12)
 #       input('Press enter when done...')
        vehicleA.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
        sensors = bng.poll_sensors(vehicleA)
        damage_striker = sensors['damagesS']
        print(sensors['damagesS'])
        print(vehicleA.state['pos'])

        vehicleB.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
        sensors = bng.poll_sensors(vehicleB)
        damage_victim = sensors['damagesV']
        print(sensors['damagesV'])
        print(vehicleB.state['pos'])

        multiObjectiveFitnessFunction(123456789, damage_striker, vehicleA.state['pos'], (0,0), damage_victim, vehicleB.state['pos'], (0,0))
        # multiobjective fitness function.

        bng.stop_scenario()

        # bng.load_scenario(scenario)
        # bng.start_scenario()
        #
        # print("sleep")
        # time.sleep(10)
        # print("wake")
        #
        # node0 = {
        #     'pos': (30, 0, 0),
        #     'speed': 0,
        # }
        #
        # node1 = {
        #     'pos': (0, 0, 0),
        #     'speed': 30,
        # }
        #
        # script = list()
        # script.append(node0)
        # script.append(node1)
        #
        # vehicleA.ai_set_line(script)
        #
        # node0 = {
        #     'pos': (0, 30, 0),
        #     'speed': 0,
        # }
        #
        # node1 = {
        #     'pos': (0, 0, 0),
        #     'speed': 30,
        # }
        #
        # script = list()
        # script.append(node0)
        # script.append(node1)
        #
        # vehicleB.ai_set_line(script)
        #
        # input('Press enter when done...')

    finally:
        bng.close()



createCrashSimulation()


# scenario.make(beamng)
# bng = beamng.open(launch=True)
# try:
#     bng.load_scenario(scenario)
#     bng.start_scenario()
#
#     input('Press enter when done...')
# finally:
#     bng.close()

