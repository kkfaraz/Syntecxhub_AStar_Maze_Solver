<img width="400" height="400" alt="demo" src="https://github.com/user-attachments/assets/282487b5-1cd5-4606-912d-961a32dbd99f" />
# Syntecxhub_AStar_Maze_Solver
Interactive A* Maze Solver Game with real-time visualization, dual heuristics, terminal analytics, and Matplotlib-based final path rendering.

# 🎮 A* Maze Solver Game (Syntecxhub Internship Project)

An interactive desktop application that visualizes the A* (A-Star) pathfinding algorithm in real time using a grid-based maze.

## 🚀 Features

- Interactive maze creation (start, goal, walls)
- Real-time A* search visualization
- Dual heuristic support:
  - Manhattan Distance
  - Euclidean Distance
- Terminal output:
  - Path length
  - Nodes explored
  - Execution time
  - Path coordinates
- Popup visualization (Matplotlib)
- Random maze generator
- Smooth animation using Pygame

---

## 🎮 Controls

| Action | Key |
|------|-----|
| Set Start | S + Click |
| Set Goal | G + Click |
| Draw Walls | Left Click |
| Run Algorithm | SPACE |
| Reset Grid | R |
| Clear Walls | C |
| Toggle Heuristic | H |
| Random Maze | M |

---

## 🖥️ Tech Stack

- Python
- Pygame
- Matplotlib

---

Syntecxhub_AStar_Maze_Solver/
│
├── main.py              # Game loop + Pygame UI
├── astar.py             # A* algorithm
├── grid.py              # Grid + Node logic
├── visualize.py         # Matplotlib popup visualization
├── settings.py          # Colors, constants
│
├── assets/              # (optional: icons, fonts)
│
├── README.md            # Documentation (VERY IMPORTANT)
├── requirements.txt     # Dependencies
├── .gitignore
└── demo.gif             # Gameplay preview (optional but powerful)

## ▶️ How to Run

```bash
pip install -r requirements.txt
python main.py

