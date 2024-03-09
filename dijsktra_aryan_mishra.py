import math
import numpy as np
from queue import PriorityQueue
import cv2
import time

height = 500
width = 1200
opt_img = np.zeros((height, width), np.uint8)


for x in range(width): 
    for y in range(height): 
        if (95<x<175) and (95<y<500):
            opt_img[y, x] = 1
        if (270<x<355) and (0<y<405):
            opt_img[y, x] = 1
        if (570<x<730) and (175<y<325):
            opt_img[y, x] = 1
        if (570 <= x <= 730) and (y > 325):
            y_line_top = 400 - abs(x - 650)  
            if y <= y_line_top:
                opt_img[y, x] = 1
        if (570 <= x <= 730) and (y < 175):
            y_line_bottom = 100 + abs(x - 650)
            if y >= y_line_bottom:
                opt_img[y, x] = 1
        if (895<x<1020) and (370<y<455):
            opt_img[y, x] = 1
        if (895<x<1020) and (45<y<130):
            opt_img[y, x] = 1
        if (1020<x<1105) and (45<y<455):
            opt_img[y, x] = 1
        if (y>=0 and y<=5) or (y<=500 and y>=495) or (x>=0 and x<=5) or (x<=1200 and x>=1195):
            opt_img[y, x] = 1


start_time = time.time() 
start = tuple(map(int, input("Enter start coordinates (x, y) separated by comma: ").split(",")))
goal = tuple(map(int, input("Enter goal coordinates (x, y) separated by comma: ").split(",")))

if opt_img[start[1], start[0]] == 1 or opt_img[goal[1], goal[0]] == 1:
    print("Not valid entries:")
    solvable = False
else:
    solvable = True

class Node:
    def __init__(self, position, cost, parent): 
        self.position = position
        self.cost = cost
        self.parent = parent

def explore(node):
    i, j = node.position
    directions = [(i, j + 1, 1), (i + 1, j, 1), (i - 1, j, 1), (i, j - 1, 1), 
                  (i + 1, j + 1, 1.4), (i - 1, j - 1, 1.4), 
                  (i - 1, j + 1, 1.4), (i + 1, j - 1, 1.4)]
    valid_paths = [(pos[:2], pos[2]) for pos in directions if 0 <= pos[0] < width and 0 <= pos[1] < height and opt_img[pos[1], pos[0]] == 0]
    return valid_paths

q = PriorityQueue()
visited = set()
node_objects = {}
total_points = {(i, j): math.inf for i in range(width) for j in range(height)}
total_points[start] = 0

node = Node(start, 0, None)
node_objects[start] = node
q.put((node.cost, node.position))

opt_img_show = np.dstack([opt_img.copy()*255, opt_img.copy()*255, opt_img.copy()*255])

fourcc = cv2.VideoWriter_fourcc(*'mp4v')  
frame_rate = 10  
frame_size = (width, height)
video_writer = cv2.VideoWriter('path_finding_video.mp4', fourcc, frame_rate, frame_size)

if solvable:
    while not q.empty():
        current_cost, current_pos = q.get()
        if current_pos == goal:
            print("Reached goal")
            break

        if current_pos in visited:
            continue

        visited.add(current_pos)
        current_node = node_objects[current_pos]

        for next_pos, cost in explore(current_node):
            next_cost = current_cost + cost
            if next_pos not in visited or next_cost < total_points[next_pos]:
                total_points[next_pos] = next_cost
                next_node = Node(next_pos, next_cost, current_node)
                node_objects[next_pos] = next_node
                q.put((next_cost, next_pos))
                opt_img_show[next_pos[1], next_pos[0]] = [0, 0, 255]

path_pos = goal
while path_pos != start:
    opt_img_show[path_pos[1], path_pos[0]] = [0, 255, 0] 
    path_pos = node_objects[path_pos].parent.position
    

video_writer.write(opt_img_show.astype('uint8'))  
video_writer.release()
