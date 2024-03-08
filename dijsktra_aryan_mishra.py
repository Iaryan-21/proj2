import math
import numpy as np
from queue import PriorityQueue
import cv2
import time

height = 500
width= 1200
opt_img = np.zeros((height, width), np.uint8)
start_time = time.time() 
start = [10,10]  
goal = [20,20] 
solvable = True

for x in range(width): 
    for y in range(height): 
        if (95<x<175) and (95<y<500):
            opt_img[y][x]=1
        if (270<x<355) and (0<y<405):
            opt_img[y][x]=1
        if (570<x<730) and (175<y<325):
            opt_img[y][x]=1
        if (570 <= x <= 730) and (y > 325):
            y_line_top = 400 - abs(x - 650)  
            if y <= y_line_top:
                opt_img[y][x] = 1
        if (570 <= x <= 730) and (y < 175):
            y_line_bottom = 100 + abs(x - 650) 
            if y >= y_line_bottom:
                opt_img[y][x] = 1
        if (895<x<1020) and (370<y<455):
            opt_img[y][x]=1
        if (895<x<1020) and (45<y<130):
            opt_img[y][x]=1
        if (1020<x<1105) and (45<y<455):
            opt_img[y][x]=1 
        if (y>=0 and y<=5):
            opt_img[y][x]=1
        if (y<=500 and y>=495):
            opt_img[y][x]=1
        if (x>=0 and x<=5):
            opt_img[y][x]=1
        if (x<=1200 and x>=1195):
            opt_img[y][x]=1
if opt_img[start[0],start[1]]==1 or opt_img[goal[0],goal[1]]==1:
    print("Not Valid enteries:")
    solvable  =False
else:
    pass


class Node:
    def __init__(self, position, cost, parent): 
        self.position = position
        self.x = position[0]
        self.y = position[1]
        self.cost = cost
        self.parent = parent

def explore(node): 
    i = node.x
    j = node.y
    paths = [(i, j + 1), (i + 1, j), (i - 1, j), (i, j - 1), (i + 1, j + 1), (i - 1, j - 1), (i - 1, j + 1),
             (i + 1, j - 1)]  
    valid_paths = []
    for position, path in enumerate(paths):
        if not (path[0] >= width or path[0] < 0 or path[1] >= height or path[1] < 0):  
            if opt_img[path[1]][path[0]] == 0:  
                cost = 1.414 if position > 3 else 1
                valid_paths.append([path, cost])
    return valid_paths 


