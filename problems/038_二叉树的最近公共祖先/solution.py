import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def lca_visual():
    """Visualize finding lowest common ancestor of two nodes."""
    tree = [3, 5, 1, 6, 2, 0, 8]
    # Find LCA of 5 and 1 -> answer is 3
    # Find LCA of 5 and 6 -> answer is 5
    # Let's do LCA of 6 and 0 -> answer is 3
    p_val, q_val = 6, 0
    p_idx, q_idx = 3, 5  # indices in level-order array
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial - highlight target nodes
    fb = FrameBuilder()
    fb.title("#236 Lowest Common Ancestor")
    fb.description(f"Find LCA of p={p_val} and q={q_val}")
    states = {p_idx: CellState.LEFT_PTR, q_idx: CellState.RIGHT_PTR}
    tr.draw(fb.draw, states=states)
    fb.label(50, HEIGHT - 80, f"p = {p_val} (blue), q = {q_val} (orange)", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # DFS traversal steps
    # (node_idx, desc, found_p, found_q, is_lca)
    dfs_steps = [
        (0, "Visit root (3)", False, False, False),
        (1, "Visit left child (5)", False, False, False),
        (3, "Visit node (6) - found p!", True, False, False),
        (4, "Visit node (2) - not p or q", False, False, False),
        (1, "Back to (5): left found p", True, False, False),
        (2, "Visit right child (1)", False, False, False),
        (5, "Visit node (0) - found q!", False, True, False),
        (6, "Visit node (8) - not p or q", False, False, False),
        (2, "Back to (1): left found q", False, True, False),
        (0, "Back to root (3): left has p, right has q", True, True, True),
    ]

    visited = set()
    found_p = False
    found_q = False

    for node_idx, desc, fp, fq, is_lca in dfs_steps:
        visited.add(node_idx)
        if fp:
            found_p = True
        if fq:
            found_q = True

        states = {}
        for v in visited:
            if v != node_idx:
                states[v] = CellState.VISITED
        # Always highlight p and q
        states[p_idx] = CellState.LEFT_PTR
        states[q_idx] = CellState.RIGHT_PTR

        if is_lca:
            states[node_idx] = CellState.FOUND
        else:
            states[node_idx] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#236 Lowest Common Ancestor")
        fb.description(desc)
        tr.draw(fb.draw, states=states)

        status = []
        if found_p:
            status.append("p found")
        if found_q:
            status.append("q found")
        fb.label(50, HEIGHT - 80, "Status: " + (", ".join(status) if status else "searching..."),
                 Colors.ACCENT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#236 Lowest Common Ancestor")
    fb.description("LCA found!")
    states = {i: CellState.VISITED for i in range(len(tree)) if tree[i] is not None}
    states[p_idx] = CellState.LEFT_PTR
    states[q_idx] = CellState.RIGHT_PTR
    states[0] = CellState.FOUND  # LCA is root
    # Show path from LCA to p and q
    tr.draw(fb.draw, states=states, path=[0, 1, 3, 2, 5])
    fb.result_banner(f"LCA({p_val}, {q_val}) = {tree[0]}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = lca_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
