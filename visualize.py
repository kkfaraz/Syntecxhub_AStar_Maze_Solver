"""
visualize.py - Matplotlib visualization for the final path
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import ListedColormap
import numpy as np

def show_final_path(grid, rows, start, goal, path):
    """
    Displays a matplotlib popup window showing the final grid and path.
    """
    # 0: Empty, 1: Wall, 2: Start, 3: Goal, 4: Path
    color_matrix = np.zeros((rows, rows), dtype=int)
    
    # Fill walls
    for row in grid:
        for node in row:
            if node.is_wall():
                color_matrix[node.row][node.col] = 1

    # Fill path
    if path:
        for (r, c) in path:
            color_matrix[r][c] = 4

    # Fill Start and Goal
    if start:
        color_matrix[start.row][start.col] = 2
    if goal:
        color_matrix[goal.row][goal.col] = 3

    # Define Colormap: White, Black, Green, Red, Purple
    colors = ['#ffffff', '#000000', '#00ff00', '#ff0000', '#800080']
    cmap = ListedColormap(colors)

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(color_matrix, cmap=cmap, vmin=0, vmax=4)

    # Gridlines
    ax.set_xticks(np.arange(-0.5, rows, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
    ax.grid(which="minor", color="gray", linestyle='-', linewidth=0.5)
    ax.tick_params(which="minor", size=0)

    # Remove ticks/labels
    ax.set_xticks([])
    ax.set_yticks([])

    ax.set_title("Final Path Visualization")

    # Legend
    legend_elements = [
        mpatches.Patch(color='#ffffff', label='Empty', ec='black'),
        mpatches.Patch(color='#000000', label='Wall'),
        mpatches.Patch(color='#00ff00', label='Start'),
        mpatches.Patch(color='#ff0000', label='Goal'),
        mpatches.Patch(color='#800080', label='Path')
    ]
    ax.legend(handles=legend_elements, loc='upper left', bbox_to_anchor=(1.05, 1))
    
    plt.tight_layout()
    plt.show()
