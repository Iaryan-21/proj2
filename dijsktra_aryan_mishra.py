"""
    @Author: Aryan Mishra
    @Date: 2021-10-10
    ENPM661 - Planning for Autonomous Robots
    Assignment 3
"""




import math                                                                                 #importing math library
import numpy as np                                                                          #importing numpy library
from queue import PriorityQueue                                                             #importing PriorityQueue from queue
import cv2                                                                                  #importing cv2 library
import time                                                                                 #importing time library

height = 500                                                                                #height of the image
width = 1200                                                                                #width of the image
opt_img = np.zeros((height, width), np.uint8)                                               #creating a black image of size 500x1200


for x in range(width):                                                                     #iterating through the width of the image
    for y in range(height):                                                                #iterating through the height of the image
        if (95<x<175) and (95<y<500):                                                      #creating a rectangle 
            opt_img[y,x] = 1
        if (270<x<355) and (0<y<405):
            opt_img[y,x] = 1
        hexagon_vertices = np.array([[(650,400),(725,325),(725,175),(650,100),(575,175),(575,325)]], dtype=np.int32) #creating a hexagon
        cv2.fillPoly(opt_img, hexagon_vertices, 1)
        if (895<x<1105) and (45<y<455):                                                    #creating part of concave rectangle
            opt_img[y,x]=1
        if(895<x<1020) and (125<y<375):                                                    #creating part of concave rectangle
            opt_img[y,x]=0
        if (y>=0 and y<=5) or (y<=500 and y>=495) or (x>=0 and x<=5) or (x<=1200 and x>=1195): #creating the boundary where th robot cannot go due to 5mm clearnece
            opt_img[y,x] = 1
       
        

start = tuple(map(int, input("Enter start coordinates (x,y) separated by ,:").split(","))) #taking the start coordinates from the user
goal = tuple(map(int, input("Enter goal coordinates (x,y) separated by ,:").split(",")))   #taking the goal coordinates from the user

if opt_img[start[1], start[0]] == 1 or opt_img[goal[1], goal[0]] == 1:                       #checking if the start and goal coordinates are valid
    print("Not valid entries:")                                                              #if not valid then print not valid entries
    solvable = False                                                                         #setting solvable to False
else:
    solvable = True                                                                          #else set solvable to True

class Node:
    def __init__(self, position, cost, parent):                                              #creating a class Node
        self.position = position                                                             #initializing the position
        self.cost = cost                                                                     #initializing the cost
        self.parent = parent                                                                 #initializing the parent

def explore(node):
    i, j = node.position
    directions = [(i,j+1,1),(i+1,j,1),(i-1,j,1),(i,j-1,1), (i+1,j+1,1.4),(i-1,j-1,1.4), (i-1,j+1,1.4),(i+1,j-1,1.4)]                                     #exploring the nodes
    valid_paths = [(pos[:2], pos[2]) for pos in directions if 0 <= pos[0] < width and 0 <= pos[1] < height and opt_img[pos[1], pos[0]] == 0]             #checking for valid paths
    return valid_paths                                                                                                                                   #returning the valid paths



q = PriorityQueue()                                                                             #creating a priority queue
visited = set()                                                                                 #creating a set for visited nodes
node_objects = {}                                                                               #creating a dictionary for the node objects
total_points = {(i, j): float('inf') for i in range(width) for j in range(height)}              #creating a dictionary for the total points

total_points[start] = 0                                                                         #setting the total points of the start to 0
node_objects[start] = Node(start, 0, None)                                                      #creating the start node
q.put((0, start))                                                                               #putting the start in the queue                                                                   

fourcc = cv2.VideoWriter_fourcc(*'mp4v')                                                         #creating a video writer object
frame_rate = 40                                                                                  #setting the frame rate
video_writer = cv2.VideoWriter('path_finding_video.mp4', fourcc, frame_rate, (width, height))    #creating a video file


solvable = True                                                                            #setting solvable to True
if solvable:
    write_frequency = 50                                                                   #setting the write frequency
    node_count = 0                                                                         #setting the node count to 0
    opt_img_show = np.zeros((height, width, 3), dtype=np.uint8)                            #creating a black image of size 500x1200

    while not q.empty():                                                                   #iterating through the queue
        current_cost, current_pos = q.get()                                                #getting the current cost and current position
        if current_pos == goal:                                                            #checking if the current position is the goal
            print("Reached goal")                                                       
            break
        if current_pos in visited:                                                         #checking if the current position is visited
            continue                                                                       
        visited.add(current_pos)                                                           #adding the current position to the visited set
        current_node = node_objects[current_pos]                                           #getting the current node

        for next_pos, cost in explore(current_node):                                       #iterating through the next position and cost
            next_cost = current_cost + cost                                                #calculating the next cost
            if next_pos not in visited or next_cost < total_points[next_pos]:              #checking if the next position is not visited or the next cost is less than the total points
                total_points[next_pos] = next_cost                                         #setting the total points to the next cost
                next_node = Node(next_pos, next_cost, current_node)                        #creating the next node
                node_objects[next_pos] = next_node                                         #setting the next node to the next position
                q.put((next_cost, next_pos))                                               #putting the next cost and next position in the queue
                
                flipped_y = height - 1 - next_pos[1]                                       
                opt_img_show[flipped_y, next_pos[0], :] = [0, 0, 255]                      #setting the color of the next position to red
                
                node_count += 1                                                           #incrementing the node count
                if node_count % write_frequency == 0:                                     #checking if the node count is divisible by the write frequency
                    video_writer.write(opt_img_show.astype('uint8'))                      #writing the image to the video file
    path = []                                                                             #creating an empty list
    current_pos = goal
    while current_pos != start:                                                           #iterating through the current position and start                                         
        path.append(current_pos)                                                          #appending the current position to the path
        current_node = node_objects[current_pos]                                          #getting the current node
        current_pos = current_node.parent.position if current_node.parent else None       
    path.reverse() 
    for position in path:                                                                 #iterating through the path
        flipped_y = height - 1 - position[1]                                              
        opt_img_show[flipped_y, position[0], :] = [0, 255, 0]                            #setting the color of the position to green
    video_writer.write(opt_img_show.astype('uint8'))                                     #writing the image to the video file

video_writer.release()



cv2.imshow('Path Finding Final', opt_img_show)                                            #displaying the final image
cv2.waitKey(0)
cv2.destroyAllWindows()
