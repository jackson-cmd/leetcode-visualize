import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def path_sum_iii_visual():
    """Visualize path sum III with prefix sum approach."""
    # tree: [10, 5, -3, 3, 2, None, 11, 3, -2, None, 1]
    # target = 8
    # Paths: 5->3, 5->2->1, -3->11, 10->5->3->-2->...
    # Simpler tree for visualization:
    tree = [10, 5, -3, 3, 2, None, 11]
    target = 8
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#437 Path Sum III")
    fb.description(f"Find paths summing to target = {target}")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "Using prefix sum approach", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # DFS with prefix sums
    # node_idx, prefix_sum, found_path_indices, description
    steps = [
        (0, 10, [], "Visit 10, prefix=10, need 10-8=2 in map -> No"),
        (1, 15, [], "Visit 5, prefix=15, need 15-8=7 in map -> No"),
        (3, 18, [], "Visit 3, prefix=18, need 18-8=10 in map -> Yes!"),
        (3, 18, [1, 3], "Found path: 5->3 = 8"),
        (4, 17, [], "Visit 2, prefix=17, need 17-8=9 in map -> No"),
        (2, 7, [], "Visit -3, prefix=7, need 7-8=-1 in map -> No"),
        (6, 18, [], "Visit 11, prefix=18, need 18-8=10 in map -> Yes!"),
        (6, 18, [2, 6], "Found path: -3->11 = 8"),
    ]

    found_paths = []
    path_count = 0
    visited = set()

    for node_idx, prefix, path_indices, desc in steps:
        visited.add(node_idx)
        states = {}
        for v in visited:
            if v != node_idx:
                states[v] = CellState.VISITED

        if path_indices:
            path_count += 1
            found_paths.extend(path_indices)
            for pi in path_indices:
                states[pi] = CellState.FOUND
            states[node_idx] = CellState.FOUND
        else:
            states[node_idx] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#437 Path Sum III")
        fb.description(desc)

        # Highlight found path edges
        path_set = path_indices if path_indices else []
        tr.draw(fb.draw, states=states, path=path_set)

        fb.label(50, HEIGHT - 100, f"Prefix sum: {prefix}", Colors.PEACH)
        fb.label(50, HEIGHT - 75, f"Paths found: {path_count}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#437 Path Sum III")
    fb.description("All paths found!")
    all_states = {i: CellState.VISITED for i in range(len(tree)) if tree[i] is not None}
    # Highlight the path nodes
    for pi in [1, 3, 2, 6]:
        all_states[pi] = CellState.FOUND
    tr.draw(fb.draw, states=all_states)
    fb.result_banner(f"Total Paths = {path_count}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = path_sum_iii_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
