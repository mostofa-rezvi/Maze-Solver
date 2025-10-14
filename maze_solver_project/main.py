from maze_solver import solve_maze_a_star, is_valid_move, DIRECTION_NAMES
from visualization import visualize_maze
from mazes.default_maze import DEFAULT_MAZE


def get_user_input(prompt, maze_rows, maze_cols):
    while True:
        try:
            coords_str = input(prompt).strip()
            if coords_str.lower() == "q":
                return None
            r, c = map(int, coords_str.split(","))
            if 0 <= r < maze_rows and 0 <= c < maze_cols:
                return (r, c)
            else:
                print(
                    f"Coordinates out of bounds. Please enter values between (0,0) and ({maze_rows-1},{maze_cols-1})."
                )
        except ValueError:
            print("Invalid input. Please enter coordinates as 'row,col' (e.g., '1,1').")


def get_start_direction_input():
    print("\nChoose initial facing direction for the agent:")
    for key, name in DIRECTION_NAMES.items():
        print(f"  {key}: {name}")
    while True:
        try:
            direction_key = int(input("Enter direction key (0-3): ").strip())
            if direction_key in DIRECTION_NAMES:
                return direction_key
            else:
                print("Invalid direction key. Please enter 0, 1, 2, or 3.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def main():
    maze = DEFAULT_MAZE
    rows = len(maze)
    cols = len(maze[0])

    print("---------------------------------------")
    print("  A* Maze Solver with Custom Constraints")
    print("---------------------------------------")
    print(f"Maze dimensions: {rows} rows x {cols} columns.")
    print("Walkable path: 0, Wall: 1")
    print(
        "Enter coordinates as 'row,col' (e.g., '1,1'). Type 'q' to quit at any prompt."
    )

    print("\nCurrent Maze Layout:")
    for r_idx, row in enumerate(maze):
        print(f"{r_idx:2d} {' '.join(map(str, row))}")
    print(
        "  " + " ".join([str(c_idx % 10) for c_idx in range(cols)])
    )
    print("-" * 30)

    start_point = None
    while start_point is None:
        input_coords = get_user_input(
            f"\nEnter Start Position (row,col) - must be a walkable path (0): ",
            rows,
            cols,
        )
        if input_coords is None:
            return
        if is_valid_move(maze, input_coords):
            start_point = input_coords
        else:
            print(
                f"({input_coords[0]},{input_coords[1]}) is a wall or out of bounds. Please choose a walkable path."
            )

    start_direction = get_start_direction_input()
    if start_direction is None:
        return

    end_point = None
    while end_point is None:
        input_coords = get_user_input(
            f"Enter End Position (row,col) - must be a walkable path (0): ", rows, cols
        )
        if input_coords is None:
            return
        if is_valid_move(maze, input_coords):
            end_point = input_coords
        else:
            print(
                f"({input_coords[0]},{input_coords[1]}) is a wall or out of bounds. Please choose a walkable path."
            )

    if start_point == end_point:
        print("Start and end points cannot be the same. Exiting.")
        return

    print(
        f"\nSolving maze from {start_point} (facing {DIRECTION_NAMES[start_direction]}) to {end_point}..."
    )
    found_path = solve_maze_a_star(
        maze, start_point, start_direction, end_point, verbose=True
    )

    if found_path:
        print("\nPath Found! Visualizing the solution...")
        visualize_maze(maze, found_path, start_point, end_point)
    else:
        print("\nNo path found.")


if __name__ == "__main__":
    main()
