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
            opt_img[y,x] = 1
        if (270<x<355) and (0<y<405):
            opt_img[y,x] = 1
        hexagon_vertices = np.array([[(650,400),(725,325),(725,175),(650,100),(575,175),(575,325)]], dtype=np.int32)
        cv2.fillPoly(opt_img, hexagon_vertices, 1)
        if (895<x<1105) and (45<y<455):
            opt_img[y,x]=1
        if(895<x<1020) and (125<y<375):
            opt_img[y,x]=0
        if (y>=0 and y<=5) or (y<=500 and y>=495) or (x>=0 and x<=5) or (x<=1200 and x>=1195):
            opt_img[y,x] = 1
       
        

start = tuple(map(int, input("Enter start coordinates (x, y) separated by ,: ").split(",")))
goal = tuple(map(int, input("Enter goal coordinates (x, y) separated by ,: ").split(",")))

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
    directions = [(i,j+1,1),(i+1,j,1),(i-1,j,1),(i,j-1,1), (i+1,j+1,1.4),(i-1,j-1,1.4), (i-1,j+1,1.4),(i+1,j-1,1.4)]
    valid_paths = [(pos[:2], pos[2]) for pos in directions if 0 <= pos[0] < width and 0 <= pos[1] < height and opt_img[pos[1], pos[0]] == 0]
    return valid_paths

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
frame_rate = 40
video_writer = cv2.VideoWriter('path_finding_video.mp4', fourcc, frame_rate, (width, height))


solvable = True  
if solvable:
    write_frequency = 50  
    node_count = 0
    opt_img_show = np.zeros((height, width, 3), dtype=np.uint8) 

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
                
                flipped_y = height - 1 - next_pos[1] 
                opt_img_show[flipped_y, next_pos[0], :] = [0, 0, 255] 
                
                node_count += 1
                if node_count % write_frequency == 0:
                    video_writer.write(opt_img_show.astype('uint8')) 
    path = []
    current_pos = goal
    while current_pos != start:
        path.append(current_pos)
        current_node = node_objects[current_pos]
        current_pos = current_node.parent.position if current_node.parent else None
    path.reverse() 
    for position in path:
        flipped_y = height - 1 - position[1] 
        opt_img_show[flipped_y, position[0], :] = [0, 255, 0] 
    video_writer.write(opt_img_show.astype('uint8'))  

video_writer.release()



cv2.imshow('Path Finding Final', opt_img_show)
cv2.waitKey(0)
cv2.destroyAllWindows()
