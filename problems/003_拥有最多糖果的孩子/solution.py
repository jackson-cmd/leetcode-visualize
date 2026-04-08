import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def kids_with_candies_viz(candies, extra):
    """Visualize Kids With the Greatest Number of Candies."""
    frames = []
    durations = []

    max_candy = max(candies)
    result = [False] * len(candies)
    arr = ArrayRenderer(candies, y=130, label="candies[]")

    # Frame 0: Initial state - show the array and find max
    fb = FrameBuilder()
    fb.title("#1431 Kids With Candies")
    fb.description(f"candies = {candies}, extraCandies = {extra}")
    arr.draw(fb.draw, states={})
    fb.label(50, 250, f"max = {max_candy}", Colors.ACCENT)
    fb.label(50, 280, f"extraCandies = {extra}", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Highlight the max
    max_states = {}
    for i, c in enumerate(candies):
        if c == max_candy:
            max_states[i] = CellState.FOUND
    fb = FrameBuilder()
    fb.title("#1431 Kids With Candies")
    fb.description(f"Find max candy = {max_candy}")
    arr.draw(fb.draw, states=max_states)
    fb.label(50, 250, f"max = {max_candy}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frames 2+: Check each kid
    for i in range(len(candies)):
        total = candies[i] + extra
        is_greatest = total >= max_candy
        result[i] = is_greatest

        states = {}
        states[i] = CellState.CURRENT
        # Mark previously checked
        for j in range(i):
            states[j] = CellState.FOUND if result[j] else CellState.REMOVED

        fb = FrameBuilder()
        fb.title("#1431 Kids With Candies")
        fb.description(f"Kid {i}: {candies[i]} + {extra} = {total} >= {max_candy} ? {'Yes' if is_greatest else 'No'}")
        arr.draw(fb.draw, states=states,
                 pointers={i: ("check", Colors.ACCENT)})
        fb.label(50, 250, f"max = {max_candy}, extra = {extra}", Colors.ACCENT)
        res_str = str([result[j] for j in range(i + 1)])
        fb.label(50, 280, f"result so far: {res_str}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#1431 Kids With Candies")
    fb.description("Complete!")
    states = {}
    for i in range(len(candies)):
        states[i] = CellState.FOUND if result[i] else CellState.REMOVED
    arr.draw(fb.draw, states=states)
    fb.result_banner(f"Result: {result}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = kids_with_candies_viz([2, 3, 5, 1, 3], 3)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
