import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def max_depth_visual():
    """Visualize finding max depth of binary tree using DFS."""
    tree = [3, 9, 20, None, None, 15, 7]
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#104 Maximum Depth of Binary Tree")
    fb.description("Tree: [3, 9, 20, null, null, 15, 7]")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "Find max depth using DFS", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # DFS traversal order with depth tracking
    # index, depth, description
    dfs_steps = [
        (0, 1, "Visit root (3), depth=1"),
        (1, 2, "Go left to (9), depth=2"),
        (1, 2, "Node 9 is leaf, return depth=2"),
        (2, 2, "Go right to (20), depth=2"),
        (5, 3, "Go left to (15), depth=3"),
        (5, 3, "Node 15 is leaf, return depth=3"),
        (6, 3, "Go right to (7), depth=3"),
        (6, 3, "Node 7 is leaf, return depth=3"),
        (2, 3, "Back to 20, max child depth=3"),
        (0, 3, "Back to root, max depth=3"),
    ]

    visited = set()
    current_max = 0
    for idx, (node_idx, depth, desc) in enumerate(dfs_steps):
        visited.add(node_idx)
        current_max = max(current_max, depth)
        states = {}
        for v in visited:
            if v != node_idx:
                states[v] = CellState.VISITED
        states[node_idx] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#104 Maximum Depth of Binary Tree")
        fb.description(desc)
        tr.draw(fb.draw, states=states)
        fb.label(50, HEIGHT - 80, f"Current max depth: {current_max}", Colors.ACCENT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#104 Maximum Depth of Binary Tree")
    fb.description("DFS complete!")
    all_found = {i: CellState.FOUND for i in range(len(tree)) if tree[i] is not None}
    tr.draw(fb.draw, states=all_found)
    fb.result_banner("Max Depth = 3")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = max_depth_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
