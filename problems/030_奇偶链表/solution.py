import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def odd_even_linked_list(values):
    """Odd even linked list rearrangement, visualized step by step."""
    frames = []
    durations = []
    n = len(values)

    ll = LinkedListRenderer(values, y=180, node_w=52, node_h=46, spacing=32)

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#328 Odd Even Linked List")
    fb.description(f'head = {values}')
    ll.draw(fb.draw, states={})
    fb.label(50, 120, "Reorder: all odd-indexed nodes, then even-indexed", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Show odd/even identification
    states = {}
    for i in range(n):
        if i % 2 == 0:
            states[i] = CellState.LEFT_PTR   # odd position (1-indexed)
        else:
            states[i] = CellState.RIGHT_PTR  # even position

    fb = FrameBuilder()
    fb.title("#328 Odd Even Linked List")
    fb.description("Identify: odd (blue) vs even (orange) positions")
    ll.draw(fb.draw, states=states)
    fb.label(50, 120, "1-indexed: pos 1,3,5 = odd; pos 2,4 = even", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Strategy explanation
    fb = FrameBuilder()
    fb.title("#328 Odd Even Linked List")
    fb.description("Strategy: collect odd nodes, then even nodes")
    ll.draw(fb.draw, states=states,
            pointers={0: ("odd", Colors.SKY), 1: ("even", Colors.PEACH)})
    fb.label(50, 120, "Traverse list, separate into two groups, reconnect", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Step through the rearrangement one pointer at a time
    odd_vals = []
    even_vals = []

    for i in range(n):
        states = {}
        pointers = {}

        # Mark already collected
        for k in range(i):
            if k % 2 == 0:
                states[k] = CellState.FOUND
            else:
                states[k] = CellState.VISITED

        # Current node
        states[i] = CellState.CURRENT
        if i % 2 == 0:
            odd_vals.append(values[i])
            pointers[i] = ("odd", Colors.SKY)
            label_text = f"Node {i} (odd pos) -> add {values[i]} to odd list"
        else:
            even_vals.append(values[i])
            pointers[i] = ("even", Colors.PEACH)
            label_text = f"Node {i} (even pos) -> add {values[i]} to even list"

        fb = FrameBuilder()
        fb.title("#328 Odd Even Linked List")
        fb.description(label_text)
        ll.draw(fb.draw, states=states, pointers=pointers)
        fb.label(50, 120, f"Odd: {odd_vals}  Even: {even_vals}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Build result: odd nodes followed by even nodes
    result = odd_vals + even_vals
    ll_result = LinkedListRenderer(result, y=180, node_w=52, node_h=46, spacing=32)

    # Frame: Show merged result with color coding
    result_states = {}
    for i in range(len(odd_vals)):
        result_states[i] = CellState.LEFT_PTR
    for i in range(len(odd_vals), len(result)):
        result_states[i] = CellState.RIGHT_PTR

    fb = FrameBuilder()
    fb.title("#328 Odd Even Linked List")
    fb.description("Connect: odd list tail -> even list head")
    ll_result.draw(fb.draw, states=result_states)
    fb.label(50, 120, f"Odd: {odd_vals} + Even: {even_vals}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#328 Odd Even Linked List")
    fb.description("Rearrangement complete!")
    ll_result.draw(fb.draw, states={k: CellState.FOUND for k in range(len(result))})
    fb.result_banner(f'Result: {result}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = odd_even_linked_list([1, 2, 3, 4, 5])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
