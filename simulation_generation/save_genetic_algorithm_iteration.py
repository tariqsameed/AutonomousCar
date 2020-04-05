Dict = {1: 'Geeks', 2: 'For', 3: 'Geeks'}

f= open("genetic_algorithm_iteration.csv","w+")
lines = ""
for k, v in Dict.items():
    lines = lines + str(k) + ',' + str(v) + ','

lines = lines[:-1]
f.writelines(lines)