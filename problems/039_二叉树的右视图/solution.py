import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def right_side_view_visual():
    """Visualize binary tree right side view using BFS."""
    tree = [1, 2, 3, None, 5, None, 4]
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#199 Binary Tree Right Side View")
    fb.description("BFS level by level, take rightmost of each level")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "Right view: []", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # BFS by levels
    # Level 0: [1] (idx 0) -> rightmost = 1
    # Level 1: [2, 3] (idx 1, 2) -> rightmost = 3
    # Level 2: [5, 4] (idx 4, 6) -> rightmost = 4
    levels = [
        (0, [0], 0, "Level 0: [1], rightmost = 1"),
        (1, [1, 2], 2, "Level 1: [2, 3], rightmost = 3"),
        (2, [4, 6], 6, "Level 2: [5, 4], rightmost = 4"),
    ]

    right_view = []
    for level_num, node_indices, rightmost_idx, desc in levels:
        # First frame: highlight all nodes at this level
        states = {}
        for ni in node_indices:
            states[ni] = CellState.WINDOW
        # Previously found rightmost nodes stay green
        for prev_right in right_view:
            states[prev_right[1]] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#199 Binary Tree Right Side View")
        fb.description(f"Processing level {level_num}")
        tr.draw(fb.draw, states=states, level_highlight=level_num)
        rv_vals = [v for v, _ in right_view]
        fb.label(50, HEIGHT - 80, f"Right view so far: {rv_vals}", Colors.ACCENT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Second frame: highlight rightmost
        right_view.append((tree[rightmost_idx], rightmost_idx))
        states[rightmost_idx] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#199 Binary Tree Right Side View")
        fb.description(desc)
        tr.draw(fb.draw, states=states, level_highlight=level_num)
        rv_vals = [v for v, _ in right_view]
        fb.label(50, HEIGHT - 80, f"Right view: {rv_vals}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#199 Binary Tree Right Side View")
    fb.description("BFS complete!")
    states = {i: CellState.VISITED for i in range(len(tree)) if tree[i] is not None}
    for _, ri in right_view:
        states[ri] = CellState.FOUND
    tr.draw(fb.draw, states=states)
    result_vals = [v for v, _ in right_view]
    fb.result_banner(f"Right View = {result_vals}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = right_side_view_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
