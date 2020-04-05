import sys
import xml.etree.ElementTree as ET
import re
import pickle

filename = 'passau'
path = "../resources/osm/"

filename = 'munich4'
path = r'F:\Passau_Masters\Research Work\Alessio\AutonomousCar\expriments_simulation\crash_simulation_6\\'


map = path + filename + '.osm'
map_lanes = path + filename + '.lanes'
map_width = path + filename + '.width'
# separate Lanes and width of road
try:
    mapFile = open(map, 'r', encoding="utf8")
    oneway =""
    nodes=[]
    lanes_dict = {}
    width_dict = {}
    lanes = 0
    width = 0
    for line in mapFile:
        if line.startswith('  <way'):
            oneway = oneway + line
        elif line.startswith('  </way'):
            oneway = oneway + line
            for node in nodes:
                lanes_dict[node] = lanes
                width_dict[node] = width

            nodes = []
            oneway = ""
            lanes = 0
            width = 0
        elif line.startswith('    <nd'):
            oneway = oneway + line
            node = ET.fromstring(line)
            nodes.append(node.attrib['ref'])
        elif line.startswith('    <tag k="lanes"'):
            oneway = oneway + line
            lane = ET.fromstring(line)
            lanes = lane.attrib['v']
        elif line.startswith('    <tag k="width"'):
            oneway = oneway + line
            width = ET.fromstring(line)
            value = width.attrib['v']
            if (value.isdigit()):
                width = value
            else:
                width =  (re.findall('\d+',value))[0]

    # print(lanes_dict.items()) # displays you pair tuple of key and value
    # print(width_dict.items())  # displays you pair tuple of key and value
    mapFile.close()
    pickle.dump(lanes_dict, open(map_lanes, "wb"))
    print("Lanes File Created.")

    pickle.dump(width_dict, open(map_width, "wb"))
    print("Width File Created.")

except IOError:
    print("Could not read file or file does not exist: ", map)
    sys.exit()