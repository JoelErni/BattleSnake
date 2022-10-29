from cmath import atan
from itertools import count


map = [[1,1,1],[2,2,2],[1,2,2]]
def floodfill(matrix, x, y):
        if matrix[x][y] == "a":  
            matrix[x][y] = "c" 
            if x > 0:
                floodfill(matrix,x-1,y)
            if x < len(matrix[y]) - 1:
                floodfill(matrix,x+1,y)
            if y > 0:
                floodfill(matrix,x,y-1)
            if y < len(matrix) - 1:
                floodfill(matrix,x,y+1)


print(aTotal)