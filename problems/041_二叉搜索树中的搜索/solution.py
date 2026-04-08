import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def search_bst_visual():
    """Visualize searching in a BST."""
    # BST: [4, 2, 7, 1, 3]
    # Search for val=2
    tree = [4, 2, 7, 1, 3]
    target = 2
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#700 Search in a BST")
    fb.description(f"Search for value = {target} in BST")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "BST property: left < root < right", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Search path: root(4) -> target < 4, go left -> node(2) = target, found!
    search_steps = [
        (0, 4, "Compare: 2 < 4, go left", False),
        (1, 2, "Compare: 2 == 2, found!", True),
    ]

    visited = set()
    for node_idx, node_val, desc, found in search_steps:
        visited.add(node_idx)
        states = {}
        for v in visited:
            if v != node_idx:
                states[v] = CellState.VISITED

        if found:
            states[node_idx] = CellState.FOUND
        else:
            states[node_idx] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#700 Search in a BST")
        fb.description(desc)
        tr.draw(fb.draw, states=states, path=list(visited))
        fb.label(50, HEIGHT - 100, f"Current node: {node_val}", Colors.ACCENT)
        fb.label(50, HEIGHT - 75, f"Target: {target}", Colors.PEACH)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Show subtree rooted at found node
    fb = FrameBuilder()
    fb.title("#700 Search in a BST")
    fb.description("Return subtree rooted at found node")
    states = {0: CellState.VISITED}
    states[1] = CellState.FOUND  # node 2
    states[3] = CellState.FOUND  # node 1 (left child of 2)
    states[4] = CellState.FOUND  # node 3 (right child of 2)
    tr.draw(fb.draw, states=states, path=[1, 3, 4])
    fb.label(50, HEIGHT - 80, "Subtree: [2, 1, 3]", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Now demonstrate a search that doesn't find
    # Search for val=5
    target2 = 5
    fb = FrameBuilder()
    fb.title("#700 Search in a BST")
    fb.description(f"Another example: search for {target2}")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, f"Target: {target2}", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    search_steps2 = [
        (0, 4, f"Compare: {target2} > 4, go right", False),
        (2, 7, f"Compare: {target2} < 7, go left", False),
    ]

    visited2 = set()
    for node_idx, node_val, desc, found in search_steps2:
        visited2.add(node_idx)
        states = {}
        for v in visited2:
            if v != node_idx:
                states[v] = CellState.VISITED
        states[node_idx] = CellState.CURRENT

        fb = FrameBuilder()
        fb.title("#700 Search in a BST")
        fb.description(desc)
        tr.draw(fb.draw, states=states, path=list(visited2))
        fb.label(50, HEIGHT - 100, f"Current node: {node_val}", Colors.ACCENT)
        fb.label(50, HEIGHT - 75, f"Target: {target2}", Colors.PEACH)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Node 7's left child (idx 5) doesn't exist
    fb = FrameBuilder()
    fb.title("#700 Search in a BST")
    fb.description(f"7 has no left child, {target2} not found")
    states = {0: CellState.VISITED, 2: CellState.REMOVED}
    tr.draw(fb.draw, states=states)
    fb.label(50, HEIGHT - 80, "Return null", Colors.RED)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final
    fb = FrameBuilder()
    fb.title("#700 Search in a BST")
    fb.description("BST search follows left/right based on comparison")
    tr.draw(fb.draw)
    fb.result_banner("O(h) search using BST property")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = search_bst_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
