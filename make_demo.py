import os
os.environ["SDL_VIDEODRIVER"] = "dummy"

import pygame
import imageio
import numpy as np

# Adjust imports from local files
from settings import *
from grid import make_grid, draw, generate_random_maze, Node
from astar import astar_search

def make_demo_gif(filename="demo.gif"):
    pygame.init()
    
    # Use smaller dimensions for GIF
    WIDTH = 400
    ROWS = 20
    
    win = pygame.display.set_mode((WIDTH, WIDTH))
    
    grid = make_grid(ROWS, WIDTH)
    
    # Build a sample solvable maze manually
    # 0 = empty, 1 = wall
    maze_layout = [
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1],
        [0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0],
        [0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0],
    ]
    
    for r in range(ROWS):
        for c in range(ROWS):
            if maze_layout[r][c] == 1:
                grid[r][c].make_wall()
                
    start = grid[0][0]
    start.make_start()
    goal = grid[19][19]
    goal.make_goal()

    for row in grid:
        for node in row:
            node.update_neighbors(grid)

    writer = imageio.get_writer(filename, mode='I', fps=30)
    
    frame_counter = 0
    def draw_capture():
        nonlocal frame_counter
        # Only capture every 3rd frame to speed up gif and reduce size
        frame_counter += 1
        
        draw(win, grid, ROWS, WIDTH)
        
        if frame_counter % 3 == 0:
            # Capture surface
            # array3d is (width, height, 3). transpose to (height, width, 3)
            array = pygame.surfarray.array3d(win)
            array = np.transpose(array, (1, 0, 2))
            writer.append_data(array)
            
    # Draw initial state and capture some frames to show start state
    for _ in range(30):
        draw(win, grid, ROWS, WIDTH)
        array = pygame.surfarray.array3d(win)
        array = np.transpose(array, (1, 0, 2))
        writer.append_data(array)

    # Run A* and record
    result = astar_search(draw_capture, grid, start, goal, "manhattan")
    
    # Capture final result for a couple seconds
    for _ in range(60):
        draw(win, grid, ROWS, WIDTH)
        array = pygame.surfarray.array3d(win)
        array = np.transpose(array, (1, 0, 2))
        writer.append_data(array)
        
    writer.close()
    pygame.quit()
    print(f"Successfully generated {filename}")

if __name__ == "__main__":
    make_demo_gif()
