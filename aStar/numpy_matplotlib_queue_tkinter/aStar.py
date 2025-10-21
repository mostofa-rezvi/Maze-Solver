import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
from queue import PriorityQueue
import random

DIRECTIONS = {
    0: (-1, 0),
    1: (0, 1),
    2: (1, 0),
    3: (0, -1),
}

TURN_MAP = {
    (0, "R"): 1,
    (0, "L"): 3,
    (1, "R"): 2,
    (1, "L"): 0,
    (2, "R"): 3,
    (2, "L"): 1,
    (3, "R"): 0,
    (3, "L"): 2,
}


# Heuristic function
def h_euclidean(cell1_pos, cell2_pos):
    x1, y1 = cell1_pos
    x2, y2 = cell2_pos
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class RandomMazeGenerator:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        # Initialize grid with all walls (1)
        self.grid = np.ones((self.rows, self.cols), dtype=int)

    # Generates a maze using Randomized DFS algorithm.
    def generate(self, start_r=None, start_c=None):

        if start_r is None:
            start_r = random.randint(0, self.rows - 1)
        if start_c is None:
            start_c = random.randint(0, self.cols - 1)

        stack = [(start_r, start_c)]
        visited = set()
        visited.add((start_r, start_c))
        self.grid[start_r][start_c] = 0

        while stack:
            current_r, current_c = stack[-1]
            unvisited_neighbors = []

            # Check 4 directions for neighbors that are 2 steps away (to ensure walls in between)
            for dr, dc in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
                nr, nc = current_r + dr, current_c + dc
                if (
                    0 <= nr < self.rows
                    and 0 <= nc < self.cols
                    and (nr, nc) not in visited
                ):
                    unvisited_neighbors.append(
                        ((nr, nc), (current_r + dr // 2, current_c + dc // 2))
                    )

            if unvisited_neighbors:
                (next_r, next_c), (wall_r, wall_c) = random.choice(unvisited_neighbors)

                self.grid[wall_r][wall_c] = 0
                self.grid[next_r][next_c] = 0
                visited.add((next_r, next_c))
                stack.append((next_r, next_c))
            else:
                stack.pop()

        return self.grid


class MazeSolver:
    def __init__(self, maze_grid, start_pos, end_pos, start_dir=0):
        self.maze_grid = maze_grid
        self.rows = len(maze_grid)
        self.cols = len(maze_grid[0])
        self.start_pos = start_pos
        self.end_pos = end_pos

        # Start direction: Default to North (0)
        self.start_node = (self.start_pos, start_dir)

    def is_valid_move(self, r, c):
        """Checks if a cell is within bounds and not a wall."""
        return 0 <= r < self.rows and 0 <= c < self.cols and self.maze_grid[r][c] == 0

    def get_neighbors(self, current_node):
        (r, c), current_direction = current_node
        neighbors = []

        # 1. Move Forward
        dr_f, dc_f = DIRECTIONS[current_direction]
        next_r_f, next_c_f = r + dr_f, c + dc_f
        if self.is_valid_move(next_r_f, next_c_f):
            next_full_node = ((next_r_f, next_c_f), current_direction)
            neighbors.append((next_full_node, "Move Forward"))

        # 2. Turn Right and Move Forward
        new_direction_r = TURN_MAP.get((current_direction, "R"))
        if new_direction_r is not None:
            dr_r, dc_r = DIRECTIONS[new_direction_r]
            next_r_r, next_c_r = r + dr_r, c + dc_r
            if self.is_valid_move(next_r_r, next_c_r):
                next_full_node = ((next_r_r, next_c_r), new_direction_r)
                neighbors.append((next_full_node, "Turn Right + Move Forward"))

        # 3. Turn Left and Move Forward
        new_direction_l = TURN_MAP.get((current_direction, "L"))
        if new_direction_l is not None:
            dr_l, dc_l = DIRECTIONS[new_direction_l]
            next_r_l, next_c_l = r + dr_l, c + dc_l
            if self.is_valid_move(next_r_l, next_c_l):
                next_full_node = ((next_r_l, next_c_l), new_direction_l)
                neighbors.append((next_full_node, "Turn Left + Move Forward"))

        return neighbors

    def solve_maze_a_star(self):

        open_set = PriorityQueue()
        open_set.put((0, self.start_node))  # (f_score, node)

        came_from = {}

        # Initialize g_score and f_score for all the possible direction nodes
        g_score = {
            ((r, c), d): float("inf")
            for r in range(self.rows)
            for c in range(self.cols)
            for d in DIRECTIONS.keys()
        }
        f_score = {
            ((r, c), d): float("inf")
            for r in range(self.rows)
            for c in range(self.cols)
            for d in DIRECTIONS.keys()
        }

        g_score[self.start_node] = 0
        f_score[self.start_node] = h_euclidean(self.start_pos, self.end_pos)

        while not open_set.empty():
            current_f, current_node = open_set.get()
            current_pos, current_dir = current_node

            if current_pos == self.end_pos:
                path = []
                current_path_node = current_node
                while current_path_node != self.start_node:
                    path.append(current_path_node[0])
                    current_path_node = came_from[current_path_node]
                path.append(self.start_node[0])
                return path[::-1]

            for next_full_node, action_desc in self.get_neighbors(current_node):
                next_pos, next_direction = next_full_node

                tentative_g_score = g_score[current_node] + 1

                if tentative_g_score < g_score[next_full_node]:
                    came_from[next_full_node] = current_node
                    g_score[next_full_node] = tentative_g_score
                    f_score[next_full_node] = tentative_g_score + h_euclidean(
                        next_pos, self.end_pos
                    )
                    open_set.put((f_score[next_full_node], next_full_node))

        return None


class MazeApp:
    def __init__(self, master):
        self.master = master
        master.title("Modern A* Maze Solver")

        self.rows = 21
        self.cols = 21
        self.maze_grid = None
        self.path = None
        self.start_pos = None
        self.end_pos = None

        self.fig, self.ax = plt.subplots(
            figsize=(6, 6), facecolor="#333333"
        )  # Darker background
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

        self.button_frame = tk.Frame(master, bg="#000000")
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.generate_button = tk.Button(
            self.button_frame,
            text="Generate New Maze",
            command=self.generate_and_plot_maze,
            font=("Arial", 12, "bold"),
            bg="#6A5ACD",
            fg="white",
            relief=tk.RAISED,
            bd=3,
        )
        self.generate_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.solve_button = tk.Button(
            self.button_frame,
            text="Solve Maze",
            command=self.solve_and_plot_path,
            font=("Arial", 12, "bold"),
            bg="#20B2AA",
            fg="white",
            relief=tk.RAISED,
            bd=3,
        )
        self.solve_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.clear_button = tk.Button(
            self.button_frame,
            text="Clear Path",
            command=self.clear_path,
            font=("Arial", 12, "bold"),
            bg="#DC143C",
            fg="white",
            relief=tk.RAISED,
            bd=3,
        )
        self.clear_button.pack(side=tk.LEFT, padx=10, pady=10, expand=True)

        self.generate_and_plot_maze()

    def generate_and_plot_maze(self):
        generator = RandomMazeGenerator(self.rows, self.cols)
        self.maze_grid = generator.generate()
        self.path = None

        walkable_cells = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self.maze_grid[r][c] == 0
        ]

        if len(walkable_cells) < 2:
            messagebox.showerror(
                "Error", "Maze too small or no walkable path to place start/end."
            )
            return

        self.start_pos = random.choice(walkable_cells)

        self.end_pos = random.choice(walkable_cells)
        while self.end_pos == self.start_pos:
            self.end_pos = random.choice(walkable_cells)

        self.plot_maze()

    def plot_maze(self):
        self.ax.clear()

        cmap = plt.cm.colors.ListedColormap(["#EEEEEE", "#333333"])
        bounds = [-0.5, 0.5, 1.5]
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

        self.ax.imshow(
            self.maze_grid,
            cmap=cmap,
            norm=norm,
            origin="upper",
            extent=[-0.5, self.cols - 0.5, self.rows - 0.5, -0.5],
            interpolation="nearest",
        )

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        self.ax.plot(
            self.start_pos[1],
            self.start_pos[0],
            marker=">",
            markersize=12,
            color="#11005036",
            label="Start",
            markeredgewidth=1.5,
            markeredgecolor="black",
        )
        self.ax.plot(
            self.end_pos[1],
            self.end_pos[0],
            marker="X",
            markersize=12,
            color="#00FFFF",
            label="End",
            markeredgewidth=1.1,
            markeredgecolor="black",
        )

        if self.path:
            path_rows = [p[0] for p in self.path]
            path_cols = [p[1] for p in self.path]
            self.ax.plot(
                path_cols,
                path_rows,
                color="#FF4500",  # Orange-red path
                linewidth=4,
                alpha=0.8,
                solid_capstyle="round",
            )
            self.ax.plot(
                path_cols,
                path_rows,
                "o",
                markersize=4,
                color="#FF8C00",
                alpha=0.6,
            )

        self.ax.set_title(
            "A* Maze Solver (Modern Look)", color="white", fontsize=14, pad=15
        )
        self.ax.set_aspect("equal")
        self.ax.invert_yaxis()
        self.fig.tight_layout()
        self.canvas.draw()

    def solve_and_plot_path(self):
        if self.maze_grid is None:
            messagebox.showwarning("Warning", "Please generate a maze first!")
            return

        solver = MazeSolver(self.maze_grid, self.start_pos, self.end_pos)
        self.path = solver.solve_maze_a_star()

        if self.path:
            print("\nPath found! Length:", len(self.path))
            self.plot_maze()
        else:
            messagebox.showinfo(
                "No Path", "No path could be found between the start and end points."
            )
            self.plot_maze()

    def clear_path(self):
        self.path = None
        self.plot_maze()


if __name__ == "__main__":
    root = tk.Tk()
    app = MazeApp(root)
    root.mainloop()
