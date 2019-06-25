
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging


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
        'x': 0,
        'y': 2,
        'z': 0.163609,
        't': 0.01,
    }

    node1 = {
        'x': 0,
        'y': 3,
        'z': 0.163609,
        't': 0.01,
    }

    node2 = {
        'x': 0,
        'y': 350,
        'z': 0.163609,
        't': 15,
    }

    node3 = {
        'x': 0,
        'y': 400,
        'z': 0.163609,
        't': 5,
    }

    script.append(node0)
    script.append(node1)
    script.append(node2)
    script.append(node3)

    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()
        vehicle.ai_set_script(script)

        input('Press enter when done...')
    finally:
        bng.close()


if __name__ == '__main__':
    main()