# visualization.py
import matplotlib.pyplot as plt
import numpy as np


def visualize_maze(
    maze,
    path,
    start_pos,
    end_pos,
    title="A* Maze Solver Path with Movement Constraints",
):
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
    ax.set_title(title)
    plt.legend()
    plt.tight_layout()
    plt.show()
