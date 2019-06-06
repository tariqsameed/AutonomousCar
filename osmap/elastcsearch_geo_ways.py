import sys
import xml.etree.ElementTree as ET
import re
from elasticsearch import Elasticsearch

filename = 'passau'
path = "../resources/osm/"
map = path + filename + '.osm'

es = Elasticsearch()

# wayid, nodes, separate Lanes, width of road
try:
    mapFile = open(map, 'r', encoding="utf8")
    fullway = ""
    nodes=[]
    lanes = 0
    width = 0
    maxSpeed = 0
    wayId = 0
    sideWalk = ""
    lanesForward = 0
    lanesBackward = 0
    oneway = ""
    roadSign =""
    for line in mapFile:
        if line.startswith('  <way'):
            fullway = fullway + line
            wayId = (re.findall('\d+', line))[0]
        elif line.startswith('  </way'):
            fullway = fullway + line

            e1 = {
                "nodes": '|'.join(nodes),
                "number_lanes": lanes,
                "width": width,
                "side_walk": sideWalk,
                "max_speed": maxSpeed,
                "lane_backward":lanesForward,
                "lane_forward":lanesBackward,
                "one_way": oneway,
                "road_sign": roadSign
            }
            res = es.index(index='waygeometry', doc_type='ways', id=wayId, body=e1)
            print(res)
            wayId = 0
            nodes = []
            fullway = ""
            lanes = 0
            width = 0
            maxSpeed = 0
            sideWalk =""
            lanesForward= 0
            lanesBackward= 0
            oneway = ""
            roadSign = ""
        elif line.startswith('    <nd'):
            fullway = fullway + line
            node = ET.fromstring(line)
            nodes.append(node.attrib['ref'])
        elif line.startswith('    <tag k="lanes"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            lanes = lane.attrib['v']
        elif line.startswith('    <tag k="width"'):
            fullway = fullway + line
            width = ET.fromstring(line)
            value = width.attrib['v']
            if (value.isdigit()):
                width = value
            else:
                width =  (re.findall('\d+',value))[0]
        elif line.startswith('    <tag k="maxspeed"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            maxSpeed = lane.attrib['v']
        elif line.startswith('    <tag k="sidewalk"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            sideWalk = lane.attrib['v'] # lanes:forward
        elif line.startswith('    <tag k="lanes:forward"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            lanesForward = lane.attrib['v']
        elif line.startswith('    <tag k="lanes:backward"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            lanesBackward = lane.attrib['v'] #
        elif line.startswith('    <tag k="oneway"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            oneway = lane.attrib['v']
        elif line.startswith('    <tag k="traffic_sign"'):
            fullway = fullway + line
            lane = ET.fromstring(line)
            roadSign = lane.attrib['v']

    mapFile.close()

    es.indices.refresh(index="waygeometry")
    res = es.search(index="waygeometry", body={"query": {"match": {"nodes": "595019|4842300509"}}})
    print("Got %d Hits:" % res['hits']['total']['value'])

    for hit in res['hits']['hits']:
        print(hit['_id'])
        print(hit['_source']['nodes'])
        print(hit['_source']['number_lanes'])
        print(hit['_source']['width'])
        print(hit['_score'])
        print('**********************')

except IOError:
    print("Could not read file or file does not exist: ", map)
    sys.exit()



