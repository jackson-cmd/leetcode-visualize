import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def max_twin_sum(values):
    """Maximum twin sum using reverse second half + two pointers, visualized."""
    frames = []
    durations = []
    n = len(values)

    ll = LinkedListRenderer(values, y=180, node_w=52, node_h=46, spacing=32)

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#2130 Maximum Twin Sum of Linked List")
    fb.description(f'head = {values}')
    ll.draw(fb.draw, states={})
    fb.label(50, 120, f"Twin: node i pairs with node (n-1-i), n={n}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Show twin pairs
    states = {}
    for i in range(n // 2):
        states[i] = CellState.LEFT_PTR
        states[n - 1 - i] = CellState.RIGHT_PTR
    fb = FrameBuilder()
    fb.title("#2130 Maximum Twin Sum of Linked List")
    fb.description("Twin pairs: node 0+3, node 1+2")
    ll.draw(fb.draw, states=states)
    fb.label(50, 120, "First half (blue) pairs with reversed second half (orange)", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Step 1: Find middle using slow/fast
    slow, fast = 0, 0
    fb = FrameBuilder()
    fb.title("#2130 Maximum Twin Sum of Linked List")
    fb.description("Step 1: Find middle with slow/fast pointers")
    ll.draw(fb.draw, states={0: CellState.CURRENT},
            pointers={0: ("s/f", Colors.ACCENT)})
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    while fast < n and fast + 1 < n:
        slow += 1
        fast += 2
        states = {slow: CellState.CURRENT}
        pointers = {slow: ("slow", Colors.ACCENT)}
        if fast < n:
            states[fast] = CellState.CHECKING
            pointers[fast] = ("fast", Colors.PEACH)

        fb = FrameBuilder()
        fb.title("#2130 Maximum Twin Sum of Linked List")
        fb.description(f'slow={slow}, fast={fast}')
        ll.draw(fb.draw, states=states, pointers=pointers)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    mid = slow

    # Step 2: Reverse second half
    second_half = values[mid:]
    second_half_reversed = second_half[::-1]
    first_half = values[:mid]

    fb = FrameBuilder()
    fb.title("#2130 Maximum Twin Sum of Linked List")
    fb.description(f'Middle at index {mid}. Reverse second half.')
    states = {}
    for i in range(mid):
        states[i] = CellState.LEFT_PTR
    for i in range(mid, n):
        states[i] = CellState.RIGHT_PTR
    ll.draw(fb.draw, states=states, pointers={mid: ("mid", Colors.RED)})
    fb.label(50, 120, f"First: {first_half}, Second: {second_half} -> reversed: {second_half_reversed}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Show the two halves side by side
    ll_first = LinkedListRenderer(first_half, y=160, node_w=52, node_h=46, spacing=32,
                                   canvas_width=800)
    ll_second = LinkedListRenderer(second_half_reversed, y=280, node_w=52, node_h=46,
                                    spacing=32, canvas_width=800)

    fb = FrameBuilder()
    fb.title("#2130 Maximum Twin Sum of Linked List")
    fb.description("Step 2: Two halves ready for comparison")
    fb.label(50, 135, f"First half: {first_half}", Colors.SKY)
    ll_first.draw(fb.draw, states={k: CellState.LEFT_PTR for k in range(len(first_half))})
    fb.label(50, 255, f"Rev. 2nd half: {second_half_reversed}", Colors.PEACH)
    ll_second.draw(fb.draw, states={k: CellState.RIGHT_PTR for k in range(len(second_half_reversed))})
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Step 3: Compare twins and find max sum
    max_sum = 0
    for i in range(len(first_half)):
        twin_sum = first_half[i] + second_half_reversed[i]
        max_sum = max(max_sum, twin_sum)

        states_f = {i: CellState.CURRENT}
        states_s = {i: CellState.CURRENT}
        for k in range(i):
            states_f[k] = CellState.FOUND
            states_s[k] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#2130 Maximum Twin Sum of Linked List")
        fb.description(f'Pair: {first_half[i]} + {second_half_reversed[i]} = {twin_sum}')
        fb.label(50, 135, "First half:", Colors.SKY)
        ll_first.draw(fb.draw, states=states_f,
                      pointers={i: ("ptr", Colors.ACCENT)})
        fb.label(50, 255, "Reversed second half:", Colors.PEACH)
        ll_second.draw(fb.draw, states=states_s,
                       pointers={i: ("ptr", Colors.ACCENT)})
        is_max = " (new max!)" if twin_sum == max_sum and (i == 0 or twin_sum > max_sum - (first_half[i] + second_half_reversed[i]) + max_sum) else ""
        fb.label(50, 380, f"Sum = {twin_sum}, Max = {max_sum}{is_max}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#2130 Maximum Twin Sum of Linked List")
    fb.description("All twin pairs compared!")
    ll.draw(fb.draw, states={k: CellState.FOUND for k in range(n)})
    fb.result_banner(f'Maximum Twin Sum: {max_sum}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = max_twin_sum([5, 4, 2, 1])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
