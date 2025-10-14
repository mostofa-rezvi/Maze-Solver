import heapq
import math


class Node:
    def __init__(self, position, direction, g_cost, h_cost, parent=None):
        self.position = position
        self.direction = direction
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

DIRECTIONS_MAP = {
    0: (-1, 0), 
    1: (0, 1),
    2: (1, 0), 
    3: (0, -1),
}

DIRECTION_NAMES = {0: "North", 1: "East", 2: "South", 3: "West"}


def euclidean_distance(pos1, pos2):
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + (pos1[1] - pos2[1]) ** 2)


def is_valid_move(maze, pos):
    rows, cols = len(maze), len(maze[0])
    r, c = pos
    return 0 <= r < rows and 0 <= c < cols and maze[r][c] == 0


def solve_maze_a_star(maze, start_pos, start_facing_direction, end_pos, verbose=True):
    rows, cols = len(maze), len(maze[0])

    open_list = []
    initial_node = Node(
        start_pos, start_facing_direction, 0, euclidean_distance(start_pos, end_pos)
    )
    heapq.heappush(open_list, initial_node)

    closed_list = set()

    step_count = 0

    while open_list:
        current_node = heapq.heappop(open_list)

        if verbose:
            print(
                f"Step {step_count}: Current Position: {current_node.position}, Facing: {DIRECTION_NAMES[current_node.direction]}"
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

        dr_f, dc_f = DIRECTIONS_MAP[current_node.direction]
        next_pos_f = (current_node.position[0] + dr_f, current_node.position[1] + dc_f)
        if is_valid_move(maze, next_pos_f):
            g_cost_f = current_node.g_cost + 1
            h_cost_f = euclidean_distance(next_pos_f, end_pos)
            neighbor_f = Node(
                next_pos_f, current_node.direction, g_cost_f, h_cost_f, current_node
            )
            if (neighbor_f.position, neighbor_f.direction) not in closed_list:
                heapq.heappush(open_list, neighbor_f)

        next_direction_r = (current_node.direction + 1) % 4
        dr_r, dc_r = DIRECTIONS_MAP[next_direction_r]
        next_pos_r = (current_node.position[0] + dr_r, current_node.position[1] + dc_r)
        if is_valid_move(maze, next_pos_r):
            g_cost_r = (
                current_node.g_cost + 1
            )
            h_cost_r = euclidean_distance(next_pos_r, end_pos)
            neighbor_r = Node(
                next_pos_r, next_direction_r, g_cost_r, h_cost_r, current_node
            )
            if (neighbor_r.position, neighbor_r.direction) not in closed_list:
                heapq.heappush(open_list, neighbor_r)

        next_direction_l = (current_node.direction - 1 + 4) % 4
        dr_l, dc_l = DIRECTIONS_MAP[next_direction_l]
        next_pos_l = (current_node.position[0] + dr_l, current_node.position[1] + dc_l)
        if is_valid_move(maze, next_pos_l):
            g_cost_l = (
                current_node.g_cost + 1
            ) 
            h_cost_l = euclidean_distance(next_pos_l, end_pos)
            neighbor_l = Node(
                next_pos_l, next_direction_l, g_cost_l, h_cost_l, current_node
            )
            if (neighbor_l.position, neighbor_l.direction) not in closed_list:
                heapq.heappush(open_list, neighbor_l)

    return None
