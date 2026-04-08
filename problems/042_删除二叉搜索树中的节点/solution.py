import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def delete_bst_visual():
    """Visualize deleting a node from BST - showing all 3 cases."""
    # BST: [5, 3, 6, 2, 4, None, 7]
    # Delete key=3 (has two children: 2 and 4)
    tree = [5, 3, 6, 2, 4, None, 7]
    delete_key = 3
    tr = BinaryTreeRenderer(tree, canvas_width=WIDTH)
    frames, durations = [], []

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description(f"Delete key = {delete_key} from BST")
    tr.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "3 cases: leaf, one child, two children", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Step 1: Search for the node
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description(f"Step 1: Search for key={delete_key}")
    states = {0: CellState.CURRENT}
    tr.draw(fb.draw, states=states)
    fb.label(50, HEIGHT - 80, f"Compare: {delete_key} < 5, go left", Colors.ACCENT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Found node 3
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description(f"Found node {delete_key}!")
    states = {0: CellState.VISITED, 1: CellState.REMOVED}
    tr.draw(fb.draw, states=states)
    fb.label(50, HEIGHT - 80, "Node 3 has TWO children (2 and 4)", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Step 2: Find inorder successor (smallest in right subtree)
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("Two-child case: find inorder successor")
    states = {0: CellState.VISITED, 1: CellState.REMOVED,
              4: CellState.CURRENT}
    tr.draw(fb.draw, states=states)
    fb.label(50, HEIGHT - 80, "Inorder successor = 4 (leftmost in right subtree)", Colors.ACCENT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Step 3: Replace value
    tree_after = [5, 4, 6, 2, None, None, 7]
    tr_after = BinaryTreeRenderer(tree_after, canvas_width=WIDTH)
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("Replace 3 with successor 4, remove old 4")
    tr_after.draw(fb.draw, states={1: CellState.FOUND})
    fb.label(50, HEIGHT - 100, "Node 3 replaced with 4", Colors.GREEN)
    fb.label(50, HEIGHT - 75, "Old node 4 removed (was leaf)", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Show final tree
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("Final BST after deletion")
    tr_after.draw(fb.draw, states={1: CellState.FOUND})
    fb.label(50, HEIGHT - 80, "BST property maintained!", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Case 1: Delete a leaf (e.g., delete 7 from original tree)
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("Case 1: Delete leaf node (7)")
    states_leaf = {6: CellState.REMOVED}
    tr.draw(fb.draw, states=states_leaf)
    fb.label(50, HEIGHT - 80, "Leaf: simply remove the node", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    tree_no_leaf = [5, 3, 6, 2, 4, None, None]
    tr_no_leaf = BinaryTreeRenderer(tree_no_leaf, canvas_width=WIDTH)
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("After removing leaf 7")
    tr_no_leaf.draw(fb.draw)
    fb.label(50, HEIGHT - 80, "Simply set parent's child to null", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Case 2: Delete node with one child
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("Case 2: Delete one-child node (6)")
    states_one = {2: CellState.REMOVED, 6: CellState.CURRENT}
    tr.draw(fb.draw, states=states_one)
    fb.label(50, HEIGHT - 80, "One child: replace node with its child", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    tree_one_child = [5, 3, 7, 2, 4]
    tr_one = BinaryTreeRenderer(tree_one_child, canvas_width=WIDTH)
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("After: 7 takes 6's place")
    tr_one.draw(fb.draw, states={2: CellState.FOUND})
    fb.label(50, HEIGHT - 80, "Child 7 replaces deleted node 6", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final summary
    fb = FrameBuilder()
    fb.title("#450 Delete Node in BST")
    fb.description("Three deletion cases handled!")
    tr.draw(fb.draw)
    fb.result_banner("BST Delete: leaf / one child / two children")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = delete_bst_visual()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
