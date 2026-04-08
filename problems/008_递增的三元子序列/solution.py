import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def increasing_triplet_viz(nums):
    """Visualize Increasing Triplet Subsequence algorithm."""
    frames = []
    durations = []

    arr = ArrayRenderer(nums, y=130, label="nums[]")
    first = float('inf')
    second = float('inf')
    found = False

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#334 Increasing Triplet")
    fb.description(f"nums = {nums}")
    arr.draw(fb.draw, states={})
    fb.label(50, 260, "first = inf", Colors.SKY)
    fb.label(50, 290, "second = inf", Colors.PEACH)
    fb.label(50, 320, "Looking for: first < second < third", Colors.ACCENT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for i, num in enumerate(nums):
        states = {}
        states[i] = CellState.CURRENT
        # Color previously seen elements
        for j in range(i):
            states[j] = CellState.INACTIVE

        # Mark elements that are first/second
        for j in range(i):
            if nums[j] == first and first != float('inf'):
                states[j] = CellState.LEFT_PTR
                break
        for j in range(i):
            if nums[j] == second and second != float('inf') and nums[j] != first:
                states[j] = CellState.RIGHT_PTR
                break

        if num <= first:
            old_first = first
            first = num
            fb = FrameBuilder()
            fb.title("#334 Increasing Triplet")
            fb.description(f"nums[{i}]={num} <= first({old_first if old_first != float('inf') else 'inf'}) -> update first={num}")
            states[i] = CellState.LEFT_PTR
            arr.draw(fb.draw, states=states,
                     pointers={i: ("check", Colors.ACCENT)})
            fb.label(50, 260, f"first = {first}", Colors.SKY)
            fb.label(50, 290, f"second = {second if second != float('inf') else 'inf'}", Colors.PEACH)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

        elif num <= second:
            old_second = second
            second = num
            fb = FrameBuilder()
            fb.title("#334 Increasing Triplet")
            fb.description(f"nums[{i}]={num} <= second({old_second if old_second != float('inf') else 'inf'}) -> update second={num}")
            states[i] = CellState.RIGHT_PTR
            arr.draw(fb.draw, states=states,
                     pointers={i: ("check", Colors.ACCENT)})
            fb.label(50, 260, f"first = {first}", Colors.SKY)
            fb.label(50, 290, f"second = {second}", Colors.PEACH)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

        else:
            # Found triplet!
            found = True
            fb = FrameBuilder()
            fb.title("#334 Increasing Triplet")
            fb.description(f"nums[{i}]={num} > second({second}) -> FOUND TRIPLET!")
            states[i] = CellState.FOUND

            # Highlight the triplet elements
            for j in range(i):
                if nums[j] == first:
                    states[j] = CellState.LEFT_PTR
                elif nums[j] == second:
                    states[j] = CellState.RIGHT_PTR

            arr.draw(fb.draw, states=states,
                     pointers={i: ("third!", Colors.GREEN)})
            fb.label(50, 260, f"first = {first}", Colors.SKY)
            fb.label(50, 290, f"second = {second}", Colors.PEACH)
            fb.label(50, 320, f"third = {num}", Colors.GREEN)
            fb.label(50, 350, f"Triplet: {first} < {second} < {num}", Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            # Final success frame
            fb = FrameBuilder()
            fb.title("#334 Increasing Triplet")
            fb.description(f"Found increasing triplet: {first} < {second} < {num}")
            arr.draw(fb.draw, states=states)
            fb.result_banner(f"Result: True ({first} < {second} < {num})")
            frames.append(fb.build())
            durations.append(DURATION_RESULT)
            return frames, durations

    # Not found
    fb = FrameBuilder()
    fb.title("#334 Increasing Triplet")
    fb.description("Scanned entire array - no triplet found")
    states = {i: CellState.REMOVED for i in range(len(nums))}
    arr.draw(fb.draw, states=states)
    fb.result_banner("Result: False")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = increasing_triplet_viz([2, 1, 5, 0, 4, 6])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
