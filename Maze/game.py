import math
import heapq
import numpy as np
import matplotlib.pyplot as plt
from typing import Tuple, List, Dict, Optional

# Direction vectors: Up, Right, Down, Left
DIRS = [(-1, 0), (0, 1), (1, 0), (0, -1)]
DIR_NAMES = ["UP", "RIGHT", "DOWN", "LEFT"]


def heuristic(r, c, gr, gc):
    """Euclidean distance heuristic."""
    return math.sqrt((r - gr) ** 2 + (c - gc) ** 2)


def successors(r, c, orient, maze):
    """Generate valid successors according to movement constraints."""
    rows, cols = len(maze), len(maze[0])
    succs = []
    for action in ["F", "R", "L"]:
        if action == "F":
            o2 = orient
        elif action == "R":
            o2 = (orient + 1) % 4
        else:
            o2 = (orient - 1) % 4
        dr, dc = DIRS[o2]
        r2, c2 = r + dr, c + dc
        if 0 <= r2 < rows and 0 <= c2 < cols and maze[r2][c2] == 0:
            succs.append(((r2, c2, o2), action))
    return succs


def reconstruct_path(parents, end_state):
    """Reconstruct full path from start to goal."""
    path = []
    s = end_state
    while s in parents:
        prev, action = parents[s]
        path.append((s, action))
        s = prev
    path.reverse()
    return [state for state, _ in path]


def astar_search(maze, start, goal, start_orient=0, verbose=True):
    """A* algorithm with constrained movement."""
    rows, cols = len(maze), len(maze[0])
    start_state = (start[0], start[1], start_orient)
    goal_r, goal_c = goal

    open_list = []
    g = {start_state: 0}
    h0 = heuristic(start[0], start[1], goal_r, goal_c)
    heapq.heappush(open_list, (h0, start_state))
    parents = {}
    closed = set()

    while open_list:
        f, current = heapq.heappop(open_list)
        r, c, orient = current
        g_curr = g[current]
        h_curr = heuristic(r, c, goal_r, goal_c)
        if verbose:
            print(
                f"POP: Pos=({r},{c}) Dir={DIR_NAMES[orient]} g={g_curr:.2f} h={h_curr:.2f} f={f:.2f}"
            )

        # Goal check
        if (r, c) == (goal_r, goal_c):
            print("\nGOAL reached! Reconstructing path...\n")
            return reconstruct_path(parents, current)

        closed.add(current)

        for next_state, action in successors(r, c, orient, maze):
            tentative_g = g_curr + 1
            if next_state in closed and tentative_g >= g.get(next_state, math.inf):
                continue
            if tentative_g < g.get(next_state, math.inf):
                g[next_state] = tentative_g
                parents[next_state] = (current, action)
                h = heuristic(next_state[0], next_state[1], goal_r, goal_c)
                f_new = tentative_g + h
                heapq.heappush(open_list, (f_new, next_state))
                if verbose:
                    r2, c2, o2 = next_state
                    print(
                        f"  PUSH: ({r2},{c2}) Dir={DIR_NAMES[o2]} Action={action} g={tentative_g} h={h:.2f} f={f_new:.2f}"
                    )
    print("No path found under the movement constraints.")
    return None


def visualize(maze, path, start, goal, filename="maze_solution.png"):
    """Plot maze and overlay the found path."""
    maze_array = np.array(maze)
    plt.imshow(maze_array, cmap="binary_r")
    if path:
        path_cells = [(r, c) for r, c, _ in path]
        xs = [c + 0.5 for r, c in path_cells]
        ys = [r + 0.5 for r, c in path_cells]
        plt.plot(xs, ys, linewidth=2, color="red", label="path")
    plt.scatter([start[1] + 0.5], [start[0] + 0.5], color="green", s=80, label="start")
    plt.scatter([goal[1] + 0.5], [goal[0] + 0.5], color="blue", s=80, label="goal")
    plt.gca().invert_yaxis()
    plt.axis("off")
    plt.legend()
    plt.title("Maze Solver Path (A* with movement constraints)")
    plt.savefig(filename, bbox_inches="tight")
    plt.show()


def main():
    # Example maze: 0 = walkable, 1 = wall
    maze = [
        [0, 1, 0, 0, 0],
        [0, 1, 0, 1, 0],
        [0, 0, 0, 1, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
    ]

    rows, cols = len(maze), len(maze[0])
    start = (rows - 1, cols - 1)  # bottom-right corner
    goal = (0, 0)  # top-left corner
    start_orient = 0  # facing up

    print("Starting A* search with constrained movement...\n")
    path = astar_search(maze, start, goal, start_orient=start_orient, verbose=True)

    if path:
        print(f"Path found with {len(path)} steps.")
        visualize(maze, path, start, goal)
    else:
        print("No path found.")


if __name__ == "__main__":
    main()
