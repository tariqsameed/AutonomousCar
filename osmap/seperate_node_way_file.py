import sys

filename = 'passau'
path = "../resources/osm/"

map = path + filename + '.osm'
map_nodes = path + filename + '.nodes'
map_ways = path + filename + '.ways'

# separate nodes
try:
    mapFile = open(map, 'r', encoding="utf8")
    mapNodesFile = open(map_nodes, 'w', encoding="utf8")
    for line in mapFile:
        if line.startswith('\t<node'):
            if line.endswith('/>\n'):
                mapNodesFile.write(line)
            elif line.endswith('>\n'):
                line = line[:-2] + '/>\n'
                mapNodesFile.write(line)
    mapFile.close()
    mapNodesFile.close()
    print("Nodes File Created.")

except IOError:
    print("Could not read file or file does not exist: ", map)
    sys.exit()

# separate ways
try:
    mapFile = open(map, 'r', encoding="utf8")
    mapWaysFile = open(map_ways, 'w', encoding="utf8")
    for line in mapFile:
        if line.startswith('\t<way') or line.startswith('\t</way'):
            mapWaysFile.write(line)
        elif line.startswith('\t\t<nd'):
            mapWaysFile.write(line)
    mapFile.close()
    mapWaysFile.close()
    print("Ways File Created.")

except IOError:
    print("Could not read file or file does not exist: ", map)
    sys.exit()
