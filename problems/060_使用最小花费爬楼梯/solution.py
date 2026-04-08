import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def min_cost_climbing_stairs(cost):
    """Min cost climbing stairs with DP visualization."""
    frames = []
    durations = []

    n = len(cost)
    dp = [0] * (n + 1)

    cell_w = min(70, (WIDTH - 80) // max(n + 1, n))
    cost_ar = ArrayRenderer(cost, y=110, cell_w=cell_w, cell_h=44, label="cost[]")
    dp_vals = [None] * (n + 1)
    dp_labels = list(range(n + 1))
    dp_renderer = DPTableRenderer(rows=1, cols=n + 1, y=240, cell_size=cell_w,
                                   canvas_width=WIDTH, label="dp[] (min cost to reach step i)")

    # Frame 0: Problem setup
    fb = FrameBuilder()
    fb.title("#746 Min Cost Climbing Stairs")
    fb.description(f"cost = {cost}")
    cost_ar.draw(fb.draw)
    dp_renderer.draw(fb.draw, dp_vals, col_labels=dp_labels)
    fb.label(50, 370, "Can start from step 0 or 1. Climb 1 or 2 steps each time.", Colors.TEXT)
    fb.label(50, 400, "dp[i] = min(dp[i-1]+cost[i-1], dp[i-2]+cost[i-2])", Colors.YELLOW)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Base cases
    dp[0] = 0
    dp[1] = 0
    dp_vals[0] = 0
    dp_vals[1] = 0

    fb = FrameBuilder()
    fb.title("#746 Min Cost Climbing Stairs")
    fb.description("Base: dp[0]=0, dp[1]=0 (start free)")
    cost_ar.draw(fb.draw)
    dp_renderer.draw(fb.draw, dp_vals,
                    states={0: CellState.FOUND, 1: CellState.FOUND},
                    col_labels=dp_labels)
    fb.label(50, 370, "Can start at step 0 or step 1 for free", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Fill DP
    for i in range(2, n + 1):
        opt1 = dp[i - 1] + cost[i - 1]
        opt2 = dp[i - 2] + cost[i - 2]
        dp[i] = min(opt1, opt2)
        dp_vals[i] = dp[i]

        states = {}
        for j in range(i):
            states[j] = CellState.FOUND
        states[i] = CellState.CURRENT
        states[i - 1] = CellState.CHECKING
        states[i - 2] = CellState.CHECKING

        arrows = [
            ((0, i - 1), (0, i)),
            ((0, i - 2), (0, i)),
        ]

        cost_states = {}
        if i - 1 < n:
            cost_states[i - 1] = CellState.CHECKING
        if i - 2 < n:
            cost_states[i - 2] = CellState.CHECKING

        chosen = "from step " + str(i - 1) if opt1 <= opt2 else "from step " + str(i - 2)

        fb = FrameBuilder()
        fb.title("#746 Min Cost Climbing Stairs")
        fb.description(f"dp[{i}] = min(dp[{i-1}]+cost[{i-1}], dp[{i-2}]+cost[{i-2}])")
        cost_ar.draw(fb.draw, states=cost_states)
        dp_renderer.draw(fb.draw, dp_vals, states=states,
                        arrows=arrows, col_labels=dp_labels)
        fb.label(50, 370, f"= min({dp[i-1]}+{cost[i-1]}, {dp[i-2]}+{cost[i-2]}) = min({opt1}, {opt2}) = {dp[i]}", Colors.YELLOW)
        fb.label(50, 400, f"Best path: come {chosen}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Trace optimal path
    path = [n]
    i = n
    while i > 1:
        if i - 2 >= 0 and dp[i] == dp[i - 2] + cost[i - 2]:
            path.append(i - 2)
            i -= 2
        else:
            path.append(i - 1)
            i -= 1
    path.reverse()

    # Show optimal path
    dp_path_states = {j: CellState.INACTIVE for j in range(n + 1)}
    for p in path:
        dp_path_states[p] = CellState.FOUND

    fb = FrameBuilder()
    fb.title("#746 Min Cost Climbing Stairs")
    fb.description(f"Optimal path: steps {path}")
    cost_ar.draw(fb.draw)
    dp_renderer.draw(fb.draw, dp_vals, states=dp_path_states, col_labels=dp_labels)
    fb.label(50, 370, f"Follow the minimum cost path to the top", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#746 Min Cost Climbing Stairs")
    fb.description("Complete!")
    final_states = {i: CellState.FOUND for i in range(n + 1)}
    cost_ar.draw(fb.draw)
    dp_renderer.draw(fb.draw, dp_vals, states=final_states, col_labels=dp_labels)
    fb.result_banner(f"Result: min cost = {dp[n]}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = min_cost_climbing_stairs([1, 100, 1, 1, 1, 100, 1, 1, 100, 1])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
