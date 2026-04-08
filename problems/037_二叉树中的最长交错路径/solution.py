import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def zigzag_visual():
    """Visualize longest zigzag path in a binary tree."""
    # Tree: [1, None, 2, 3, 4, None, None, 5, 6]
    # But level-order with None pads gets complex. Use a simpler tree:
    # [1, 2, 3, None, 4, None, None, None, None, 5, None]
    # Let's use: [1, None, 2, None, None, 3, 4]
    # Actually for BinaryTreeRenderer we need full level-order.
    # Tree:     1
    #            \
    #             2
    #            / \
    #           3   4
    #            \
    #             5
    # Level order: [1, None, 2, None, None, 3, 4, None, None, None, None, None, 5]
    # This is too many Nones. Simpler:
    #       1
    #      / \
    #     2   3
    #      \   \
    #       4   5
    #      /
    #     6
    # Level order: [1, 2, 3, None, 4, None, 5, None, None, 6]
    # Zigzag: 1->right->3->right->5 is NOT zigzag (both right)
    # Zigzag: 1->left->2->right->4->left->6 = length 3 (zigzag!)
    tree = [1, 2, 3, None, 4, None, 5, None, None, 6, None]
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH, node_r=20, level_gap=60)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#1372 Longest ZigZag Path")
    fb.description("Find longest alternating left-right path")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "ZigZag: alternate left/right at each step", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Show different zigzag attempts
    # Path 1: root(0)->left->2(1)->right->4(4)->left->6(9) = length 3
    # Path 2: root(0)->right->3(2)->right->5(6) = length 1 (reset at second right)
    zigzag_attempts = [
        # (path_indices, direction_labels, length, desc, is_best)
        ([0], ["start"], 0, "Start at root (1)", False),
        ([0, 1], ["R->L"], 1, "Go left to 2, zigzag len=1", False),
        ([0, 1, 4], ["R->L", "L->R"], 2, "Go right to 4, zigzag len=2", False),
        ([0, 1, 4, 9], ["R->L", "L->R", "R->L"], 3, "Go left to 6, zigzag len=3", True),
        ([0, 2], ["L->R"], 1, "Try: root right to 3, len=1", False),
        ([0, 2, 6], ["L->R", "...R"], 1, "3 right to 5, same dir, reset len=1", False),
    ]

    best_len = 0
    best_path = []
    for path, dirs, length, desc, is_best in zigzag_attempts:
        if is_best:
            best_len = length
            best_path = path

        states = {}
        for i, pi in enumerate(path):
            if i == len(path) - 1:
                states[pi] = CellState.CURRENT
            else:
                states[pi] = CellState.WINDOW

        fb = FrameBuilder()
        fb.title("#1372 Longest ZigZag Path")
        fb.description(desc)
        tr.draw(fb.draw, states=states, path=path)
        fb.label(50, HEIGHT - 100, f"Current zigzag length: {length}", Colors.ACCENT)
        fb.label(50, HEIGHT - 75, f"Best zigzag length: {best_len}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Highlight best path
    fb = FrameBuilder()
    fb.title("#1372 Longest ZigZag Path")
    fb.description("Best zigzag: 1 -> 2 -> 4 -> 6")
    states = {pi: CellState.FOUND for pi in best_path}
    tr.draw(fb.draw, states=states, path=best_path)
    fb.result_banner(f"Longest ZigZag = {best_len}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = zigzag_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
