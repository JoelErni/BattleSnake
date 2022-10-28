import math

c1 = {'x': 0, 'y': 0}
c2 = {'x': 4, 'y': 3}



def Euclidean_Distance(x,y) -> float:
    result = math.sqrt(math.pow(x['x']-y['x'],2)+math.pow(x['y']-y['y'],2))
    return result

print(Euclidean_Distance(c1,c2))