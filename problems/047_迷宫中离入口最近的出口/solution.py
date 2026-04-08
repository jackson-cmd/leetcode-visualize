import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
from collections import deque

def nearest_exit(maze, entrance):
    """Visualize BFS to find nearest exit in a maze."""
    frames, durations = [], []
    rows, cols = len(maze), len(maze[0])

    grid = GridRenderer(rows, cols, cell_size=52,
                        canvas_width=WIDTH, y=90)

    def is_exit(r, c):
        return (r == 0 or r == rows - 1 or c == 0 or c == cols - 1) and \
               [r, c] != entrance

    # Frame 0: Show initial maze
    fb = FrameBuilder()
    fb.title("#1926 Nearest Exit from Entrance")
    fb.description(f"Maze {rows}x{cols}, entrance={entrance}")
    states = {}
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] == '+':
                states[(r, c)] = CellState.INACTIVE
    states[tuple(entrance)] = CellState.CURRENT

    display_vals = []
    for r in range(rows):
        row_vals = []
        for c in range(cols):
            if maze[r][c] == '+':
                row_vals.append('#')
            elif [r, c] == entrance:
                row_vals.append('E')
            elif is_exit(r, c):
                row_vals.append('X')
            else:
                row_vals.append('.')
        display_vals.append(row_vals)

    grid.draw(fb.draw, values=display_vals, states=states)
    fb.label(30, HEIGHT - 45, "BFS starting from entrance", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # BFS
    queue = deque([(entrance[0], entrance[1], 0)])
    visited = {(entrance[0], entrance[1])}
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    found_exit = None
    found_steps = -1

    while queue:
        # Process one BFS level at a time for cleaner visualization
        level_size = len(queue)
        level_cells = []
        next_level = []

        for _ in range(level_size):
            r, c, steps = queue.popleft()
            level_cells.append((r, c, steps))

            if is_exit(r, c):
                found_exit = (r, c)
                found_steps = steps
                break

            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and \
                   maze[nr][nc] == '.' and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc, steps + 1))
                    next_level.append((nr, nc))

        if found_exit:
            break

        # Show this BFS level
        states = {}
        for r in range(rows):
            for c in range(cols):
                if maze[r][c] == '+':
                    states[(r, c)] = CellState.INACTIVE
        states[tuple(entrance)] = CellState.CURRENT
        for vr, vc in visited:
            if (vr, vc) != tuple(entrance):
                states[(vr, vc)] = CellState.VISITED
        for nr, nc in next_level:
            states[(nr, nc)] = CellState.CHECKING

        step_val = level_cells[0][2] if level_cells else 0

        fb = FrameBuilder()
        fb.title("#1926 Nearest Exit from Entrance")
        fb.description(f"BFS level {step_val}: exploring {len(level_cells)} cells")
        grid.draw(fb.draw, values=display_vals, states=states)
        fb.label(30, HEIGHT - 45,
                 f"Steps: {step_val}   Visited: {len(visited)}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    if found_exit:
        # Show the exit found
        states = {}
        for r in range(rows):
            for c in range(cols):
                if maze[r][c] == '+':
                    states[(r, c)] = CellState.INACTIVE
        for vr, vc in visited:
            states[(vr, vc)] = CellState.VISITED
        states[tuple(entrance)] = CellState.CURRENT
        states[found_exit] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#1926 Nearest Exit from Entrance")
        fb.description(f"Exit found at {found_exit}!")
        grid.draw(fb.draw, values=display_vals, states=states)
        fb.result_banner(f"Nearest exit: {found_steps} steps")
        frames.append(fb.build())
        durations.append(DURATION_RESULT)
    else:
        fb = FrameBuilder()
        fb.title("#1926 Nearest Exit from Entrance")
        fb.description("No exit reachable!")
        fb.result_banner("Result: -1 (no exit)")
        frames.append(fb.build())
        durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    maze = [
        ["+", "+", ".", "+"],
        [".", ".", ".", "+"],
        ["+", "+", "+", "."]
    ]
    entrance = [1, 0]
    frames, durations = nearest_exit(maze, entrance)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
