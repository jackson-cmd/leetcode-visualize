import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def house_robber(nums):
    """House robber DP visualization with array + dp table."""
    frames = []
    durations = []

    n = len(nums)
    cell_w = min(60, (WIDTH - 80) // n)
    house_ar = ArrayRenderer(nums, y=110, cell_w=cell_w, cell_h=48, label="houses (value)")
    dp = [0] * n
    dp_vals = [None] * n
    dp_renderer = DPTableRenderer(rows=1, cols=n, y=260, cell_size=cell_w,
                                   canvas_width=WIDTH, label="dp[] (max rob up to house i)")
    dp_labels = list(range(n))

    # Frame 0: Problem setup
    fb = FrameBuilder()
    fb.title("#198 House Robber")
    fb.description(f"nums = {nums}")
    house_ar.draw(fb.draw)
    dp_renderer.draw(fb.draw, dp_vals, col_labels=dp_labels)
    fb.label(50, 380, "Rule: can't rob two adjacent houses", Colors.TEXT)
    fb.label(50, 410, "dp[i] = max(dp[i-1], dp[i-2]+nums[i])", Colors.YELLOW)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Show adjacent constraint visually
    fb = FrameBuilder()
    fb.title("#198 House Robber")
    fb.description("Adjacent houses cannot both be robbed")
    adj_states = {0: CellState.FOUND, 1: CellState.REMOVED, 2: CellState.FOUND,
                  3: CellState.REMOVED, 4: CellState.FOUND}
    house_ar.draw(fb.draw, states=adj_states)
    dp_renderer.draw(fb.draw, dp_vals, col_labels=dp_labels)
    fb.label(50, 380, "Green = rob, Red = must skip (adjacent)", Colors.TEXT)
    fb.label(50, 410, "Need DP to find the optimal combination", Colors.YELLOW)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Explain the choice
    fb = FrameBuilder()
    fb.title("#198 House Robber")
    fb.description("At each house: rob it or skip it?")
    house_ar.draw(fb.draw)
    dp_renderer.draw(fb.draw, dp_vals, col_labels=dp_labels)
    fb.label(50, 380, "Skip house i: dp[i] = dp[i-1] (keep previous best)", Colors.SKY)
    fb.label(50, 410, "Rob house i: dp[i] = dp[i-2] + nums[i] (skip adjacent)", Colors.PEACH)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Base case: dp[0]
    dp[0] = nums[0]
    dp_vals[0] = dp[0]

    fb = FrameBuilder()
    fb.title("#198 House Robber")
    fb.description(f"Base: dp[0] = nums[0] = {nums[0]}")
    house_ar.draw(fb.draw, states={0: CellState.CURRENT})
    dp_renderer.draw(fb.draw, dp_vals, states={0: CellState.FOUND}, col_labels=dp_labels)
    fb.label(50, 380, f"Only one house: rob it for {nums[0]}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Base case: dp[1]
    if n >= 2:
        dp[1] = max(nums[0], nums[1])
        dp_vals[1] = dp[1]

        fb = FrameBuilder()
        fb.title("#198 House Robber")
        fb.description(f"Base: dp[1] = max({nums[0]}, {nums[1]}) = {dp[1]}")
        h_states = {0: CellState.CHECKING, 1: CellState.CHECKING}
        house_ar.draw(fb.draw, states=h_states)
        dp_renderer.draw(fb.draw, dp_vals,
                        states={0: CellState.FOUND, 1: CellState.FOUND},
                        col_labels=dp_labels)
        fb.label(50, 380, f"Two houses: rob the more valuable one", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Fill DP
    for i in range(2, n):
        skip = dp[i - 1]
        rob = dp[i - 2] + nums[i]
        dp[i] = max(skip, rob)
        dp_vals[i] = dp[i]

        chose_rob = rob >= skip

        # Show the two options
        dp_states = {j: CellState.FOUND for j in range(i)}
        dp_states[i] = CellState.CURRENT

        h_states = {i: CellState.CURRENT}

        fb = FrameBuilder()
        fb.title("#198 House Robber")
        fb.description(f"House {i}: skip (dp[{i-1}]={skip}) or rob (dp[{i-2}]+{nums[i]}={rob})?")
        house_ar.draw(fb.draw, states=h_states)
        dp_states_show = dict(dp_states)
        dp_states_show[i - 1] = CellState.LEFT_PTR
        dp_states_show[i - 2] = CellState.RIGHT_PTR
        arrows = [((0, i - 1), (0, i)), ((0, i - 2), (0, i))]
        dp_renderer.draw(fb.draw, dp_vals, states=dp_states_show,
                        arrows=arrows, col_labels=dp_labels)
        action = "ROB" if chose_rob else "SKIP"
        fb.label(50, 380,
                f"max({skip}, {rob}) = {dp[i]} -> {action} house {i}",
                Colors.GREEN if chose_rob else Colors.PEACH)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Trace back which houses to rob
    robbed = []
    i = n - 1
    while i >= 0:
        if i == 0 or dp[i] != dp[i - 1]:
            robbed.append(i)
            i -= 2
        else:
            i -= 1
    robbed.reverse()

    # Show the decision for each house
    h_states = {}
    for i in range(n):
        if i in robbed:
            h_states[i] = CellState.FOUND
        else:
            h_states[i] = CellState.INACTIVE

    fb = FrameBuilder()
    fb.title("#198 House Robber")
    fb.description(f"Optimal: rob houses {robbed}")
    house_ar.draw(fb.draw, states=h_states)
    dp_renderer.draw(fb.draw, dp_vals,
                    states={i: CellState.FOUND for i in range(n)},
                    col_labels=dp_labels)
    total = sum(nums[i] for i in robbed)
    fb.label(50, 380, f"Rob: {' + '.join(str(nums[i]) for i in robbed)} = {total}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final
    fb = FrameBuilder()
    fb.title("#198 House Robber")
    fb.description("Maximum robbery value found!")
    house_ar.draw(fb.draw, states=h_states)
    dp_renderer.draw(fb.draw, dp_vals,
                    states={i: CellState.FOUND for i in range(n)},
                    col_labels=dp_labels)
    fb.result_banner(f"Result: {dp[n-1]}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = house_robber([2, 7, 9, 3, 1])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
