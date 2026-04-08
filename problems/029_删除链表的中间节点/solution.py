import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def delete_middle(values):
    """Delete middle node of linked list using slow/fast pointers, visualized."""
    frames = []
    durations = []
    n = len(values)

    ll = LinkedListRenderer(values, y=200, node_w=52, node_h=46, spacing=32)

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description(f'head = {values}')
    ll.draw(fb.draw, states={}, pointers={})
    fb.label(50, 130, f"Length = {n}, need to delete index {n // 2}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Explain strategy
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description("Strategy: slow/fast pointers to find middle")
    states = {}
    for i in range(n):
        states[i] = CellState.DEFAULT
    states[n // 2] = CellState.REMOVED
    ll.draw(fb.draw, states=states, pointers={n // 2: ("?mid", Colors.RED)})
    fb.label(50, 130, "When fast reaches end, slow is at middle", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Slow/Fast pointer traversal
    slow, fast = 0, 0
    prev_slow = -1

    # Frame: Initialize pointers
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description("Initialize: slow=0, fast=0")
    ll.draw(fb.draw, states={0: CellState.CURRENT},
            pointers={0: ("s/f", Colors.ACCENT)})
    fb.label(50, 130, "slow moves 1 step, fast moves 2 steps", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    step = 0
    while fast < n and (fast + 1) < n:
        prev_slow = slow
        slow += 1
        fast += 2
        step += 1

        states = {}
        pointers = {}
        # Mark traversed nodes
        for k in range(slow):
            states[k] = CellState.VISITED
        states[slow] = CellState.CURRENT
        if fast < n:
            states[fast] = CellState.CHECKING

        pointers[slow] = ("slow", Colors.ACCENT)
        if fast < n:
            pointers[fast] = ("fast", Colors.PEACH)

        fb = FrameBuilder()
        fb.title("#2095 Delete Middle of Linked List")
        fast_pos = fast if fast < n else "end"
        fb.description(f'Step {step}: slow={slow}, fast={fast_pos}')
        ll.draw(fb.draw, states=states, pointers=pointers)
        fb.label(50, 130, f"slow at node {values[slow]}, fast at {'end' if fast >= n else 'node ' + str(values[fast])}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Frame: Fast reached end
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description(f'Fast reached end! slow at index {slow}')
    states = {}
    for k in range(n):
        states[k] = CellState.VISITED
    states[slow] = CellState.CURRENT
    ll.draw(fb.draw, states=states, pointers={slow: ("slow", Colors.ACCENT)})
    fb.label(50, 130, f"Middle node found: index {slow}, value {values[slow]}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Highlight middle for removal
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description(f'Delete node {slow} (val={values[slow]})')
    states = {slow: CellState.REMOVED}
    if prev_slow >= 0:
        states[prev_slow] = CellState.CURRENT
    ll.draw(fb.draw, states=states,
            pointers={slow: ("DEL", Colors.RED)})
    fb.label(50, 130, f"Link prev node to next: {values[prev_slow]}.next -> {values[slow+1] if slow+1 < n else 'null'}", Colors.RED)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Build result
    result = values[:slow] + values[slow + 1:]
    ll_result = LinkedListRenderer(result, y=200, node_w=52, node_h=46, spacing=32)

    # Frame: Show reconnected list
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description("Node removed, list reconnected")
    ll_result.draw(fb.draw, states={k: CellState.FOUND for k in range(len(result))})
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#2095 Delete Middle of Linked List")
    fb.description("Done!")
    ll_result.draw(fb.draw, states={k: CellState.FOUND for k in range(len(result))})
    fb.result_banner(f'Result: {result}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = delete_middle([1, 3, 4, 7, 1, 2, 6])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
