import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
import bisect

def spells_and_potions(spells, potions, success):
    """Sort potions then binary search for each spell."""
    frames = []
    durations = []

    sorted_potions = sorted(potions)
    n = len(sorted_potions)

    # Frame 0: Initial state
    sp_ar = ArrayRenderer(spells, y=110, cell_w=56, cell_h=48, label="spells")
    pt_ar = ArrayRenderer(sorted_potions, y=220, cell_w=56, cell_h=48, label="potions (sorted)")

    fb = FrameBuilder()
    fb.title("#2300 Spells and Potions")
    fb.description(f"spells={spells}, potions={potions}, success={success}")
    sp_ar.draw(fb.draw)
    pt_ar.draw(fb.draw)
    fb.label(50, 340, "Sort potions first, then binary search for each spell", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: After sorting
    fb = FrameBuilder()
    fb.title("#2300 Spells and Potions")
    fb.description(f"Sorted potions: {sorted_potions}")
    sp_ar.draw(fb.draw)
    pt_ar.draw(fb.draw, states={i: CellState.FOUND for i in range(n)})
    fb.label(50, 340, "Potions sorted. Now binary search for each spell.", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    result = []

    for si, spell in enumerate(spells):
        # Need spell * potion >= success => potion >= success / spell
        threshold = success / spell
        # Find first potion >= threshold
        lo, hi = 0, n - 1
        pos = n  # default: no valid potion

        sp_states = {si: CellState.CURRENT}
        for k in range(si):
            sp_states[k] = CellState.FOUND

        # Show threshold calculation
        fb = FrameBuilder()
        fb.title("#2300 Spells and Potions")
        fb.description(f"Spell={spell}: need potion >= {success}/{spell} = {threshold:.1f}")
        sp_ar.draw(fb.draw, states=sp_states, pointers={si: ("spell", Colors.ACCENT)})
        pt_ar.draw(fb.draw)
        fb.label(50, 340, f"Binary search for first potion >= {threshold:.1f}", Colors.YELLOW)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Binary search steps
        lo, hi = 0, n - 1
        pos = n
        while lo <= hi:
            mid = (lo + hi) // 2
            pt_states = {}
            for i in range(n):
                if i < lo or i > hi:
                    pt_states[i] = CellState.INACTIVE
                elif i == mid:
                    pt_states[i] = CellState.CURRENT
                else:
                    pt_states[i] = CellState.WINDOW

            product = spell * sorted_potions[mid]
            if sorted_potions[mid] >= threshold:
                pos = mid
                fb = FrameBuilder()
                fb.title("#2300 Spells and Potions")
                fb.description(f"Spell={spell}: mid={mid}, {spell}*{sorted_potions[mid]}={product} >= {success}")
                sp_ar.draw(fb.draw, states=sp_states)
                pt_ar.draw(fb.draw, states=pt_states,
                          pointers={mid: ("mid", Colors.ACCENT)})
                fb.label(50, 340, f"Valid! Search left for earlier valid potion", Colors.GREEN)
                frames.append(fb.build())
                durations.append(DURATION_NORMAL)
                hi = mid - 1
            else:
                fb = FrameBuilder()
                fb.title("#2300 Spells and Potions")
                fb.description(f"Spell={spell}: mid={mid}, {spell}*{sorted_potions[mid]}={product} < {success}")
                sp_ar.draw(fb.draw, states=sp_states)
                pt_ar.draw(fb.draw, states=pt_states,
                          pointers={mid: ("mid", Colors.ACCENT)})
                fb.label(50, 340, f"Too small, search right", Colors.RED)
                frames.append(fb.build())
                durations.append(DURATION_NORMAL)
                lo = mid + 1

        count = n - pos
        result.append(count)

        # Show result for this spell
        pt_states = {}
        for i in range(n):
            if i >= pos:
                pt_states[i] = CellState.FOUND
            else:
                pt_states[i] = CellState.INACTIVE
        fb = FrameBuilder()
        fb.title("#2300 Spells and Potions")
        fb.description(f"Spell={spell}: {count} valid potions")
        sp_ar.draw(fb.draw, states=sp_states)
        pt_ar.draw(fb.draw, states=pt_states)
        fb.label(50, 340, f"Result so far: {result}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final
    fb = FrameBuilder()
    fb.title("#2300 Spells and Potions")
    fb.description("All spells processed!")
    sp_ar.draw(fb.draw, states={i: CellState.FOUND for i in range(len(spells))})
    pt_ar.draw(fb.draw)
    fb.result_banner(f"Result: {result}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = spells_and_potions([5, 1, 3], [1, 2, 3, 4, 5], 7)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
