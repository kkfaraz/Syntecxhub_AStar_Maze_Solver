"""
astar.py - A* algorithm implementation adapted for Pygame real-time visualization
"""

import pygame
import heapq
import time
import math

def h_manhattan(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def h_euclidean(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.sqrt((x1 - x2)**2 + (y1 - y2)**2)

def reconstruct_path(came_from, current, draw_func):
    path = []
    while current in came_from:
        current = came_from[current]
        path.append(current.get_pos())
        current.make_path()
        draw_func()
    # The list is from goal to start. We reverse it to be start to goal.
    path.reverse()
    return path

def astar_search(draw_func, grid, start, goal, heuristic_type="manhattan"):
    """
    Executes A* search.
    draw_func: callback to update Pygame display
    """
    start_time = time.time()
    
    # Select heuristic
    if heuristic_type == "euclidean":
        h = h_euclidean
    else:
        h = h_manhattan

    count = 0
    open_set = []
    heapq.heappush(open_set, (0, count, start))
    came_from = {}
    
    # g_score: shortest distance from start node to current node
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0
    
    # f_score: predicted distance from start to goal via current node (g + h)
    f_score = {node: float("inf") for row in grid for node in row}
    f_score[start] = h(start.get_pos(), goal.get_pos())

    # Keep track of items in the priority queue for O(1) lookups
    open_set_hash = {start}

    nodes_explored = 0

    while open_set:
        # Check for quit events to not freeze the game window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return {"found": False, "reason": "quit"}

        current = heapq.heappop(open_set)[2]
        open_set_hash.remove(current)

        if current == goal:
            path_nodes = reconstruct_path(came_from, goal, draw_func)
            end_time = time.time()
            # Also append the goal to the path list for completeness
            path_nodes.append(goal.get_pos())
            
            # Make sure start and goal colors remain explicitly clear
            start.make_start()
            goal.make_goal()
            draw_func()
            
            return {
                "found": True,
                "path": path_nodes,
                "path_length": len(path_nodes) - 1, # edges
                "nodes_explored": nodes_explored,
                "execution_time": end_time - start_time
            }

        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), goal.get_pos())
                
                if neighbor not in open_set_hash:
                    count += 1
                    heapq.heappush(open_set, (f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if neighbor != goal:
                        neighbor.make_open()

        draw_func()

        if current != start:
            current.make_closed()
        
        nodes_explored += 1

    end_time = time.time()
    return {
        "found": False,
        "nodes_explored": nodes_explored,
        "execution_time": end_time - start_time
    }
