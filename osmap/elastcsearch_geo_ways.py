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
    oneway =""
    nodes=[]
    lanes = 0
    width = 0
    wayId = 0
    for line in mapFile:
        if line.startswith('  <way'):
            oneway = oneway + line
            wayId = (re.findall('\d+', line))[0]
        elif line.startswith('  </way'):
            oneway = oneway + line

            e1 = {
                "nodes": '|'.join(nodes),
                "number_lanes": lanes,
                "width": width,

            }
            res = es.index(index='geometry', doc_type='ways', id=wayId, body=e1)
            print(res)
            wayId = 0
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

    mapFile.close()

    es.indices.refresh(index="geometry")
    res = es.search(index="geometry", body={"query": {"match": {"nodes": "595019|4842300509"}}})
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



