from cmath import atan
from itertools import count


map = [[1,1,1],[2,2,2],[1,2,2]]
aTotal = 0
for x in map:
    aTotal = aTotal + x.count(1)

print(aTotal)