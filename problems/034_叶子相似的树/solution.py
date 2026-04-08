import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def leaf_similar_visual():
    """Visualize leaf-similar trees comparison."""
    tree1 = [3, 5, 1, 6, 2, 9, 8]
    tree2 = [3, 5, 1, 6, 7, 4, 2]
    # Tree1 leaves: 6, 2, 9, 8 (indices 3,4,5,6 but tree2 leaf seq differs)
    # Actually: tree1 leaves L-R: 6,2,9,8; tree2 leaves L-R: 6,7,4,2
    # These are NOT similar. Let's use a similar pair.
    tree1 = [3, 5, 1, 6, 2, 9, 8]
    tree2 = [7, 2, 9, 6, None, None, 8]
    # tree1 leaves: 6,2,9,8; tree2 leaves: 6,8 -- not matching
    # Use simpler example: both have leaves [1,2,3]
    tree1 = [5, 3, 8, 1, None, None, 2]  # leaves: 1, 2
    tree2 = [4, 1, 6, None, None, 2, None]  # leaves: 1, 2
    # leaves of tree1: 1(idx3), 2(idx6) -> [1,2]
    # leaves of tree2: 1(idx3) -- wait idx3 is None for tree2
    # Let me be precise:
    # tree2 = [4, 1, 6, None, None, 2, None]
    # idx0=4, idx1=1, idx2=6, idx3=None, idx4=None, idx5=2, idx6=None
    # children of 1(idx1): idx3=None, idx4=None -> leaf
    # children of 6(idx2): idx5=2, idx6=None -> 2 is leaf
    # leaves: [1, 2] -- matches!

    HALF_W = WIDTH // 2
    tr1 = BinaryTreeRenderer(tree1, canvas_width=HALF_W, y=100, node_r=18, level_gap=55)
    tr2 = BinaryTreeRenderer(tree2, canvas_width=HALF_W, y=100, node_r=18, level_gap=55)

    frames, durations = [], []

    def draw_two_trees(fb, states1, states2, leaves1_so_far, leaves2_so_far):
        d = fb.draw
        # Divider
        d.line([(HALF_W, 80), (HALF_W, HEIGHT - 70)], fill=Colors.OVERLAY, width=1)
        fb.label(HALF_W // 2 - 20, 78, "Tree 1", Colors.ACCENT)
        fb.label(HALF_W + HALF_W // 2 - 20, 78, "Tree 2", Colors.PEACH)
        # Draw tree1 on left half
        tr1.draw(d, states=states1)
        # Draw tree2 on right half - shift positions
        save_pos = dict(tr2.positions)
        shifted = {k: (v[0] + HALF_W, v[1]) for k, v in save_pos.items()}
        tr2.positions = shifted
        tr2.draw(d, states=states2)
        tr2.positions = save_pos
        # Show leaf sequences
        l1_str = "Leaves1: [" + ", ".join(str(x) for x in leaves1_so_far) + "]"
        l2_str = "Leaves2: [" + ", ".join(str(x) for x in leaves2_so_far) + "]"
        fb.label(30, HEIGHT - 100, l1_str, Colors.GREEN)
        fb.label(30, HEIGHT - 75, l2_str, Colors.PEACH)

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#872 Leaf-Similar Trees")
    fb.description("Compare leaf sequences of two trees")
    draw_two_trees(fb, {}, {}, [], [])
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Collect leaves from tree1 step by step
    # tree1 = [5, 3, 8, 1, None, None, 2]
    # Leaves: idx3=1 (left child of 3), idx6=2 (right child of 8)
    tree1_leaf_indices = [3, 6]
    tree1_leaf_values = [1, 2]

    leaves1 = []
    for step, (li, lv) in enumerate(zip(tree1_leaf_indices, tree1_leaf_values)):
        leaves1.append(lv)
        states1 = {}
        for prev in tree1_leaf_indices[:step]:
            states1[prev] = CellState.FOUND
        states1[li] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#872 Leaf-Similar Trees")
        fb.description(f"Tree1: found leaf {lv} at index {li}")
        draw_two_trees(fb, states1, {}, leaves1, [])
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Mark all tree1 leaves as found
    states1_done = {li: CellState.FOUND for li in tree1_leaf_indices}

    # Collect leaves from tree2 step by step
    # tree2 = [4, 1, 6, None, None, 2, None]
    # idx1=1 is leaf (children None,None), idx5=2 is leaf (child of 6)
    tree2_leaf_indices = [1, 5]
    tree2_leaf_values = [1, 2]

    leaves2 = []
    for step, (li, lv) in enumerate(zip(tree2_leaf_indices, tree2_leaf_values)):
        leaves2.append(lv)
        states2 = {}
        for prev in tree2_leaf_indices[:step]:
            states2[prev] = CellState.FOUND
        states2[li] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#872 Leaf-Similar Trees")
        fb.description(f"Tree2: found leaf {lv} at index {li}")
        draw_two_trees(fb, states1_done, states2, tree1_leaf_values, leaves2)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Compare
    fb = FrameBuilder()
    fb.title("#872 Leaf-Similar Trees")
    fb.description("Compare: [1, 2] == [1, 2]")
    states2_done = {li: CellState.FOUND for li in tree2_leaf_indices}
    draw_two_trees(fb, states1_done, states2_done, tree1_leaf_values, tree2_leaf_values)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final
    fb = FrameBuilder()
    fb.title("#872 Leaf-Similar Trees")
    fb.description("Leaf sequences match!")
    draw_two_trees(fb, states1_done, states2_done, tree1_leaf_values, tree2_leaf_values)
    fb.result_banner("Result: True (Leaf-Similar)")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = leaf_similar_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
