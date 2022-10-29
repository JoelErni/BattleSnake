a = [[1,2,3],[2,3,1],[3,1,2]]


output = ""
for x in range(len(a)):
    for y in range(len(a[x])):
        output = output + str(a[x][y])
    output = output + "\n"
print(output)