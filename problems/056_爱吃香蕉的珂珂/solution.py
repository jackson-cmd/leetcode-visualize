import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
import math

def koko_eating_bananas(piles, h):
    """Binary search on eating speed k, visualized."""
    frames = []
    durations = []

    pile_ar = ArrayRenderer(piles, y=110, cell_w=60, cell_h=48, label="piles")

    # Frame 0: Problem setup
    fb = FrameBuilder()
    fb.title("#875 Koko Eating Bananas")
    fb.description(f"piles = {piles}, h = {h} hours")
    pile_ar.draw(fb.draw)
    fb.label(50, 220, "Find minimum eating speed k to finish in h hours", Colors.TEXT)
    fb.label(50, 250, "Each hour, eat min(k, pile) bananas from one pile", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Explain the binary search
    fb = FrameBuilder()
    fb.title("#875 Koko Eating Bananas")
    fb.description(f"Binary search speed k in [1, {max(piles)}]")
    pile_ar.draw(fb.draw)
    fb.label(50, 220, f"If k=1: too slow (need {sum(piles)} hours > {h})", Colors.RED)
    fb.label(50, 250, f"If k={max(piles)}: fast (need {len(piles)} hours)", Colors.GREEN)
    fb.label(50, 280, "Binary search for the minimum valid k", Colors.YELLOW)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    lo, hi = 1, max(piles)
    step = 0
    answer = hi

    while lo <= hi:
        mid = (lo + hi) // 2
        step += 1

        hours = sum(math.ceil(p / mid) for p in piles)
        hours_per_pile = [math.ceil(p / mid) for p in piles]

        pile_states = {}
        for i in range(len(piles)):
            if hours_per_pile[i] <= 1:
                pile_states[i] = CellState.FOUND
            elif hours_per_pile[i] <= 2:
                pile_states[i] = CellState.WINDOW
            else:
                pile_states[i] = CellState.CHECKING

        # Frame: Show speed and calculation
        fb = FrameBuilder()
        fb.title("#875 Koko Eating Bananas")
        fb.description(f"Step {step}: try k={mid} (search [{lo}..{hi}])")
        pile_ar.draw(fb.draw, states=pile_states)
        detail = " + ".join([f"{math.ceil(p/mid)}" for p in piles])
        fb.label(50, 220, f"Hours per pile: {[math.ceil(p/mid) for p in piles]}", Colors.TEXT)
        fb.label(50, 250, f"Total hours = {detail} = {hours}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Frame: Show decision
        fb = FrameBuilder()
        fb.title("#875 Koko Eating Bananas")
        if hours <= h:
            answer = mid
            fb.description(f"k={mid}: {hours} hours <= {h}, works!")
            pile_ar.draw(fb.draw, states=pile_states)
            fb.label(50, 220, f"k={mid} is valid, try smaller: search [{lo}..{mid-1}]", Colors.GREEN)
            fb.label(50, 250, f"Best answer so far: k={answer}", Colors.YELLOW)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            hi = mid - 1
        else:
            fb.description(f"k={mid}: {hours} hours > {h}, too slow!")
            pile_ar.draw(fb.draw, states=pile_states)
            fb.label(50, 220, f"k={mid} too slow, try faster: search [{mid+1}..{hi}]", Colors.RED)
            fb.label(50, 250, f"Need faster speed", Colors.PEACH)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            lo = mid + 1

    # Show the answer verification
    final_hours = [math.ceil(p / answer) for p in piles]
    pile_states = {i: CellState.FOUND for i in range(len(piles))}

    fb = FrameBuilder()
    fb.title("#875 Koko Eating Bananas")
    fb.description(f"Verify: k={answer}")
    pile_ar.draw(fb.draw, states=pile_states)
    detail = " + ".join([str(h) for h in final_hours])
    fb.label(50, 220, f"At k={answer}: hours = {detail} = {sum(final_hours)} <= {h}", Colors.GREEN)
    fb.label(50, 250, "This is the minimum valid speed!", Colors.YELLOW)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final
    fb = FrameBuilder()
    fb.title("#875 Koko Eating Bananas")
    fb.description("Binary search complete!")
    pile_ar.draw(fb.draw, states=pile_states)
    fb.result_banner(f"Result: k = {answer}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = koko_eating_bananas([3, 6, 7, 11], 8)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
