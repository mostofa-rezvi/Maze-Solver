from pyamaze import maze, agent, textLabel
from queue import PriorityQueue


def h(cell1, cell2):
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def aStar(m):
    start = (m.rows, m.cols)
    end = (1, 1)

    g_score = {cell: float("inf") for cell in m.grid}
    f_score = {cell: float("inf") for cell in m.grid}

    g_score[start] = 0
    f_score[start] = h(start, end)

    open_set = PriorityQueue()
    open_set.put((f_score[start], start))

    came_from = {}

    while not open_set.empty():
        current_f_score, current_cell = open_set.get()

        if current_cell == end:
            path = {}
            while current_cell != start:
                prev_cell = came_from[current_cell]
                path[prev_cell] = current_cell
                current_cell = prev_cell
            return path

        for direction in "ESNW":
            if m.maze_map[current_cell][direction]:
                child_cell = None
                if direction == "E":
                    child_cell = (current_cell[0], current_cell[1] + 1)
                elif direction == "W":
                    child_cell = (current_cell[0], current_cell[1] - 1)
                elif direction == "N":
                    child_cell = (current_cell[0] - 1, current_cell[1])
                elif direction == "S":
                    child_cell = (current_cell[0] + 1, current_cell[1])

                if child_cell:
                    tentative_g_score = g_score[current_cell] + 1

                    if tentative_g_score < g_score[child_cell]:
                        came_from[child_cell] = current_cell
                        g_score[child_cell] = tentative_g_score
                        f_score[child_cell] = g_score[child_cell] + h(child_cell, end)
                        open_set.put((f_score[child_cell], child_cell))

    return {}


if __name__ == "__main__":
    m = maze(10, 10)
    m.CreateMaze()

    path = aStar(m)

    a = agent(m, footprints=True, filled=True)
    m.tracePath({a: path})
    l = textLabel(m, "A Star Path Length", len(path) + 1)

    print("Maze Map:", m.maze_map)
    print("Maze Grid:", m.grid)

    m.run()
