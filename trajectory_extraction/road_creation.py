
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging


def main():
    beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')

    scenario = Scenario('GridMap', 'road_test')
    road_a = Road('custom_track_center', looped=True)
    nodes = [
        (0, 0, 0, 5),
        (25, 300, 0, 6),
        (25, 350, 0, 4),
        (-25, 350, 0, 5),
    ]
    road_a.nodes.extend(nodes)
    scenario.add_road(road_a)

    road_b = Road('track_editor_C_center')
    nodes = [
        (0, 0, 0, 5),
        (50, 375, 0, 5),
    ]
    road_b.nodes.extend(nodes)
    scenario.add_road(road_b)
    vehicle = Vehicle('ego', model='etk800', licence='PYTHON', colour='Black')
    scenario.add_vehicle(vehicle,  pos = ( 0, 0, 0.163609), rot=(0,0,0))
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