import numpy as np
import matplotlib.pyplot as plt
from queue import PriorityQueue

# Define directions and their corresponding coordinate changes
# (row_change, col_change)
# 0: North, 1: East, 2: South, 3: West
DIRECTIONS = {
    0: (-1, 0),  # North
    1: (0, 1),  # East
    2: (1, 0),  # South
    3: (0, -1),  # West
}

# Define mapping for easier direction changes
# (current_direction, turn_action) -> new_direction
# Actions: 'F' (Forward), 'R' (Right), 'L' (Left)
TURN_MAP = {
    (0, "R"): 1,
    (0, "L"): 3,  # Facing North
    (1, "R"): 2,
    (1, "L"): 0,  # Facing East
    (2, "R"): 3,
    (2, "L"): 1,  # Facing South
    (3, "R"): 0,
    (3, "L"): 2,  # Facing West
}


def h_euclidean(cell1_pos, cell2_pos):
    """
    Heuristic function: Euclidean distance between two cell positions.
    """
    x1, y1 = cell1_pos
    x2, y2 = cell2_pos
    return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5


class MazeSolver:
    def __init__(self, maze_grid):
        self.maze_grid = maze_grid
        self.rows = len(maze_grid)
        self.cols = len(maze_grid[0])
        self.start_pos = (self.rows - 1, self.cols - 1)  # Bottom right
        self.end_pos = (0, 0)  # Top left (adjusted to 0-indexed)

        # Start direction: Initially facing North (0) as it's at the bottom.
        # This can be adjusted based on specific entry point requirements,
        # but North makes sense from bottom-right to top-left.
        self.start_node = (self.start_pos, 0)  # (position, direction)

    def is_valid_move(self, r, c):
        """Checks if a cell is within bounds and not a wall."""
        return 0 <= r < self.rows and 0 <= c < self.cols and self.maze_grid[r][c] == 0

    def get_neighbors(self, current_node):
        """
        Generates valid neighboring nodes based on movement constraints.
        A node is (position, direction).
        Allowed: Move Forward, Turn Right+Move Forward, Turn Left+Move Forward.
        Returns a list of (next_full_node, action_description) tuples.
        """
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
        """
        Solves the maze using the A* algorithm with directional constraints.
        A node in this context is (position, direction).
        """
        open_set = PriorityQueue()
        open_set.put((0, self.start_node))  # (f_score, node)

        # came_from[node] is the node immediately preceding it on the cheapest path from start
        came_from = {}

        # g_score[node] is the cost of the cheapest path from start to node
        g_score = {
            ((r, c), d): float("inf")
            for r in range(self.rows)
            for c in range(self.cols)
            for d in DIRECTIONS.keys()
        }
        g_score[self.start_node] = 0

        # f_score[node] = g_score[node] + h(node)
        f_score = {
            ((r, c), d): float("inf")
            for r in range(self.rows)
            for c in range(self.cols)
            for d in DIRECTIONS.keys()
        }
        f_score[self.start_node] = h_euclidean(self.start_pos, self.end_pos)

        while not open_set.empty():
            current_f, current_node = open_set.get()
            current_pos, current_dir = current_node

            # Optional: Print exploration steps for debugging/understanding
            # This makes the output very verbose for large mazes
            # print(f"  Exploring: Cell {current_pos}, Direction: {current_dir} (f={current_f:.2f}, g={g_score[current_node]:.2f})")

            if current_pos == self.end_pos:
                print("  Goal reached!")
                path = []
                current_path_node = current_node
                while current_path_node != self.start_node:
                    path.append(
                        current_path_node[0]
                    )  # Store only position for path visualization
                    current_path_node = came_from[current_path_node]
                path.append(self.start_node[0])
                return path[::-1]  # Reverse to get path from start to end

            for next_full_node, action_desc in self.get_neighbors(current_node):
                next_pos, next_direction = next_full_node  # Unpack the full node here

                tentative_g_score = (
                    g_score[current_node] + 1
                )  # Each valid move (including turns) costs 1

                # print(f"    From {current_pos} (Dir: {current_dir}) -> Action: {action_desc} -> To {next_pos} (Dir: {next_direction})")

                # The key for g_score is the full node: (position, direction)
                if tentative_g_score < g_score[next_full_node]:
                    came_from[next_full_node] = current_node
                    g_score[next_full_node] = tentative_g_score
                    f_score[next_full_node] = tentative_g_score + h_euclidean(
                        next_pos, self.end_pos
                    )
                    open_set.put((f_score[next_full_node], next_full_node))

        print("No path found.")
        return None

    def visualize_maze_and_path(self, path=None):
        """
        Visualizes the maze and the found path using Matplotlib.
        """
        fig, ax = plt.subplots(figsize=(self.cols, self.rows))

        # Create a colormap: 0=white (path), 1=black (wall)
        cmap = plt.cm.colors.ListedColormap(["white", "black"])
        bounds = [-0.5, 0.5, 1.5]
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

        ax.imshow(
            self.maze_grid,
            cmap=cmap,
            norm=norm,
            origin="upper",
            extent=[-0.5, self.cols - 0.5, self.rows - 0.5, -0.5],
        )

        # Grid lines
        ax.set_xticks(np.arange(-0.5, self.cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, self.rows, 1), minor=True)
        ax.grid(which="minor", color="gray", linestyle="-", linewidth=1)
        ax.tick_params(which="minor", size=0)

        # Plot the path if found
        if path:
            path_rows = [p[0] for p in path]
            path_cols = [p[1] for p in path]
            ax.plot(
                path_cols,
                path_rows,
                color="red",
                linewidth=3,
                marker="o",
                markersize=5,
                markerfacecolor="red",
            )

        # Mark start and end points
        ax.plot(
            self.start_pos[1], self.start_pos[0], "go", markersize=10, label="Start"
        )  # Green circle
        ax.plot(
            self.end_pos[1], self.end_pos[0], "bo", markersize=10, label="End"
        )  # Blue circle

        ax.set_title("Maze Solved with A* and Movement Constraints")
        ax.set_xlabel("Columns")
        ax.set_ylabel("Rows")
        ax.invert_yaxis()  # Origin at top-left
        plt.legend()
        plt.show()


# --- Main execution ---
if __name__ == "__main__":
    # Example Maze
    # 0 = walkable, 1 = wall
    maze_layout = [
        [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 0, 1, 1, 1, 1, 0],
        [0, 1, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 1, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 1, 1, 1, 0, 0, 0, 0],  # Start at (9,9)
    ]

    # Ensure start and end are walkable
    maze_layout[9][9] = 0  # Bottom right
    maze_layout[0][0] = 0  # Top left

    solver = MazeSolver(maze_layout)
    found_path = solver.solve_maze_a_star()

    if found_path:
        print("\nPath found! Length:", len(found_path))
        print("Path (rows, cols):", found_path)
    else:
        print("\nNo path could be found with the given constraints.")

    solver.visualize_maze_and_path(found_path)
