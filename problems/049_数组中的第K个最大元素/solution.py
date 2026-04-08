import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
import heapq

def kth_largest(nums, k):
    """Visualize finding Kth largest using a min-heap of size k."""
    frames, durations = [], []

    arr = ArrayRenderer(nums, y=100, cell_w=55, label="nums")

    # Build heap array for display (level-order)
    min_heap = []

    def heap_to_tree_array(h):
        """Convert heap list to display array for BinaryTreeRenderer."""
        if not h:
            return []
        return list(h)

    # Frame 0: Initial
    fb = FrameBuilder(WIDTH, HEIGHT_TALL)
    fb.title("#215 Kth Largest Element")
    fb.description(f"nums = {nums}, k = {k}")
    arr.draw(fb.draw)
    fb.label(30, 200, "Min-Heap (size k): empty", Colors.TEXT)
    fb.label(30, HEIGHT_TALL - 45, f"Goal: find {k}th largest element", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for i, num in enumerate(nums):
        # Highlight current element
        states = {j: CellState.FOUND for j in range(i)}
        states[i] = CellState.CURRENT

        if len(min_heap) < k:
            heapq.heappush(min_heap, num)
            action = f"Push {num} (heap size < k={k})"
        elif num > min_heap[0]:
            removed = heapq.heapreplace(min_heap, num)
            action = f"Push {num}, pop {removed} (num > heap top)"
        else:
            action = f"Skip {num} (<= heap top {min_heap[0]})"

        # Draw array
        fb = FrameBuilder(WIDTH, HEIGHT_TALL)
        fb.title("#215 Kth Largest Element")
        fb.description(action)
        arr.draw(fb.draw, states=states,
                 pointers={i: ("i", Colors.ACCENT)})

        # Draw heap as tree
        heap_vals = heap_to_tree_array(min_heap)
        if heap_vals:
            heap_tree = HeapRenderer(heap_vals, y=250, node_r=20,
                                     level_gap=55, canvas_width=WIDTH,
                                     canvas_height=HEIGHT_TALL)
            heap_states = {0: CellState.CURRENT}  # Root is min
            heap_tree.draw(fb.draw, states=heap_states)

        fb.label(30, 220, f"Min-Heap (size {len(min_heap)}), top = {min_heap[0] if min_heap else '?'}",
                 Colors.TEXT)
        fb.label(30, HEIGHT_TALL - 45,
                 f"Heap: {sorted(min_heap)}   Step {i+1}/{len(nums)}",
                 Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    result = min_heap[0]
    fb = FrameBuilder(WIDTH, HEIGHT_TALL)
    fb.title("#215 Kth Largest Element")
    fb.description("Processing complete!")
    states = {j: CellState.FOUND for j in range(len(nums))}
    # Highlight the answer in the array
    for j, v in enumerate(nums):
        if v == result:
            states[j] = CellState.CURRENT
            break
    arr.draw(fb.draw, states=states)

    heap_vals = heap_to_tree_array(min_heap)
    heap_tree = HeapRenderer(heap_vals, y=250, node_r=20,
                             level_gap=55, canvas_width=WIDTH,
                             canvas_height=HEIGHT_TALL)
    heap_states = {0: CellState.FOUND}
    heap_tree.draw(fb.draw, states=heap_states)
    fb.label(30, 220, f"Min-Heap top = answer", Colors.GREEN)

    fb.result_banner(f"{k}th largest = {result}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = kth_largest([3, 2, 1, 5, 6, 4], 2)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
