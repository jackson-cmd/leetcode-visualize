import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def guess_number(n, pick):
    """Binary search to guess the number, visualized."""
    frames = []
    durations = []

    values = list(range(1, n + 1))
    ar = ArrayRenderer(values, y=160, cell_w=56, cell_h=52)

    # Frame 0: Problem setup
    fb = FrameBuilder()
    fb.title("#374 Guess Number Higher or Lower")
    fb.description(f"n = {n}, pick = ? (hidden target)")
    ar.draw(fb.draw, states={})
    fb.label(50, 380, "Goal: find the pick number using binary search", Colors.TEXT)
    fb.label(50, 410, "Each guess returns: -1 (too high), 1 (too low), 0 (correct)", Colors.SUBTEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Show binary search strategy
    fb = FrameBuilder()
    fb.title("#374 Guess Number Higher or Lower")
    fb.description("Strategy: binary search on range [1, 10]")
    ar.draw(fb.draw, states={i: CellState.WINDOW for i in range(n)})
    fb.label(50, 380, "Start with lo=1, hi=10", Colors.YELLOW)
    fb.label(50, 410, "Each step halves the search range", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    lo, hi = 0, n - 1
    step = 0

    while lo <= hi:
        mid = (lo + hi) // 2
        mid_val = values[mid]
        step += 1

        # Build states
        states = {}
        for i in range(len(values)):
            if i < lo or i > hi:
                states[i] = CellState.INACTIVE
            elif i == mid:
                states[i] = CellState.CURRENT
            else:
                states[i] = CellState.WINDOW

        pointers = {
            lo: ("lo", Colors.SKY),
            hi: ("hi", Colors.PEACH),
            mid: ("mid", Colors.ACCENT),
        }

        # Frame: Show mid calculation
        fb = FrameBuilder()
        fb.title("#374 Guess Number Higher or Lower")
        fb.description(f"Step {step}: lo={values[lo]}, hi={values[hi]}, mid=({values[lo]}+{values[hi]})/2={mid_val}")
        ar.draw(fb.draw, states=states, pointers=pointers)
        fb.label(50, 380, f"Guess mid = {mid_val}", Colors.ACCENT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        if mid_val == pick:
            # Found it - show the match
            states[mid] = CellState.FOUND
            fb = FrameBuilder()
            fb.title("#374 Guess Number Higher or Lower")
            fb.description(f"Step {step}: guess({mid_val}) == 0, FOUND!")
            ar.draw(fb.draw, states=states, pointers={mid: ("FOUND", Colors.GREEN)})
            fb.label(50, 380, f"guess({mid_val}) returns 0 -- correct!", Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            break
        elif mid_val < pick:
            # Show the guess result
            fb = FrameBuilder()
            fb.title("#374 Guess Number Higher or Lower")
            fb.description(f"Step {step}: guess({mid_val}) == 1, too low!")
            ar.draw(fb.draw, states=states, pointers=pointers)
            fb.label(50, 380, f"guess({mid_val}) returns 1: pick > {mid_val}", Colors.PEACH)
            fb.label(50, 410, f"Eliminate [{values[lo]}..{mid_val}], new range [{mid_val+1}..{values[hi]}]", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            # Show the narrowed range
            lo = mid + 1
            states2 = {}
            for i in range(len(values)):
                if i < lo or i > hi:
                    states2[i] = CellState.INACTIVE
                else:
                    states2[i] = CellState.WINDOW
            fb = FrameBuilder()
            fb.title("#374 Guess Number Higher or Lower")
            fb.description(f"Narrowed range: [{values[lo]}..{values[hi]}]")
            ar.draw(fb.draw, states=states2,
                   pointers={lo: ("lo", Colors.SKY), hi: ("hi", Colors.PEACH)})
            fb.label(50, 380, f"Search range now has {hi - lo + 1} candidates", Colors.YELLOW)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
        else:
            fb = FrameBuilder()
            fb.title("#374 Guess Number Higher or Lower")
            fb.description(f"Step {step}: guess({mid_val}) == -1, too high!")
            ar.draw(fb.draw, states=states, pointers=pointers)
            fb.label(50, 380, f"guess({mid_val}) returns -1: pick < {mid_val}", Colors.SKY)
            fb.label(50, 410, f"Eliminate [{mid_val}..{values[hi]}], new range [{values[lo]}..{mid_val-1}]", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            hi = mid - 1
            states2 = {}
            for i in range(len(values)):
                if i < lo or i > hi:
                    states2[i] = CellState.INACTIVE
                else:
                    states2[i] = CellState.WINDOW
            fb = FrameBuilder()
            fb.title("#374 Guess Number Higher or Lower")
            fb.description(f"Narrowed range: [{values[lo]}..{values[hi]}]")
            ar.draw(fb.draw, states=states2,
                   pointers={lo: ("lo", Colors.SKY), hi: ("hi", Colors.PEACH)})
            fb.label(50, 380, f"Search range now has {hi - lo + 1} candidates", Colors.YELLOW)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#374 Guess Number Higher or Lower")
    fb.description("Binary search complete!")
    final_states = {i: CellState.INACTIVE for i in range(len(values))}
    final_states[pick - 1] = CellState.FOUND
    ar.draw(fb.draw, states=final_states,
           pointers={pick - 1: ("pick", Colors.GREEN)})
    fb.result_banner(f"Result: pick = {pick} (found in {step} steps)")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = guess_number(10, 6)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
