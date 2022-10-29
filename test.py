map = []
for y in reversed(range(11)):
    map1 = ['a'] * 11
    for x in range(11):
        if x & 2 == 0:
            map1[x] = 'b'
            break
    map.append(map1)
print(map)