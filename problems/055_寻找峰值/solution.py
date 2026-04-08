import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def find_peak_element(nums):
    """Binary search for peak element, visualized."""
    frames = []
    durations = []

    ar = ArrayRenderer(nums, y=160, cell_w=55, cell_h=52)

    # Frame 0: Problem setup
    fb = FrameBuilder()
    fb.title("#162 Find Peak Element")
    fb.description(f"nums = {nums}")
    ar.draw(fb.draw)
    fb.label(50, 300, "Peak: element greater than its neighbors", Colors.TEXT)
    fb.label(50, 330, "Assume nums[-1] = nums[n] = -inf", Colors.SUBTEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Explain binary search approach
    fb = FrameBuilder()
    fb.title("#162 Find Peak Element")
    fb.description("Key insight: if nums[mid] < nums[mid+1], peak is on the right")
    ar.draw(fb.draw, states={i: CellState.WINDOW for i in range(len(nums))})
    fb.label(50, 300, "Going uphill means there must be a peak ahead", Colors.YELLOW)
    fb.label(50, 330, "Binary search: compare mid with mid+1", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    lo, hi = 0, len(nums) - 1
    step = 0

    while lo < hi:
        mid = (lo + hi) // 2
        step += 1

        states = {}
        for i in range(len(nums)):
            if i < lo or i > hi:
                states[i] = CellState.INACTIVE
            elif i == mid:
                states[i] = CellState.CURRENT
            elif i == mid + 1:
                states[i] = CellState.CHECKING
            else:
                states[i] = CellState.WINDOW

        pointers = {
            lo: ("lo", Colors.SKY),
            hi: ("hi", Colors.PEACH),
            mid: ("mid", Colors.ACCENT),
        }

        # Frame: Show mid calculation
        fb = FrameBuilder()
        fb.title("#162 Find Peak Element")
        fb.description(f"Step {step}: lo={lo}, hi={hi}, mid={mid}")
        ar.draw(fb.draw, states=states, pointers=pointers)
        fb.label(50, 300, f"Compare nums[{mid}]={nums[mid]} vs nums[{mid+1}]={nums[mid+1]}", Colors.YELLOW)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        if nums[mid] < nums[mid + 1]:
            # Frame: decision
            fb = FrameBuilder()
            fb.title("#162 Find Peak Element")
            fb.description(f"nums[{mid}]={nums[mid]} < nums[{mid+1}]={nums[mid+1]}: go right")
            # Mark eliminated region
            elim_states = dict(states)
            for i in range(lo, mid + 1):
                elim_states[i] = CellState.REMOVED
            ar.draw(fb.draw, states=elim_states, pointers=pointers)
            fb.label(50, 300, f"Ascending slope -> peak must be to the right", Colors.PEACH)
            fb.label(50, 330, f"Set lo = {mid + 1}", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            lo = mid + 1
        else:
            fb = FrameBuilder()
            fb.title("#162 Find Peak Element")
            fb.description(f"nums[{mid}]={nums[mid]} >= nums[{mid+1}]={nums[mid+1]}: go left")
            elim_states = dict(states)
            for i in range(mid + 1, hi + 1):
                elim_states[i] = CellState.REMOVED
            ar.draw(fb.draw, states=elim_states, pointers=pointers)
            fb.label(50, 300, f"Descending slope -> peak is at mid or left", Colors.SKY)
            fb.label(50, 330, f"Set hi = {mid}", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            hi = mid

        # Show narrowed range
        new_states = {}
        for i in range(len(nums)):
            if i < lo or i > hi:
                new_states[i] = CellState.INACTIVE
            else:
                new_states[i] = CellState.WINDOW
        fb = FrameBuilder()
        fb.title("#162 Find Peak Element")
        fb.description(f"Narrowed: [{lo}..{hi}], {hi - lo + 1} elements remain")
        ar.draw(fb.draw, states=new_states,
               pointers={lo: ("lo", Colors.SKY), hi: ("hi", Colors.PEACH)})
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Show the found peak
    peak_idx = lo
    states = {i: CellState.INACTIVE for i in range(len(nums))}
    states[peak_idx] = CellState.FOUND

    fb = FrameBuilder()
    fb.title("#162 Find Peak Element")
    fb.description(f"lo == hi == {peak_idx}: peak found!")
    ar.draw(fb.draw, states=states, pointers={peak_idx: ("peak", Colors.GREEN)})
    fb.label(50, 300, f"nums[{peak_idx}] = {nums[peak_idx]} is a peak element", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Verify neighbors
    fb = FrameBuilder()
    fb.title("#162 Find Peak Element")
    fb.description("Verify: peak > both neighbors")
    verify_states = {i: CellState.INACTIVE for i in range(len(nums))}
    verify_states[peak_idx] = CellState.FOUND
    if peak_idx > 0:
        verify_states[peak_idx - 1] = CellState.CHECKING
    if peak_idx < len(nums) - 1:
        verify_states[peak_idx + 1] = CellState.CHECKING
    ar.draw(fb.draw, states=verify_states, pointers={peak_idx: ("peak", Colors.GREEN)})
    left_val = nums[peak_idx - 1] if peak_idx > 0 else "-inf"
    right_val = nums[peak_idx + 1] if peak_idx < len(nums) - 1 else "-inf"
    fb.label(50, 300, f"Left={left_val} < {nums[peak_idx]} > {right_val}=Right", Colors.GREEN)
    fb.result_banner(f"Result: index = {peak_idx}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = find_peak_element([1, 2, 1, 3, 5, 6, 4])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
