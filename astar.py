# A Star path planning
# Copyright (c) 2022 Rishabh Mukund
# MIT License
#
# Description: Using A star algorith to find the optimum path from staring
# to goal poisiton

import heapq as heap
import numpy as np
import cv2


def getAdjNodes(curr_node, validPoints, clearance):
    """
    Definition
    ---
    Method to generate all adjacent nodes for a given node

    Parameters
    ---
    curr_node : node of intrest
    validPoints : list of all valid points
    clearance : minimum distance required from obstacles

    Returns
    ---
    adjNodes : list of adjacent nodes with cost from parent node
    """
    adjNodes = []
    moves = [-60, -30, 0, 30, 60]
    # flag = True
    for move in moves:
        # Checking if the point is valid
        angle = curr_node[-1] + move
        x = int(curr_node[0] + 5 * np.cos(np.radians(angle)))
        y = int(curr_node[1] + 5 * np.sin(np.radians(angle)))
        if (x, y) in validPoints:
            adjNodes.append(((x, y, angle), 5))
            # Checking for clearance
            # for i in range(clearance):
            #     if not (curr_node[0] + move[0] + (i * move[0]), curr_node[1]
            #             + move[1] + (i * move[1])) in validPoints:
            #         flag = False
            #         break
            #     if not flag:
            #         break
            # if flag:
    return adjNodes


def updateNode(new_node, curr_node, node_cost, queue, parent_map, cost, goal):
    """
    Definition
    ---
    Method to update nodes based on cost and closed list of nodes

    Parameters
    ---
    new_node : node of intrest
    curr_node : parent node
    node_cost : dict of all nodes mapped to costs
    queue : priority queue of nodes to check
    parent_map : dict of nodes mapped to parent node_cost
    cost : cost to get to new node from parent node
    goal : goal node

    Returns
    ---
    Reached : if new_node is goal node returns True othervise returns False
    node_cost : dict of all nodes mapped to costs
    queue : priority queue of nodes to check
    parent_map : dict of nodes mapped to parent node_cost
    """
    dist = abs(np.linalg.norm(np.asarray(
        new_node[0:2]) - np.asarray(goal[0:2])))
    new_cost = node_cost[curr_node] + cost + dist
    temp_cost = node_cost.get(new_node)
    if not temp_cost or (temp_cost > new_cost):
        node_cost[new_node] = new_cost
        parent_map[new_node[0:2]] = curr_node[0:2]
        heap.heappush(queue, (new_cost, new_node))
    if abs(np.linalg.norm(np.asarray(goal[0:2])
                          - np.asarray(new_node[0:2]))) < 2.5:
        return True, node_cost, queue, parent_map
    return False, node_cost, queue, parent_map


def astar(start, goal, validPoints, clearance):
    """
    Definition
    ---
    Method to get least cost path from starting to goal node using dijkstra's

    Parameters
    ---
    start : starting node
    goal : goal node
    validPoints : list of all valid points
    clearance : minimum distance required from obstacles

    Returns
    ---
    Reached : if path is found True othervise False
    parent_map : dict of nodes mapped to parent node_cost
    closed : list of all the explored nodes
    """
    closed = []
    queue = []
    node_cost = {}
    parent_map = {}
    reached = False

    node_cost[start] = 0
    heap.heappush(queue, (0, start))

    if abs(np.linalg.norm(np.asarray(goal[0:2])-np.asarray(start[0:2]))) < 2.5:
        reached = True
        parent_map[goal[0:2]] = start[0:2]

    while not reached and queue:
        curr_cost, curr_node = heap.heappop(queue)
        closed.append(curr_node[0:2])
        adjNodes = getAdjNodes(curr_node, validPoints, clearance)
        for new_node, cost in adjNodes:
            if new_node[0:2] in closed:
                continue
            print('checking for node: ', new_node)
            flag, node_cost, queue, parent_map = updateNode(
                new_node, curr_node, node_cost, queue, parent_map, cost, goal)
            if flag:
                reached = True
                break
    return reached, parent_map, closed


def getPath(parent_map, start, goal):
    """
    Definition
    ---
    Method to generate path using backtracking

    Parameters
    ---
    parent_map : dict of nodes mapped to parent node_cost
    start : starting node
    goal : goal node

    Returns
    ---
    path: list of all the points from starting to goal position
    """
    curr_node = goal[0:2]
    parent_node = parent_map[goal[0:2]]
    path = [curr_node]
    while not parent_node == start[0:2]:
        curr_node = parent_node
        parent_node = parent_map[curr_node]
        path.append(curr_node)
    path.append(start[0:2])
    return path[::-1]


def animate(map_len, map_bre, validPoints, closed, path, parent_map):
    """
    Definition
    ---
    Method to animate the nodes explored by dijkstra's algorithm and plot the
    best path

    Parameters
    ---
    map_len : length of map
    map_bre : breadth of map
    validPoints : list of all valid points
    closed : list of all the explored nodes
    path: list of all the points from starting to goal position
    """
    map_frame = np.zeros((map_bre + 1, map_len + 1, 3))
    resize = (800, 500)
    for point in validPoints:
        map_frame[map_bre - point[1], point[0]] = [255, 255, 255]
    for point in closed:
        map_frame[map_bre - point[1], point[0]] = [0, 127, 0]
        if(point[0:2] == (50, 20)):
            continue
        cv2.imshow('map_frame', cv2.resize(map_frame, resize))
        cv2.waitKey(1)
    for point in path:
        map_frame[map_bre - point[1], point[0]] = [0, 0, 127]
        cv2.imshow('map_frame', cv2.resize(map_frame, resize))
        cv2.waitKey(1)
    cv2.waitKey(0)


if __name__ == '__main__':
    map_len = 400
    map_bre = 250
    clearance = 5

    validPoints = []

    for i in range(map_len):
        for j in range(map_bre):
            validPoints.append((i, j))

    start = 50, 20, 0
    goal = 150, 100, 0

    reached, parent_map, closed = astar(start, goal, validPoints, clearance)
    if reached:
        print('reached')
        path = getPath(parent_map, start, goal)
        print(path)
        animate(map_len, map_bre, validPoints, closed, path, parent_map)
    else:
        print('lol')