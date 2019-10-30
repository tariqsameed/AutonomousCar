import time
from beamngpy import BeamNGpy, Scenario, Road, Vehicle, setup_logging
from beamngpy.sensors import Damage

sd = {'lowpressure': False, 'damageExt': 3000, 'type': 'Damage', 'damage': 8887.68115234375, 'partDamage': {'etk800_headlight_L': {'name': 'Left Headlight', 'damage': 1}, 'etk800_body_wagon': {'name': 'Wagon Unibody', 'damage': 0.026836158192090395}, 'etk800_hood': {'name': 'Hood', 'damage': 1}, 'etk800_bumperbar_F': {'name': 'Front Bumper Support', 'damage': 1}, 'etk800_fender_L': {'name': 'Front Left Fender', 'damage': 0.06557377049180328}, 'etk800_bumper_F': {'name': 'Front Bumper', 'damage': 1}}, 'deformGroupDamage': {'windshield_break': {'maxEvents': 5109.999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.00019569471624266148}, 'radtube_break': {'maxEvents': 599.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001666666666666667}, 'doorglass_RR_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'sideglass_R_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'taillightglass_L_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'radiator_damage': {'maxEvents': 2799.9999999999995, 'damage': 0.005357142857142858, 'eventCount': 15, 'invMaxEvents': 0.0003571428571428572}, 'driveshaft': {'maxEvents': 99.99999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.010000000000000002}, 'doorglass_FR_break': {'maxEvents': 659.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015151515151515154}, 'doorglass_FL_break': {'maxEvents': 659.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015151515151515154}, 'fendersignal_R_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'headlightglass_L_break': {'maxEvents': 439.99999999999994, 'damage': 0.10227272727272729, 'eventCount': 45, 'invMaxEvents': 0.002272727272727273}, 'headlightglass_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'fendersignal_L_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'taillightglass_R_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'foglightglass_L_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgatelight_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sideglass_L_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'tailgatelight_L_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sunroof_break': {'maxEvents': 813.3333333333334, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0012295081967213114}, 'doorglass_RL_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'foglightglass_R_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgateglass_break': {'maxEvents': 899.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0011111111111111113}}}
vd = {'lowpressure': False, 'damageExt': 4000, 'type': 'Damage', 'damage': 6643.386474609375, 'partDamage': {'etk800_tailgateglass': {'name': 'Tailgate Glass', 'damage': 1}, 'etk800_body_wagon': {'name': 'Wagon Unibody', 'damage': 0.019303201506591337}, 'etk800_tailgate': {'name': 'Tailgate', 'damage': 1}, 'etk_exhaust_i6_petrol': {'name': 'Dual Outlet Exhaust', 'damage': 0.08108108108108109}, 'etk800_bumper_R': {'name': 'Rear Bumper', 'damage': 0.648}}, 'deformGroupDamage': {'windshield_break': {'maxEvents': 5109.999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.00019569471624266148}, 'radtube_break': {'maxEvents': 599.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001666666666666667}, 'doorglass_RR_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'sideglass_R_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'taillightglass_L_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'radiator_damage': {'maxEvents': 2799.9999999999995, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0003571428571428572}, 'driveshaft': {'maxEvents': 99.99999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.010000000000000002}, 'doorglass_FR_break': {'maxEvents': 659.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015151515151515154}, 'doorglass_FL_break': {'maxEvents': 659.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015151515151515154}, 'fendersignal_R_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'headlightglass_L_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'headlightglass_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'fendersignal_L_break': {'maxEvents': 1299.9999999999998, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0007692307692307693}, 'taillightglass_R_break': {'maxEvents': 539.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0018518518518518521}, 'foglightglass_L_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgatelight_R_break': {'maxEvents': 439.99999999999994, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.002272727272727273}, 'sideglass_L_break': {'maxEvents': 666.6666666666666, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015}, 'tailgatelight_L_break': {'maxEvents': 439.99999999999994, 'damage': 0.004545454545454546, 'eventCount': 2, 'invMaxEvents': 0.002272727272727273}, 'sunroof_break': {'maxEvents': 813.3333333333334, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0012295081967213114}, 'doorglass_RL_break': {'maxEvents': 639.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0015625000000000003}, 'foglightglass_R_break': {'maxEvents': 999.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.001}, 'tailgateglass_break': {'maxEvents': 899.9999999999999, 'damage': 0, 'eventCount': 0, 'invMaxEvents': 0.0011111111111111113}}}

def DamageExtraction(striker_damage, victim_damage):
    print("damage extraction")

    striker_damage_area = ""
    victim_damage_area = ""

    # Striker Damage
    if striker_damage['damage'] > 100:
        stkeys = striker_damage['partDamage']
        #front damage
        for keys in stkeys:
            if 'bumperbar_F' in keys or 'body_wagon' in keys or 'door_FL' in keys or 'headlight_R' in keys or 'bumper_F' in keys or  'headlight_L' in keys or 'fender_R' in keys or 'fender_L' in keys or 'hood' in keys:
                #print("striker front")
                striker_damage_area = striker_damage_area + 'F'
                break


        # back damage
        for keys in stkeys:
            if 'tailgateglass' in keys or 'tailgate' in keys or 'taillight_L' in keys or 'exhaust_i6_petrol' in keys or 'bumper_R' in keys:
                #print("striker back")
                striker_damage_area = striker_damage_area + 'B'
                break

        # right damage
        for keys in stkeys:
            if 'mirror_R' in keys or 'doorglass_FR' in keys or 'door_RR_wagon' in keys or 'door_FR' in keys:
                #print("striker right")
                striker_damage_area = striker_damage_area + 'R'
                break

        # left damage
        for keys in stkeys:
            if 'fender_L' in keys or 'door_FL' in keys or 'doorglass_RL_wagon' in keys or 'door_RL_wagon' in keys or 'mirror_L' in keys:
                #print("striker left")
                striker_damage_area = striker_damage_area + 'L'
                break

        print(striker_damage_area)



    # Victim Damage
    if victim_damage['damage'] > 100:
        vikeys = victim_damage['partDamage']
        # front damage
        for keys in vikeys:
            if 'bumperbar_F' in keys or 'door_FL' in keys or 'headlight_R' in keys or 'bumper_F' in keys or 'headlight_L' in keys or 'fender_R' in keys or 'fender_L' in keys or 'hood' in keys:
                #print("victim front")
                victim_damage_area = victim_damage_area + 'F'
                break

        # back damage
        for keys in vikeys:
            if 'tailgateglass' in keys or 'tailgate' in keys or 'exhaust_i6_petrol' in keys or 'bumper_R' in keys:
                #print("victim back")
                victim_damage_area = victim_damage_area + 'B'
                break

        # right damage
        for keys in vikeys:
            if 'mirror_R' in keys or 'doorglass_FR' in keys or 'door_RR_wagon' in keys or 'door_FR' in keys:
                #print("victim right")
                victim_damage_area = victim_damage_area + 'R'
                break

        # left damage
        for keys in vikeys:
            if 'fender_L' in keys or 'door_FL' in keys or 'doorglass_RL_wagon' in keys or 'door_RL_wagon' in keys or 'mirror_L' in keys:
                #print("vicitm left")
                victim_damage_area = victim_damage_area + 'L'
                break

        print(victim_damage_area)



DamageExtraction(sd,vd)



#
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
#     time.sleep(30)
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
#     DamageExtraction(damage_striker, damage_victim)
#
#     bng.stop_scenario()
#
# finally:
#     bng.close()