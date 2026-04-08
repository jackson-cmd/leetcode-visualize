import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def reverse_linked_list(values):
    """Reverse linked list using prev/curr/next pointers, visualized."""
    frames = []
    durations = []
    n = len(values)

    ll = LinkedListRenderer(values, y=200, node_w=52, node_h=46, spacing=36)

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#206 Reverse Linked List")
    fb.description(f'head = {values}')
    ll.draw(fb.draw, states={})
    fb.label(50, 130, "Reverse by changing next pointers one by one", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Explain strategy
    fb = FrameBuilder()
    fb.title("#206 Reverse Linked List")
    fb.description("Use prev, curr, next pointers to reverse links")
    ll.draw(fb.draw, states={})
    fb.label(50, 130, "For each node: save next, point curr.next to prev, advance", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Initialize prev=None, curr=0
    fb = FrameBuilder()
    fb.title("#206 Reverse Linked List")
    fb.description("Initialize: prev=None, curr=head(0)")
    ll.draw(fb.draw, states={0: CellState.CURRENT},
            pointers={0: ("curr", Colors.ACCENT)})
    fb.label(50, 130, "prev = None", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    prev = -1  # -1 means None
    curr = 0

    while curr < n:
        nxt = curr + 1 if curr + 1 < n else -1

        states = {}
        pointers = {}

        # Color the nodes
        states[curr] = CellState.CURRENT
        if prev >= 0:
            states[prev] = CellState.CHECKING
        if nxt >= 0 and nxt < n:
            states[nxt] = CellState.WINDOW

        pointers[curr] = ("curr", Colors.ACCENT)
        if prev >= 0:
            pointers[prev] = ("prev", Colors.PEACH)
        if nxt >= 0 and nxt < n:
            pointers[nxt] = ("next", Colors.TEAL)

        # Show the step: save next, reverse link
        nxt_str = str(values[nxt]) if nxt >= 0 and nxt < n else "null"
        prev_str = str(values[prev]) if prev >= 0 else "None"

        fb = FrameBuilder()
        fb.title("#206 Reverse Linked List")
        fb.description(f'Save next={nxt_str}, set {values[curr]}.next -> {prev_str}')
        connections = [(i, i + 1) for i in range(n - 1)]
        ll.draw(fb.draw, states=states, pointers=pointers, connections=connections)
        fb.label(50, 130, f"Reverse link: {values[curr]} now points to {prev_str}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Frame: advance pointers
        prev = curr
        curr = nxt if nxt >= 0 else n

        if curr < n:
            states2 = {curr: CellState.CURRENT, prev: CellState.CHECKING}
            pointers2 = {curr: ("curr", Colors.ACCENT), prev: ("prev", Colors.PEACH)}

            fb = FrameBuilder()
            fb.title("#206 Reverse Linked List")
            fb.description(f'Advance: prev={values[prev]}, curr={values[curr]}')
            ll.draw(fb.draw, states=states2, pointers=pointers2, connections=connections)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Frame: curr is null, prev is new head
    fb = FrameBuilder()
    fb.title("#206 Reverse Linked List")
    fb.description(f'curr=null, prev={values[prev]} is new head!')
    ll.draw(fb.draw, states={prev: CellState.FOUND},
            pointers={prev: ("head", Colors.GREEN)})
    fb.label(50, 130, "All links reversed", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Build result
    result = values[::-1]
    ll_result = LinkedListRenderer(result, y=200, node_w=52, node_h=46, spacing=36)

    # Final frame
    fb = FrameBuilder()
    fb.title("#206 Reverse Linked List")
    fb.description("Reversed!")
    ll_result.draw(fb.draw, states={k: CellState.FOUND for k in range(n)})
    fb.result_banner(f'Result: {result}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = reverse_linked_list([1, 2, 3, 4, 5])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
