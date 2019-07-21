
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
import time

import sys
sys.stdout = open('vehicle.txt','w')

def main():
    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')

    scenario = Scenario('GridMap', 'road_test')
    road_a = Road('custom_track_center', looped=False)
    nodes = [
        (0, 0, 0, 4),
        (0, 400, 0, 4),
    ]
    road_a.nodes.extend(nodes)
    scenario.add_road(road_a)

    vehicle = Vehicle('ego', model='etk800', licence='PYTHON', colour='Black')
    scenario.add_vehicle(vehicle,  pos = ( 0, 0, 0.163609) , rot=(0,0,180)) # 0.163609 ,
    scenario.make(beamng)

    script = list()

    node0 = {
        'pos' : ( 0, 0, 0.163609),
        'speed': 20,
    }

    node1 = {
        'pos': (0, 100, 0.163609),
        'speed': 30,
    }


    script.append(node0)
    script.append(node1)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()
        vehicle.ai_set_line(script)
        # update the state of vehicle at impact.


        for _ in range(100):
            time.sleep(0.1)
            vehicle.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
            sensors = bng.poll_sensors(vehicle)  # Polls the data of all sensors attached to the vehicle
            print(vehicle.state['pos'])
            if vehicle.state['pos'][1] > 99:
                print('free state')
                vehicle.control(throttle=0, steering=0, brake=0, parkingbrake=0)
                vehicle.update_vehicle()


        bng.stop_scenario()

        for _ in range(20):
            time.sleep(0.1)

        bng.load_scenario(scenario)
        bng.start_scenario()

        node0 = {
            'pos': (0, 50 , 0.163609),
            'speed': 20,
        }

        node1 = {
            'pos': (0, 100, 0.163609),
            'speed': 30,
        }

        script.append(node0)
        script.append(node1)

        vehicle.ai_set_line(script)

        input('Press enter when done...')
    finally:
        bng.close()


if __name__ == '__main__':
    main()