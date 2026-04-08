import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def can_place_flowers_viz(flowerbed, n):
    """Visualize Can Place Flowers algorithm."""
    frames = []
    durations = []

    bed = list(flowerbed)  # mutable copy
    planted = 0
    arr = ArrayRenderer(bed, y=150, cell_w=55, label="flowerbed[]")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#605 Can Place Flowers")
    fb.description(f"flowerbed = {flowerbed}, n = {n}")
    states = {}
    for i, v in enumerate(bed):
        if v == 1:
            states[i] = CellState.FOUND
    arr.draw(fb.draw, states=states)
    fb.label(50, 270, f"Need to plant: {n} flowers", Colors.ACCENT)
    fb.label(50, 300, f"Planted: {planted}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Scan and plant
    for i in range(len(bed)):
        # Build states for current scan position
        states = {}
        for j, v in enumerate(bed):
            if v == 1:
                states[j] = CellState.FOUND
        states[i] = CellState.CURRENT

        empty_left = (i == 0 or bed[i - 1] == 0)
        empty_right = (i == len(bed) - 1 or bed[i + 1] == 0)
        can_plant = bed[i] == 0 and empty_left and empty_right

        fb = FrameBuilder()
        fb.title("#605 Can Place Flowers")
        if bed[i] == 1:
            fb.description(f"Position {i}: already has flower, skip")
        elif can_plant:
            fb.description(f"Position {i}: empty, neighbors empty -> plant!")
        else:
            fb.description(f"Position {i}: empty but neighbor occupied, skip")
        arr.draw(fb.draw, states=states, values_override=bed,
                 pointers={i: ("scan", Colors.ACCENT)})
        fb.label(50, 270, f"Need: {n}, Planted: {planted}", Colors.ACCENT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        if can_plant:
            bed[i] = 1
            planted += 1

            states[i] = CellState.SELECTED  # newly planted
            fb = FrameBuilder()
            fb.title("#605 Can Place Flowers")
            fb.description(f"Planted flower at position {i}!")
            arr.draw(fb.draw, states=states, values_override=bed,
                     pointers={i: ("new!", Colors.MAUVE)})
            fb.label(50, 270, f"Need: {n}, Planted: {planted}", Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            if planted >= n:
                # Early exit
                fb = FrameBuilder()
                fb.title("#605 Can Place Flowers")
                fb.description(f"Planted enough! ({planted} >= {n})")
                states_final = {}
                for j, v in enumerate(bed):
                    if v == 1:
                        states_final[j] = CellState.FOUND
                arr.draw(fb.draw, states=states_final, values_override=bed)
                fb.result_banner(f"Result: True (planted {planted})")
                frames.append(fb.build())
                durations.append(DURATION_RESULT)
                return frames, durations

    # Final frame
    success = planted >= n
    fb = FrameBuilder()
    fb.title("#605 Can Place Flowers")
    fb.description("Scan complete!")
    states_final = {}
    for j, v in enumerate(bed):
        if v == 1:
            states_final[j] = CellState.FOUND
    arr.draw(fb.draw, states=states_final, values_override=bed)
    fb.result_banner(f"Result: {success} (planted {planted}, need {n})")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = can_place_flowers_viz([1, 0, 0, 0, 0, 0, 1], 2)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
