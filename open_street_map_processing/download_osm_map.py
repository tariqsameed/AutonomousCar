import requests

filename = 'passau'
path = "../resources/osm/"
map_nodes_ways = path + filename + '.osm'


lat = 48.5706833
lon = 13.4587882
around = 200

overpass_url = "http://overpass-api.de/api/interpreter"
overpass_query = """
[out:xml];
(
  way
  (around:"""+str(around)+""","""+str(lat)+""","""+str(lon)+""")
  [highway~"^(primary|secondary|tertiary|residential)$"]
  [name];
>;);out;
"""
response = requests.get(overpass_url,
                        params={'data': overpass_query})
data = response.text
f = open(map_nodes_ways, "w", encoding="utf8")
f.write(data)
f.close()