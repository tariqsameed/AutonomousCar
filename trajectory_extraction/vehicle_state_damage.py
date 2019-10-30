import time
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
from beamngpy.sensors import Damage

sd = {'lowpressure': False, 'damageExt': 7000, 'type': 'Damage', 'damage': 31603.890625, 'partDamage': {'etk800_bumperbar_F': {'name': 'Front Bumper Support', 'damage': 1}, 'etk800_body_wagon': {'name': 'Wagon Unibody', 'damage': 0.07815442561205273}, 'etk800_door_FL': {'name': 'Front Left Door', 'damage': 0.009174311926605505}, 'etk800_headlight_R': {'name': 'Right Headlight', 'damage': 0.7272727272727273}, 'etk800_bumper_F': {'name': 'Front Bumper', 'damage': 1}, 'etk800_headlight_L': {'name': 'Left Headlight', 'damage': 1}, 'etk800_fender_R': {'name': 'Front Right Fender', 'damage': 0.01639344262295082}, 'etk800_fender_L': {'name': 'Front Left Fender', 'damage': 0.21311475409836064}, 'etk800_hood': {'name': 'Hood', 'damage': 1}}, 'deformGroupDamage': {'windshield_break': {'maxEvents': 5109.999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.00019569471624266148}, 'radtube_break': {'maxEvents': 599.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001666666666666667}, 'doorglass_RR_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'sideglass_R_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'taillightglass_L_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'radiator_damage': {'maxEvents': 2799.9999999999995, 'damage': 0.012857142857142859, 'eventCount': 36, 'invMaxEvents': 0.0003571428571428572}, 'driveshaft': {'maxEvents': 99.99999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.010000000000000002}, 'doorglass_FR_break': {'maxEvents': 659.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015151515151515154}, 'doorglass_FL_break': {'maxEvents': 659.9999999999999, 'damage': 0.0015151515151515154, 'eventCount': 1, 'invMaxEvents': 0.0015151515151515154}, 'fendersignal_R_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'headlightglass_L_break': {'maxEvents': 439.99999999999994, 'damage': 0.0840909090909091, 'eventCount': 37, 'invMaxEvents': 0.002272727272727273}, 'headlightglass_R_break': {'maxEvents': 439.99999999999994, 'damage': 0.03636363636363637, 'eventCount': 16, 'invMaxEvents': 0.002272727272727273}, 'fendersignal_L_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'taillightglass_R_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'foglightglass_L_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgatelight_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sideglass_L_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'tailgatelight_L_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sunroof_break': {'maxEvents': 813.3333333333334, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0012295081967213114}, 'doorglass_RL_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'foglightglass_R_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgateglass_break': {'maxEvents': 899.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0011111111111111113}}}
vd = {'lowpressure': True, 'damageExt': 2500, 'type': 'Damage', 'damage': 15404.4619140625, 'partDamage': {'etk800_body_wagon': {'name': 'Wagon Unibody', 'damage': 0.003295668549905838}, 'etk800_bumper_F': {'name': 'Front Bumper', 'damage': 0.020338983050847456}, 'etk800_door_FR': {'name': 'Front Right Door', 'damage': 0.027522935779816515}, 'etk800_fender_R': {'name': 'Front Right Fender', 'damage': 1}, 'etk800_swaybar_F': {'name': 'Front Sway Bar', 'damage': 1}, 'etk800_steering': {'name': 'Steering', 'damage': 1}, 'etk_exhaust_i6_petrol': {'name': 'Dual Outlet Exhaust', 'damage': 0.013513513513513514}, 'etk800_suspension_F': {'name': 'Independent Front Suspension', 'damage': 0.09836065573770492}, 'etk800_bumper_R': {'name': 'Rear Bumper', 'damage': 0.144}}, 'deformGroupDamage': {'windshield_break': {'maxEvents': 5109.999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.00019569471624266148}, 'radtube_break': {'maxEvents': 599.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001666666666666667}, 'doorglass_RR_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'sideglass_R_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'taillightglass_L_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'radiator_damage': {'maxEvents': 2799.9999999999995, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0003571428571428572}, 'driveshaft': {'maxEvents': 99.99999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.010000000000000002}, 'doorglass_FR_break': {'maxEvents': 659.9999999999999, 'damage': 0.0030303030303030307, 'eventCount': 2, 'invMaxEvents': 0.0015151515151515154}, 'doorglass_FL_break': {'maxEvents': 659.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015151515151515154}, 'fendersignal_R_break': {'maxEvents': 1299.9999999999998, 'damage': 0.016923076923076926, 'eventCount': 22, 'invMaxEvents': 0.0007692307692307693}, 'headlightglass_L_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'headlightglass_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'fendersignal_L_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'taillightglass_R_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'foglightglass_L_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgatelight_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sideglass_L_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'tailgatelight_L_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sunroof_break': {'maxEvents': 813.3333333333334, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0012295081967213114}, 'doorglass_RL_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'foglightglass_R_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgateglass_break': {'maxEvents': 899.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0011111111111111113}}}


def DamageExtractoin(striker_damage, victim_damage):
    print("damage extraction")

    striker_damage_area = ""
    victim_damage_area = ""

    if striker_damage['damage'] > 100:
        print(striker_damage['partDamage'])
        



    if victim_damage['damage'] > 100:
        print(victim_damage['partDamage'])



DamageExtractoin(sd,vd)



#
# print("Damage Crash Simulation")
#
# beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')
# scenario = Scenario('GridMap', 'road_crash_simulation')
#
# road_a = Road('track_editor_C_center', looped=False)
# road_b = Road('track_editor_C_center', looped=False)
#
# nodesa = [
#     (30, 0, -4, 4),
#     (0, 0, -4, 4)
# ]
#
# nodesb = [
#     (0, 30, -4, 4),
#     (0, 0, -4, 4)
# ]
#
# road_a.nodes.extend(nodesa)
# road_b.nodes.extend(nodesb)
#
# vehicleA = Vehicle('ego_vehicle', model='etk800', licence='PYTHON')
#
# damageS = Damage();
# vehicleA.attach_sensor('damagesS', damageS);
#
# scenario.add_vehicle(vehicleA, pos=(30, 0, 0), rot=(0, 0, 90))
#
# vehicleB = Vehicle('victim_vehicle', model='etk800', licence='PYTHON')
#
# damageV = Damage();
# vehicleB.attach_sensor('damagesV', damageV);
#
# scenario.add_vehicle(vehicleB, pos=(0, 30, 0), rot=(0, 0, 0))
#
#
# scenario.add_road(road_a)
# scenario.add_road(road_b)
#
# scenario.make(beamng)
#
# bng = beamng.open(launch=True)
# try:
#     bng.load_scenario(scenario)
#     bng.start_scenario()
#
#     time.sleep(50)
#  #       input('Press enter when done...')
#     vehicleA.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
#     sensors = bng.poll_sensors(vehicleA)
#     damage_striker = sensors['damagesS']
#     print(sensors['damagesS'])
#
#     vehicleB.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
#     sensors = bng.poll_sensors(vehicleB)
#     damage_victim = sensors['damagesV']
#     print(sensors['damagesV'])
#
#     bng.stop_scenario()
#
# finally:
#     bng.close()