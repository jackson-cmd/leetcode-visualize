import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def tribonacci(n):
    """Tribonacci sequence with DP table visualization."""
    frames = []
    durations = []

    target_n = n
    dp = [0] * (target_n + 1)
    dp[0] = 0
    if target_n >= 1:
        dp[1] = 1
    if target_n >= 2:
        dp[2] = 1

    # We'll show all values as we fill them
    display_vals = [None] * (target_n + 1)

    cell_sz = min(60, (WIDTH - 80) // (target_n + 1))
    dp_renderer = DPTableRenderer(rows=1, cols=target_n + 1, y=160, cell_size=cell_sz,
                                   canvas_width=WIDTH, label="dp[]")
    col_labels = list(range(target_n + 1))

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#1137 N-th Tribonacci Number")
    fb.description(f"T(n) = T(n-1) + T(n-2) + T(n-3), find T({target_n})")
    dp_renderer.draw(fb.draw, display_vals, col_labels=col_labels)
    fb.label(50, 300, "T(0)=0, T(1)=1, T(2)=1", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Base cases
    display_vals[0] = 0
    if target_n >= 1:
        display_vals[1] = 1
    if target_n >= 2:
        display_vals[2] = 1

    base_states = {}
    base_states[0] = CellState.FOUND
    if target_n >= 1:
        base_states[1] = CellState.FOUND
    if target_n >= 2:
        base_states[2] = CellState.FOUND

    fb = FrameBuilder()
    fb.title("#1137 N-th Tribonacci Number")
    fb.description("Base cases: T(0)=0, T(1)=1, T(2)=1")
    dp_renderer.draw(fb.draw, display_vals, states=base_states, col_labels=col_labels)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Fill DP
    for i in range(3, target_n + 1):
        dp[i] = dp[i - 1] + dp[i - 2] + dp[i - 3]
        display_vals[i] = dp[i]

        states = {}
        for j in range(i):
            states[j] = CellState.FOUND
        states[i] = CellState.CURRENT
        states[i - 1] = CellState.CHECKING
        states[i - 2] = CellState.CHECKING
        states[i - 3] = CellState.CHECKING

        # Dependency arrows (in 1D, arrows are (0, from_col) -> (0, to_col))
        arrows = [
            ((0, i - 1), (0, i)),
            ((0, i - 2), (0, i)),
            ((0, i - 3), (0, i)),
        ]

        fb = FrameBuilder()
        fb.title("#1137 N-th Tribonacci Number")
        fb.description(f"T({i}) = T({i-1}) + T({i-2}) + T({i-3}) = {dp[i-1]} + {dp[i-2]} + {dp[i-3]} = {dp[i]}")
        dp_renderer.draw(fb.draw, display_vals, states=states,
                        arrows=arrows, col_labels=col_labels)
        fb.label(50, 300, f"Computing dp[{i}] from three predecessors", Colors.YELLOW)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    final_states = {i: CellState.FOUND for i in range(target_n + 1)}
    final_states[target_n] = CellState.FOUND

    fb = FrameBuilder()
    fb.title("#1137 N-th Tribonacci Number")
    fb.description("Complete!")
    dp_renderer.draw(fb.draw, display_vals, states=final_states, col_labels=col_labels)
    fb.result_banner(f"Result: T({target_n}) = {dp[target_n]}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = tribonacci(10)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
