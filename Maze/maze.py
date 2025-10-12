import heapq
import math
import matplotlib.pyplot as plt
import numpy as np


class Node:
    def __init__(self, position, direction, g_cost, h_cost, parent=None):
        self.position = position  # (row, col)
        self.direction = direction  # 0:N, 1:E, 2:S, 3:W
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.f_cost = g_cost + h_cost
        self.parent = parent

    def __lt__(self, other):
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        return self.position == other.position and self.direction == other.direction

    def __hash__(self):
        return hash((self.position, self.direction))


# Directions: (dr, dc) for (North, East, South, West)
DIRECTIONS = {
    0: (-1, 0),  # North
    1: (0, 1),  # East
    2: (1, 0),  # South
    3: (0, -1),  # West
}


def euclidean_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def is_valid_move(maze, pos):
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0


def solve_maze_a_star(maze, start_pos, end_pos):
    rows, cols = len(maze), len(maze[0])

    # Initial direction is West (facing left) because starting from bottom-right (cols-1, rows-1)
    # and "first entering the maze from the bottom right corner" usually implies moving inwards.
    # We assume 'entering' means the first move is *into* the maze, towards the left.
    # So, the agent is at start_pos and facing West (direction 3).
    start_direction = 3  # West

    open_list = []
    # Node(position, direction, g_cost, h_cost, parent)
    initial_node = Node(
        start_pos, start_direction, 0, euclidean_distance(start_pos, end_pos)
    )
    heapq.heappush(open_list, initial_node)

    # closed_list stores (position, direction) tuples
    closed_list = set()

    # For printing steps
    step_count = 0

    while open_list:
        current_node = heapq.heappop(open_list)

        print(
            f"Step {step_count}: Current Position: {current_node.position}, Facing: {list(DIRECTIONS.keys())[current_node.direction]}"
        )
        step_count += 1

        if current_node.position == end_pos:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]  # Reverse to get path from start to end

        if (current_node.position, current_node.direction) in closed_list:
            continue
        closed_list.add((current_node.position, current_node.direction))

        # Possible Actions:
        # 1. Move Forward
        # 2. Turn Right and Move Forward
        # 3. Turn Left and Move Forward (cannot move backward)

        # Action 1: Move Forward
        dr_f, dc_f = DIRECTIONS[current_node.direction]
        next_pos_f = (current_node.position[0] + dr_f, current_node.position[1] + dc_f)
        if is_valid_move(maze, next_pos_f):
            g_cost_f = current_node.g_cost + 1
            h_cost_f = euclidean_distance(next_pos_f, end_pos)
            neighbor_f = Node(
                next_pos_f, current_node.direction, g_cost_f, h_cost_f, current_node
            )
            if (neighbor_f.position, neighbor_f.direction) not in closed_list:
                heapq.heappush(open_list, neighbor_f)

        # Action 2: Turn Right and Move Forward
        # New direction: (current_direction + 1) % 4
        next_direction_r = (current_node.direction + 1) % 4
        dr_r, dc_r = DIRECTIONS[next_direction_r]
        next_pos_r = (current_node.position[0] + dr_r, current_node.position[1] + dc_r)
        if is_valid_move(maze, next_pos_r):
            g_cost_r = (
                current_node.g_cost + 1
            )  # Turning and moving counts as one "step"
            h_cost_r = euclidean_distance(next_pos_r, end_pos)
            neighbor_r = Node(
                next_pos_r, next_direction_r, g_cost_r, h_cost_r, current_node
            )
            if (neighbor_r.position, neighbor_r.direction) not in closed_list:
                heapq.heappush(open_list, neighbor_r)

        # Action 3: Turn Left and Move Forward
        # New direction: (current_direction - 1 + 4) % 4
        next_direction_l = (current_node.direction - 1 + 4) % 4
        dr_l, dc_l = DIRECTIONS[next_direction_l]
        next_pos_l = (current_node.position[0] + dr_l, current_node.position[1] + dc_l)
        if is_valid_move(maze, next_pos_l):
            g_cost_l = (
                current_node.g_cost + 1
            )  # Turning and moving counts as one "step"
            h_cost_l = euclidean_distance(next_pos_l, end_pos)
            neighbor_l = Node(
                next_pos_l, next_direction_l, g_cost_l, h_cost_l, current_node
            )
            if (neighbor_l.position, neighbor_l.direction) not in closed_list:
                heapq.heappush(open_list, neighbor_l)

    return None  # No path found


def visualize_maze(maze, path, start_pos, end_pos):
    fig, ax = plt.subplots(figsize=(len(maze[0]), len(maze)))

    # Walls in black, walkable paths in white
    maze_display = np.array(maze)
    ax.imshow(maze_display, cmap="binary", origin="upper")

    # Plot the path
    if path:
        path_rows = [p[0] for p in path]
        path_cols = [p[1] for p in path]
        ax.plot(
            path_cols, path_rows, color="red", linewidth=2, marker="o", markersize=4
        )

    # Mark start and end points
    ax.plot(
        start_pos[1],
        start_pos[0],
        marker="s",
        color="green",
        markersize=10,
        label="Start",
    )
    ax.plot(
        end_pos[1], end_pos[0], marker="*", color="blue", markersize=10, label="End"
    )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_title("A* Maze Solver Path with Movement Constraints")
    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    # Example Maze
    # 0 = walkable path, 1 = wall
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 1, 1, 1, 1, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]

    # Maze dimensions
    rows = len(maze)
    cols = len(maze[0])

    # Start: Bottom right corner (r, c)
    start_point = (rows - 2, cols - 2)  # (8, 8) in the example maze
    # End: Top left corner (r, c)
    end_point = (1, 1)

    print(
        f"Solving maze from {start_point} to {end_point} with complex movement constraints..."
    )
    found_path = solve_maze_a_star(maze, start_point, end_point)

    if found_path:
        print("\nPath Found! Visualizing the solution...")
        visualize_maze(maze, found_path, start_point, end_point)
    else:
        print("\nNo path found.")
