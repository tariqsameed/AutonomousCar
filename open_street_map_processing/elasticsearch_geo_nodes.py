import sys
import xml.etree.ElementTree as ET
from elasticsearch import Elasticsearch

filename = 'passau'
path = "../resources/osm/"
map = path + filename + '.osm'

es = Elasticsearch()

# wayid, nodes, separate Lanes, width of road
try:
    mapFile = open(map, 'r', encoding="utf8")
    fullway = ""
    nodeId = ""
    lat = 0
    lon = 0
    highway = "" # traffic signal
    crossing = ""
    roadSign = ""
    for line in mapFile:
        line = line.lstrip()
        if line.startswith('<node'):
            if line.endswith('/>\n'):
                node = ET.fromstring(line.lstrip())
                nodeId = node.attrib['id']
                lat = (float(node.attrib['lat']))
                lon = (float(node.attrib['lon']))

                # Index Elements
                e1 = {
                    "lat": lat,
                    "lon": lon,
                    "highway": highway,
                    "crossing": crossing,
                    "road_sign": roadSign,
                }
                res = es.index(index='nodegeometry', doc_type='nodes', id=nodeId, body=e1)
                print(res)
                nodeId = ""
                lat = 0
                long = 0
                highway = ""  # traffic signal
                crossing = ""
                roadSign = ""

            elif line.endswith('>\n'):
                line = line[:-2] + '/>\n'
                node = ET.fromstring(line.lstrip())
                nodeId = node.attrib['id']
                lat = (float(node.attrib['lat']))
                lon = (float(node.attrib['lon']))

        elif line.startswith('</node'):
            e1 = {
                "lat": lat,
                "lon": lon,
                "highway": highway,
                "crossing": crossing,
                "road_sign": roadSign,
            }
            res = es.index(index='nodegeometry', doc_type='nodes', id=nodeId, body=e1)
            print(res)
            nodeId = ""
            lat = 0
            long = 0
            highway = ""  # traffic signal
            crossing = ""
            roadSign = ""
        elif line.startswith('<tag k="highway"'):
            lane = ET.fromstring(line)
            highway = lane.attrib['v']
        elif line.startswith('<tag k="crossing"'):
            lane = ET.fromstring(line)
            crossing = lane.attrib['v']
        elif line.startswith('<tag k="traffic_sign"'):
            lane = ET.fromstring(line)
            roadSign = lane.attrib['v']

    mapFile.close()

    es.indices.refresh(index="nodegeometry")
    res = es.search(index="nodegeometry", body={"query": {"match": {"_id": "595019"}}})
    print("Got %d Hits:" % res['hits']['total']['value'])

    for hit in res['hits']['hits']:
        print(hit['_id'])
        print(hit['_source']['lat'])
        print(hit['_source']['lon'])
        print(hit['_score'])
        print('**********************')

except IOError:
    print("Could not read file or file does not exist: ", map)
    sys.exit()



