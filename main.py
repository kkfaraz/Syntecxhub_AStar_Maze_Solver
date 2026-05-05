"""
main.py - Entry point for the A* Maze Solver Game
"""

import pygame
import sys
from settings import *
from grid import make_grid, draw, get_clicked_pos, generate_random_maze
from astar import astar_search
from visualize import show_final_path

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("A* Maze Solver Game with Dual Output Visualization")

def main():
    grid = make_grid(ROWS, WIDTH)
    
    start = None
    goal = None
    
    run = True
    heuristic = "manhattan"
    clock = pygame.time.Clock()
    
    print("Welcome to the A* Maze Solver!")
    print("--------------------------------")
    print("Controls:")
    print(" - Left Click: Draw walls")
    print(" - Right Click: Erase")
    print(" - S + Left Click: Set Start")
    print(" - G + Left Click: Set Goal")
    print(" - SPACE: Run A* Search")
    print(" - R: Reset completely")
    print(" - C: Clear walls and paths (keeps Start/Goal)")
    print(" - H: Toggle Heuristic")
    print(" - M: Generate Random Maze")
    print("--------------------------------\n")

    while run:
        clock.tick(FPS)
        draw(WIN, grid, ROWS, WIDTH)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            keys = pygame.key.get_pressed()
                
            if pygame.mouse.get_pressed()[0]: # Left Click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                
                if keys[pygame.K_s]:
                    if start:
                        start.reset()
                    start = node
                    start.make_start()
                    if start == goal:
                        goal = None
                elif keys[pygame.K_g]:
                    if goal:
                        goal.reset()
                    goal = node
                    goal.make_goal()
                    if goal == start:
                        start = None
                else:
                    if node != start and node != goal:
                        node.make_wall()
                        
            elif pygame.mouse.get_pressed()[2]: # Right Click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, WIDTH)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == goal:
                    goal = None
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and goal:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    # Run A*
                    result = astar_search(lambda: draw(WIN, grid, ROWS, WIDTH), grid, start, goal, heuristic)
                    
                    if result and result.get("reason") == "quit":
                        run = False
                        break

                    # Terminal Output
                    print("\n--- A* Search Results ---")
                    if result.get("found"):
                        print("Path Found!")
                        print(f"Length: {result.get('path_length')}")
                        print(f"Nodes Explored: {result.get('nodes_explored')}")
                        print(f"Execution Time: {result.get('execution_time'):.4f} seconds")
                        print(f"Path: {result.get('path')}")
                        
                        # Show popup
                        show_final_path(grid, ROWS, start, goal, result.get("path"))
                    else:
                        print("No Path Found!")
                        print(f"Nodes Explored: {result.get('nodes_explored')}")
                        print(f"Execution Time: {result.get('execution_time'):.4f} seconds")
                        
                        show_final_path(grid, ROWS, start, goal, None)
                        
                if event.key == pygame.K_c:
                    for row in grid:
                        for node in row:
                            if node != start and node != goal:
                                node.reset()
                                
                if event.key == pygame.K_r:
                    start = None
                    goal = None
                    grid = make_grid(ROWS, WIDTH)
                    
                if event.key == pygame.K_m:
                    generate_random_maze(grid, ROWS)
                    start = None
                    goal = None
                    
                if event.key == pygame.K_h:
                    if heuristic == "manhattan":
                        heuristic = "euclidean"
                    else:
                        heuristic = "manhattan"
                    print(f"Heuristic switched to: {heuristic}")

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
