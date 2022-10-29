a = [[2,0],[0,2]]


output = ""
for x in range(len(a)):
    for y in range(len(a[x])):
        output = output + str(a[x][y])
    output = output + "\n"
print(output)