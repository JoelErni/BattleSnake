import math
n = {'x': 0, 'y': 0}
c1 = [{'x': 4, 'y': 3},{'x': 3, 'y': 6},{'x': 4, 'y': 8}]
res={}
for x in c1:
    res[n] = math.sqrt(math.pow(n['x']-x['x'],2)+math.pow(n['y']-x['y'],2))