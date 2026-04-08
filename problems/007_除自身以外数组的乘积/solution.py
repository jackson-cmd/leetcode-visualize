import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def product_except_self_viz(nums):
    """Visualize Product of Array Except Self with left/right passes."""
    frames = []
    durations = []
    n = len(nums)

    arr = ArrayRenderer(nums, y=110, label="nums[]")
    left_arr = ArrayRenderer([1] * n, y=220, label="left[]")
    right_arr = ArrayRenderer([1] * n, y=330, label="right[]")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#238 Product Except Self")
    fb.description(f"nums = {nums}")
    arr.draw(fb.draw, states={})
    left_arr.draw(fb.draw, states={}, values_override=[1] * n)
    right_arr.draw(fb.draw, states={}, values_override=[1] * n)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Left pass: left[i] = product of all elements to the left of i
    left = [1] * n
    for i in range(1, n):
        left[i] = left[i - 1] * nums[i - 1]

        states_arr = {i: CellState.CURRENT}
        if i - 1 >= 0:
            states_arr[i - 1] = CellState.CHECKING
        for j in range(i - 1):
            states_arr[j] = CellState.FOUND

        states_left = {i: CellState.CURRENT}
        for j in range(i):
            states_left[j] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#238 Product Except Self")
        fb.description(f"Left pass: left[{i}] = left[{i-1}] * nums[{i-1}] = {left[i-1]} * {nums[i-1]} = {left[i]}")
        arr.draw(fb.draw, states=states_arr,
                 pointers={i: ("i", Colors.ACCENT)})
        left_arr.draw(fb.draw, states=states_left, values_override=left)
        right_arr.draw(fb.draw, states={}, values_override=[1] * n)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Show left pass complete
    fb = FrameBuilder()
    fb.title("#238 Product Except Self")
    fb.description(f"Left pass complete: {left}")
    arr.draw(fb.draw, states={})
    left_arr.draw(fb.draw,
                  states={i: CellState.FOUND for i in range(n)},
                  values_override=left)
    right_arr.draw(fb.draw, states={}, values_override=[1] * n)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Right pass: right[i] = product of all elements to the right of i
    right = [1] * n
    for i in range(n - 2, -1, -1):
        right[i] = right[i + 1] * nums[i + 1]

        states_arr = {i: CellState.CURRENT}
        if i + 1 < n:
            states_arr[i + 1] = CellState.CHECKING
        for j in range(i + 2, n):
            states_arr[j] = CellState.FOUND

        states_right = {i: CellState.CURRENT}
        for j in range(i + 1, n):
            states_right[j] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#238 Product Except Self")
        fb.description(f"Right pass: right[{i}] = right[{i+1}] * nums[{i+1}] = {right[i+1]} * {nums[i+1]} = {right[i]}")
        arr.draw(fb.draw, states=states_arr,
                 pointers={i: ("i", Colors.PEACH)})
        left_arr.draw(fb.draw,
                      states={j: CellState.FOUND for j in range(n)},
                      values_override=left)
        right_arr.draw(fb.draw, states=states_right, values_override=right)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Combine: result[i] = left[i] * right[i]
    result = [left[i] * right[i] for i in range(n)]
    fb = FrameBuilder()
    fb.title("#238 Product Except Self")
    fb.description("Combine: result[i] = left[i] * right[i]")
    arr.draw(fb.draw, states={})
    left_arr.draw(fb.draw,
                  states={i: CellState.FOUND for i in range(n)},
                  values_override=left)
    right_arr.draw(fb.draw,
                   states={i: CellState.FOUND for i in range(n)},
                   values_override=right)
    fb.label(50, 430, f"result = {result}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final frame
    result_arr = ArrayRenderer(result, y=220, label="result[]")
    fb = FrameBuilder()
    fb.title("#238 Product Except Self")
    fb.description("Done!")
    arr.draw(fb.draw, states={i: CellState.FOUND for i in range(n)})
    result_arr.draw(fb.draw,
                    states={i: CellState.FOUND for i in range(n)},
                    values_override=result)
    fb.result_banner(f"Result: {result}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = product_except_self_viz([1, 2, 3, 4])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
