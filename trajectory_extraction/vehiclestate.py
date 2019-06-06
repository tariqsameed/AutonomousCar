import time

import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from beamngpy import BeamNGpy, Vehicle, Scenario, Road
from beamngpy.sensors import Electrics, Damage
from IPython.display import display

# Instantiate a BeamNGpy instance the other classes use for reference & communication
beamng = BeamNGpy('localhost', 64256, home='F:\Softwares\BeamNG_Research_SVN')  # This is the host & port used to communicate over

# Create a vehile instance that will be called 'ego' in the simulation
# using the etk800 model the simulator ships with
vehicle = Vehicle('ego', model='van', licence='PYTHON', colour='white')
vehicleV = Vehicle('victim', model='etk800', licence='PYTHON', colour='red')
# Create an Electrics sensor and attach it to the vehicle
electrics = Electrics()
vehicle.attach_sensor('electrics', electrics);

damage = Damage();
vehicle.attach_sensor('damages', damage);

# Create a scenario called vehicle_state taking place in the west_coast_usa map the simulator ships with
scenario = Scenario('west_coast_usa', 'vehicle_state')
# Add the vehicle and specify that it should start at a certain position and orientation.
# The position & orientation values were obtained by opening the level in the simulator,
# hitting F11 to open the editor and look for a spot to spawn and simply noting down the
# corresponding values.
scenario.add_vehicle(vehicle, pos=(-727.121, 101, 118.675), rot=(0, 0, 45))  # 45 degree rotation around the z-axis
#scenario.add_vehicle(vehicleV,pos=(-707.121, 101, 118.675), rot=(0, 0, 45))

# The make function of a scneario is used to compile the scenario and produce a scenario file the simulator can load
scenario.make(beamng)

bng = beamng.open()
bng.load_scenario(scenario)
bng.start_scenario()  # After loading, the simulator waits for further input to actually start

#vehicle.ai_set_mode('span')

vehicle.update_vehicle()
sensors = bng.poll_sensors(vehicle)

print('The vehicle position is:')
display(vehicle.state['pos'])

print('The vehicle direction is:')
display(vehicle.state['dir'])

print('The wheel speed is:')
display(sensors['electrics']['values']['wheelspeed'])

print('The throttle intensity is:')
display(sensors['electrics']['values']['throttle'])

print('The brake intensity is:')
display(sensors['electrics']['values']['brake'])

print('The Damage is:')
display(sensors['damages'])
display(damage)

Road('track_editor_C_center', looped=True)

positions = list()
directions = list()
wheel_speeds = list()
throttles = list()
brakes = list()
damages = list()

for _ in range(240):
    time.sleep(0.1)
    vehicle.update_vehicle()  # Synchs the vehicle's "state" variable with the simulator
    sensors = bng.poll_sensors(vehicle)  # Polls the data of all sensors attached to the vehicle
    positions.append(vehicle.state['pos'])
    directions.append(vehicle.state['dir'])
    wheel_speeds.append(sensors['electrics']['values']['wheelspeed'])
    throttles.append(sensors['electrics']['values']['throttle'])
    brakes.append(sensors['electrics']['values']['brake'])

damages.append(sensors['damages'])
bng.close()

#print(wheel_speeds)
print(directions)



#x = [p[0] for p in positions]
#y = [p[1] for p in positions]
#plt.plot(x, y, '.')
#plt.axis('square')
#plt.show()
#plt.clf()