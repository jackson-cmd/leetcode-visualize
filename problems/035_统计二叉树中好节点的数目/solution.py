import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def good_nodes_visual():
    """Visualize counting good nodes in a binary tree."""
    # tree: [3, 1, 4, 3, None, 1, 5]
    # Good nodes: 3(root, always good), 4(path max 3<4), 3(path max 3<=3), 5(path max 4<5)
    # Not good: 1(path max 3>1), 1(path max 4>1)
    tree = [3, 1, 4, 3, None, 1, 5]
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#1448 Count Good Nodes")
    fb.description("Good node: no larger value on path from root")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "Good nodes count: 0", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # DFS steps: (node_idx, path_max, is_good, description)
    dfs_steps = [
        (0, 3, True, "Root 3, path_max=3, 3>=3 -> Good!"),
        (1, 3, False, "Node 1, path_max=3, 1<3 -> Not good"),
        (3, 3, True, "Node 3, path_max=3, 3>=3 -> Good!"),
        (2, 4, True, "Node 4, path_max=3, 4>=3 -> Good!"),
        (5, 4, False, "Node 1, path_max=4, 1<4 -> Not good"),
        (6, 5, True, "Node 5, path_max=4, 5>=4 -> Good!"),
    ]

    good_set = set()
    bad_set = set()
    visited = set()
    good_count = 0

    for node_idx, path_max, is_good, desc in dfs_steps:
        visited.add(node_idx)
        if is_good:
            good_count += 1
            good_set.add(node_idx)
        else:
            bad_set.add(node_idx)

        states = {}
        for g in good_set:
            if g != node_idx:
                states[g] = CellState.FOUND
        for b in bad_set:
            if b != node_idx:
                states[b] = CellState.REMOVED
        states[node_idx] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#1448 Count Good Nodes")
        fb.description(desc)
        tr.draw(fb.draw, states=states)
        color = Colors.GREEN if is_good else Colors.RED
        fb.label(50, HEIGHT - 100, f"Path max: {path_max}", Colors.PEACH)
        fb.label(50, HEIGHT - 75, f"Good nodes count: {good_count}", color)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#1448 Count Good Nodes")
    fb.description("DFS complete!")
    states = {}
    for g in good_set:
        states[g] = CellState.FOUND
    for b in bad_set:
        states[b] = CellState.REMOVED
    tr.draw(fb.draw, states=states)
    fb.result_banner(f"Good Nodes = {good_count}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = good_nodes_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
