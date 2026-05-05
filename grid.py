"""
grid.py - Grid and Node representations, and random maze generation
"""

import pygame
import random
from settings import *

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = col * width
        self.y = row * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == YELLOW

    def is_open(self):
        return self.color == LIGHT_BLUE

    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN

    def is_goal(self):
        return self.color == RED

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = GREEN

    def make_closed(self):
        self.color = YELLOW

    def make_open(self):
        self.color = LIGHT_BLUE

    def make_wall(self):
        self.color = BLACK

    def make_goal(self):
        self.color = RED

    def make_path(self):
        self.color = PURPLE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Down
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
        # Up
        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():
            self.neighbors.append(grid[self.row - 1][self.col])
        # Right
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
        # Left
        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False


def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid

def draw_grid_lines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid_lines(win, rows, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    # Ensure indices are within bounds
    if row >= rows: row = rows - 1
    if col >= rows: col = rows - 1

    return row, col

def generate_random_maze(grid, rows):
    """
    Generates a random maze using Recursive Backtracking.
    Modifies the grid in place. Start and Goal states are not managed here.
    """
    # 1. Fill entire grid with walls
    for row in grid:
        for node in row:
            node.make_wall()

    def get_carvable_neighbors(node):
        neighbors = []
        r, c = node.get_pos()
        # Directions: Down, Up, Right, Left
        # We look 2 steps ahead to maintain walls between paths
        if r < rows - 2 and grid[r+2][c].is_wall():
            neighbors.append((grid[r+2][c], grid[r+1][c]))
        if r > 1 and grid[r-2][c].is_wall():
            neighbors.append((grid[r-2][c], grid[r-1][c]))
        if c < rows - 2 and grid[r][c+2].is_wall():
            neighbors.append((grid[r][c+2], grid[r][c+1]))
        if c > 1 and grid[r][c-2].is_wall():
            neighbors.append((grid[r][c-2], grid[r][c-1]))
        return neighbors

    # Choose a random odd starting point
    start_r = random.randrange(1, rows-1, 2)
    start_c = random.randrange(1, rows-1, 2)
    start_node = grid[start_r][start_c]
    start_node.reset()

    stack = [start_node]

    while stack:
        current = stack[-1]
        neighbors = get_carvable_neighbors(current)

        if neighbors:
            # Choose a random neighbor to carve
            next_node, wall_to_remove = random.choice(neighbors)
            wall_to_remove.reset()
            next_node.reset()
            stack.append(next_node)
        else:
            # Backtrack
            stack.pop()

    # Sometimes the edges remain as walls, which is generally good for mazes.
    # Return grid as-is, the main loop will need to ensure Start/Goal are accessible.
