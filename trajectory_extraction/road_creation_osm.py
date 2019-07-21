
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging


def main():
    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')

    scenario = Scenario('GridMap', 'road_test')
    road_a = Road('custom_track_center', looped=False)
    nodes = [
        (0, 0, 0, 8),
        (125, 0, 0, 8),
        (250, -10, 0, 12)
    ]
    road_a.nodes.extend(nodes)
    scenario.add_road(road_a)

    road_b = Road('custom_track_center', looped=False)
    nodes = [
        (125, 0, 0,12 ),
        (250, -10, 0, 12)
    ]
    road_b.nodes.extend(nodes)
    scenario.add_road(road_b)

    road_c = Road('custom_track_center', looped=False)
    nodes = [
        (125, 125, 0, 8),
        (125, 0, 0, 8),
    ]
    road_c.nodes.extend(nodes)
    scenario.add_road(road_c)

    vehicle = Vehicle('ego', model='etk800', licence='PYTHON', colour='Black')
    scenario.add_vehicle(vehicle, pos=(0, 0, 0.163609), rot=(0, 0, 180))  # 0.163609 ,

    scenario.make(beamng)
    bng = beamng.open(launch=True)
    try:
        bng.load_scenario(scenario)
        bng.start_scenario()



        input('Press enter when done...')
    finally:
        bng.close()


if __name__ == '__main__':
    main()