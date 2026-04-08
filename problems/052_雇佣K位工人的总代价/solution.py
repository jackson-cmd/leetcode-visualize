import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
import heapq

def total_cost_hire_workers(costs, k, candidates):
    """Visualize hiring K workers using two min-heaps from both ends."""
    frames, durations = [], []
    n = len(costs)

    arr = ArrayRenderer(costs, y=100, cell_w=55, cell_h=50,
                        label="costs", canvas_width=WIDTH_WIDE)

    # Frame 0: Initial
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#2462 Hire K Workers")
    fb.description(f"costs={costs}, k={k}, candidates={candidates}")
    arr.draw(fb.draw)
    fb.label(30, HEIGHT_TALL - 65,
             f"Hire {k} workers, consider {candidates} from each end",
             Colors.TEXT)
    fb.label(30, HEIGHT_TALL - 40, "Total cost: 0", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Two heaps approach
    left_heap = []   # min-heap for left candidates
    right_heap = []  # min-heap for right candidates
    left = 0
    right = n - 1
    total_cost = 0
    hired = set()

    # Initialize heaps
    for i in range(candidates):
        if left <= right:
            heapq.heappush(left_heap, (costs[left], left))
            left += 1
    for i in range(candidates):
        if left <= right:
            heapq.heappush(right_heap, (costs[right], right))
            right -= 1

    # Show initial heap state
    states = {}
    for cost_val, idx in left_heap:
        states[idx] = CellState.LEFT_PTR
    for cost_val, idx in right_heap:
        states[idx] = CellState.RIGHT_PTR

    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#2462 Hire K Workers")
    fb.description(f"Left pool (blue), Right pool (orange)")
    arr.draw(fb.draw, states=states)
    left_vals = sorted([c for c, _ in left_heap])
    right_vals = sorted([c for c, _ in right_heap])
    fb.label(30, 210, f"Left heap: {left_vals}", Colors.SKY)
    fb.label(30, 235, f"Right heap: {right_vals}", Colors.PEACH)
    fb.label(30, HEIGHT_TALL - 40, "Total cost: 0", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for hire_round in range(k):
        # Pick the cheaper option
        left_min = left_heap[0] if left_heap else (float('inf'), -1)
        right_min = right_heap[0] if right_heap else (float('inf'), -1)

        if left_min[0] <= right_min[0]:
            cost_val, idx = heapq.heappop(left_heap)
            source = "left"
            # Add next from left
            if left <= right:
                heapq.heappush(left_heap, (costs[left], left))
                left += 1
        else:
            cost_val, idx = heapq.heappop(right_heap)
            source = "right"
            # Add next from right
            if left <= right:
                heapq.heappush(right_heap, (costs[right], right))
                right -= 1

        total_cost += cost_val
        hired.add(idx)

        # Update display
        states = {}
        for c, i in left_heap:
            states[i] = CellState.LEFT_PTR
        for c, i in right_heap:
            states[i] = CellState.RIGHT_PTR
        for h in hired:
            states[h] = CellState.FOUND
        states[idx] = CellState.CURRENT

        fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
        fb.title("#2462 Hire K Workers")
        fb.description(f"Round {hire_round+1}: hire worker {idx} (cost={cost_val}) from {source}")
        arr.draw(fb.draw, states=states,
                 pointers={idx: ("hire", Colors.GREEN)})
        left_vals = sorted([c for c, _ in left_heap])
        right_vals = sorted([c for c, _ in right_heap])
        fb.label(30, 210, f"Left heap: {left_vals}", Colors.SKY)
        fb.label(30, 235, f"Right heap: {right_vals}", Colors.PEACH)
        fb.label(30, HEIGHT_TALL - 65,
                 f"Hired: {hire_round+1}/{k}", Colors.TEXT)
        fb.label(30, HEIGHT_TALL - 40,
                 f"Total cost: {total_cost}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#2462 Hire K Workers")
    fb.description(f"All {k} workers hired!")
    states = {}
    for h in hired:
        states[h] = CellState.FOUND
    arr.draw(fb.draw, states=states)
    fb.result_banner(f"Total cost: {total_cost}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = total_cost_hire_workers(
        [17, 12, 10, 2, 7, 2, 11, 20, 8], k=3, candidates=4)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
