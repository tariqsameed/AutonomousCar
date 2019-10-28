import time
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
from beamngpy.sensors import Electrics, Damage

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

    damage = Damage();
    vehicleA.attach_sensor('damagesS', damage);

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

        time.sleep(3)

        node0 = {
            'pos': (30, 0, 0),
            'speed': 0,
        }

        node1 = {
            'pos': (0, 0, 0),
            'speed': 30,
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
            'speed': 30,
        }

        script = list()
        script.append(node3)
        script.append(node4)

        vehicleB.ai_set_line(script)

        input('Press enter when done...')
        vehicleA.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
        sensors = bng.poll_sensors(vehicleA)
        print(sensors['damagesS'])

        vehicleB.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
        sensors = bng.poll_sensors(vehicleB)
        print(sensors['damagesV'])

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