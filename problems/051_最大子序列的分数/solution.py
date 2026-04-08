import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
import heapq

def max_subsequence_score(nums1, nums2, k):
    """Visualize maximum subsequence score using sorting + min-heap."""
    frames, durations = [], []

    n = len(nums1)
    # Pair and sort by nums2 descending
    pairs = sorted(zip(nums2, nums1), reverse=True)
    sorted_n2 = [p[0] for p in pairs]
    sorted_n1 = [p[1] for p in pairs]

    arr1 = ArrayRenderer(sorted_n1, y=100, cell_w=55, cell_h=45,
                         label="nums1 (sorted by nums2 desc)")
    arr2 = ArrayRenderer(sorted_n2, y=195, cell_w=55, cell_h=45,
                         label="nums2 (descending)")

    # Frame 0: Show sorted arrays
    fb = FrameBuilder(WIDTH, HEIGHT_TALL)
    fb.title("#2542 Maximum Subsequence Score")
    fb.description(f"Sort pairs by nums2 descending, k={k}")
    arr1.draw(fb.draw, show_indices=True)
    arr2.draw(fb.draw, show_indices=True)
    fb.label(30, 290, f"Score = sum(selected nums1) * min(selected nums2)", Colors.TEXT)
    fb.label(30, HEIGHT_TALL - 45, f"k = {k}, need to pick {k} indices", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Process: iterate nums2 desc, maintain top-k nums1 values via min-heap
    min_heap = []
    heap_sum = 0
    max_score = 0
    best_state = None

    for i in range(n):
        heapq.heappush(min_heap, sorted_n1[i])
        heap_sum += sorted_n1[i]

        if len(min_heap) > k:
            removed = heapq.heappop(min_heap)
            heap_sum -= removed

        states1 = {}
        states2 = {}
        for j in range(i + 1):
            states1[j] = CellState.VISITED
            states2[j] = CellState.VISITED
        states1[i] = CellState.CURRENT
        states2[i] = CellState.CURRENT

        # Highlight selected elements in heap
        heap_set = list(min_heap)
        for j in range(i + 1):
            if sorted_n1[j] in heap_set:
                states1[j] = CellState.FOUND
                heap_set.remove(sorted_n1[j])

        if len(min_heap) == k:
            score = heap_sum * sorted_n2[i]
            if score > max_score:
                max_score = score

            fb = FrameBuilder(WIDTH, HEIGHT_TALL)
            fb.title("#2542 Maximum Subsequence Score")
            fb.description(f"i={i}: sum={heap_sum} * min_n2={sorted_n2[i]} = {score}")
            arr1.draw(fb.draw, states=states1,
                      pointers={i: ("i", Colors.ACCENT)})
            arr2.draw(fb.draw, states=states2)

            # Draw heap
            heap_vals = sorted(min_heap)
            if heap_vals:
                heap_tree = HeapRenderer(heap_vals, y=340, node_r=18,
                                         level_gap=50, canvas_width=WIDTH,
                                         canvas_height=HEIGHT_TALL)
                h_states = {0: CellState.CURRENT}
                heap_tree.draw(fb.draw, states=h_states)

            fb.label(30, 305, f"Heap (size {k}): {sorted(min_heap)}, sum={heap_sum}",
                     Colors.TEXT)
            fb.label(30, HEIGHT_TALL - 45,
                     f"Score: {score}   Max so far: {max_score}", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
        else:
            fb = FrameBuilder(WIDTH, HEIGHT_TALL)
            fb.title("#2542 Maximum Subsequence Score")
            fb.description(f"i={i}: building heap ({len(min_heap)}/{k})")
            arr1.draw(fb.draw, states=states1,
                      pointers={i: ("i", Colors.ACCENT)})
            arr2.draw(fb.draw, states=states2)
            fb.label(30, 305, f"Heap: {sorted(min_heap)}, sum={heap_sum}",
                     Colors.TEXT)
            fb.label(30, HEIGHT_TALL - 45,
                     f"Heap size: {len(min_heap)}/{k}", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder(WIDTH, HEIGHT_TALL)
    fb.title("#2542 Maximum Subsequence Score")
    fb.description("All elements processed!")
    states1 = {j: CellState.FOUND for j in range(n)}
    states2 = {j: CellState.FOUND for j in range(n)}
    arr1.draw(fb.draw, states=states1)
    arr2.draw(fb.draw, states=states2)
    fb.result_banner(f"Maximum score: {max_score}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = max_subsequence_score([1, 3, 3, 2], [2, 1, 3, 4], 3)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
