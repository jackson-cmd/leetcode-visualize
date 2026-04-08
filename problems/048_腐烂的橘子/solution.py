import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
from collections import deque

def rotting_oranges(grid):
    """Visualize BFS spread of rotting oranges."""
    frames, durations = [], []
    rows, cols = len(grid), len(grid[0])

    grid_renderer = GridRenderer(rows, cols, cell_size=60,
                                 canvas_width=WIDTH, y=100)

    # Deep copy grid for simulation
    state = [row[:] for row in grid]

    # Symbols for display
    def get_display():
        vals = []
        for r in range(rows):
            row_v = []
            for c in range(cols):
                if state[r][c] == 0:
                    row_v.append('')
                elif state[r][c] == 1:
                    row_v.append('O')  # Fresh orange
                else:
                    row_v.append('X')  # Rotten
            vals.append(row_v)
        return vals

    def get_states(spreading=None):
        st = {}
        for r in range(rows):
            for c in range(cols):
                if state[r][c] == 0:
                    st[(r, c)] = CellState.INACTIVE
                elif state[r][c] == 1:
                    st[(r, c)] = (("#3b5a2d", Colors.GREEN), Colors.GREEN)
                    st[(r, c)] = ("#2d5a2d", Colors.GREEN)
                elif state[r][c] == 2:
                    st[(r, c)] = CellState.REMOVED
        if spreading:
            for r, c in spreading:
                st[(r, c)] = CellState.CHECKING
        return st

    def count_fresh():
        return sum(1 for r in range(rows) for c in range(cols) if state[r][c] == 1)

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#994 Rotting Oranges")
    fresh = count_fresh()
    rotten = sum(1 for r in range(rows) for c in range(cols) if state[r][c] == 2)
    fb.description(f"Fresh: {fresh}, Rotten: {rotten}")
    grid_renderer.draw(fb.draw, values=get_display(), states=get_states())
    fb.label(30, HEIGHT - 45, "Minute: 0", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Find initial rotten oranges
    queue = deque()
    for r in range(rows):
        for c in range(cols):
            if state[r][c] == 2:
                queue.append((r, c, 0))

    minutes = 0
    dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    while queue:
        # Process one level at a time
        level_size = len(queue)
        newly_rotten = []

        for _ in range(level_size):
            r, c, t = queue.popleft()
            for dr, dc in dirs:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and state[nr][nc] == 1:
                    state[nr][nc] = 2
                    queue.append((nr, nc, t + 1))
                    newly_rotten.append((nr, nc))
                    minutes = t + 1

        if newly_rotten:
            # Show spreading
            fb = FrameBuilder()
            fb.title("#994 Rotting Oranges")
            fb.description(f"Minute {minutes}: {len(newly_rotten)} oranges rot")
            grid_renderer.draw(fb.draw, values=get_display(),
                               states=get_states(spreading=newly_rotten))
            fresh = count_fresh()
            fb.label(30, HEIGHT - 45,
                     f"Minute: {minutes}   Fresh remaining: {fresh}",
                     Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            # Show settled state
            fb = FrameBuilder()
            fb.title("#994 Rotting Oranges")
            fb.description(f"After minute {minutes}")
            grid_renderer.draw(fb.draw, values=get_display(), states=get_states())
            fb.label(30, HEIGHT - 45,
                     f"Minute: {minutes}   Fresh remaining: {fresh}",
                     Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fresh = count_fresh()
    result = -1 if fresh > 0 else minutes
    fb = FrameBuilder()
    fb.title("#994 Rotting Oranges")
    fb.description("Simulation complete!")
    grid_renderer.draw(fb.draw, values=get_display(), states=get_states())
    fb.result_banner(f"Minutes: {result}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    frames, durations = rotting_oranges(grid)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
