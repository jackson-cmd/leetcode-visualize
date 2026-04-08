import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def max_level_sum_visual():
    """Visualize finding the level with maximum sum."""
    tree = [1, 7, 0, 7, -8, None, None]
    # Level 0: 1, sum=1
    # Level 1: 7+0=7
    # Level 2: 7+(-8)=-1
    # Max sum level = 1 (sum=7)
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#1161 Maximum Level Sum")
    fb.description("Find the level with maximum element sum")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "BFS level by level, compute sum per level", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Levels data
    levels = [
        (0, [0], [1], 1, "Level 1: sum(1) = 1"),
        (1, [1, 2], [7, 0], 7, "Level 2: sum(7, 0) = 7"),
        (2, [3, 4], [7, -8], -1, "Level 3: sum(7, -8) = -1"),
    ]

    max_sum = float('-inf')
    max_level = 0
    level_sums = []

    for level_num, node_indices, node_vals, level_sum, desc in levels:
        # Highlight current level
        states = {}
        for ni in node_indices:
            states[ni] = CellState.CURRENT

        # Mark previous levels as visited
        for prev_level in levels[:level_num]:
            for pi in prev_level[1]:
                states[pi] = CellState.VISITED

        fb = FrameBuilder()
        fb.title("#1161 Maximum Level Sum")
        fb.description(desc)
        tr.draw(fb.draw, states=states, level_highlight=level_num)

        level_sums.append(level_sum)
        if level_sum > max_sum:
            max_sum = level_sum
            max_level = level_num + 1

        sums_str = ", ".join(f"L{i+1}={s}" for i, s in enumerate(level_sums))
        fb.label(50, HEIGHT - 100, f"Sums: {sums_str}", Colors.PEACH)
        fb.label(50, HEIGHT - 75, f"Max sum so far: {max_sum} at level {max_level}",
                 Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Highlight the max level
    fb = FrameBuilder()
    fb.title("#1161 Maximum Level Sum")
    fb.description(f"Level {max_level} has maximum sum = {max_sum}")
    states = {}
    # Level 1 (index 1) nodes highlighted
    for ni in levels[max_level - 1][1]:
        states[ni] = CellState.FOUND
    # Other nodes visited
    for lnum, (_, nis, _, _, _) in enumerate(levels):
        if lnum != max_level - 1:
            for ni in nis:
                states[ni] = CellState.VISITED
    tr.draw(fb.draw, states=states, level_highlight=max_level - 1)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#1161 Maximum Level Sum")
    fb.description("Complete!")
    for ni in levels[max_level - 1][1]:
        states[ni] = CellState.FOUND
    tr.draw(fb.draw, states=states, level_highlight=max_level - 1)
    fb.result_banner(f"Max Level = {max_level} (sum = {max_sum})")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = max_level_sum_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
