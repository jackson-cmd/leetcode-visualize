import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def domino_tromino_tiling(n):
    """Domino and tromino tiling DP visualization."""
    frames = []
    durations = []

    MOD = 10**9 + 7
    target = n

    dp = [0] * (target + 1)
    dp[0] = 1
    if target >= 1:
        dp[1] = 1
    if target >= 2:
        dp[2] = 2

    dp_vals = [None] * (target + 1)
    dp_labels = list(range(target + 1))
    cell_sz = min(70, (WIDTH - 80) // (target + 1))
    dp_renderer = DPTableRenderer(rows=1, cols=target + 1, y=160, cell_size=cell_sz,
                                   canvas_width=WIDTH, label="dp[] (ways to tile 2xi)")

    font = get_font(16)

    # Frame 0: Problem
    fb = FrameBuilder()
    fb.title("#790 Domino and Tromino Tiling")
    fb.description(f"Tile a 2 x {target} board with dominoes and trominoes")
    dp_renderer.draw(fb.draw, dp_vals, col_labels=dp_labels)
    fb.label(50, 290, "Domino: 2x1 or 1x2 rectangle", Colors.TEXT)
    fb.label(50, 320, "Tromino: L-shaped (covers 3 cells)", Colors.TEXT)
    # Draw small tile shapes
    draw_rounded_rect(fb.draw, (400, 285, 430, 325), 4, fill=Colors.ACCENT, outline=Colors.TEXT)
    draw_rounded_rect(fb.draw, (440, 285, 500, 305), 4, fill=Colors.TEAL, outline=Colors.TEXT)
    draw_rounded_rect(fb.draw, (400, 340, 430, 380), 4, fill=Colors.MAUVE, outline=Colors.TEXT)
    draw_rounded_rect(fb.draw, (430, 360, 460, 380), 4, fill=Colors.MAUVE, outline=Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Recurrence
    fb = FrameBuilder()
    fb.title("#790 Domino and Tromino Tiling")
    fb.description("Recurrence: dp[i] = 2*dp[i-1] + dp[i-3]")
    dp_renderer.draw(fb.draw, dp_vals, col_labels=dp_labels)
    fb.label(50, 290, "2*dp[i-1]: place vertical domino, or two horizontal dominoes", Colors.ACCENT)
    fb.label(50, 320, "dp[i-3]: place a pair of trominoes covering 3 columns", Colors.MAUVE)
    fb.label(50, 350, "This accounts for all distinct tiling patterns", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Base cases
    dp_vals[0] = 1
    if target >= 1:
        dp_vals[1] = 1
    if target >= 2:
        dp_vals[2] = 2

    base_states = {0: CellState.FOUND}
    if target >= 1:
        base_states[1] = CellState.FOUND
    if target >= 2:
        base_states[2] = CellState.FOUND

    fb = FrameBuilder()
    fb.title("#790 Domino and Tromino Tiling")
    fb.description("Base: dp[0]=1, dp[1]=1, dp[2]=2")
    dp_renderer.draw(fb.draw, dp_vals, states=base_states, col_labels=dp_labels)
    fb.label(50, 290, "dp[0]=1 (empty board, 1 way)", Colors.TEXT)
    fb.label(50, 320, "dp[1]=1 (one vertical domino)", Colors.TEXT)
    fb.label(50, 350, "dp[2]=2 (two vertical or two horizontal)", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Visual tiles for n=2
    fb = FrameBuilder()
    fb.title("#790 Domino and Tromino Tiling")
    fb.description("dp[2] = 2: two ways to tile 2x2")
    dp_renderer.draw(fb.draw, dp_vals, states=base_states, col_labels=dp_labels)
    tile_x, tile_y = 150, 300
    draw_rounded_rect(fb.draw, (tile_x, tile_y, tile_x+30, tile_y+64), 4,
                     fill=Colors.ACCENT, outline=Colors.TEXT)
    draw_rounded_rect(fb.draw, (tile_x+34, tile_y, tile_x+64, tile_y+64), 4,
                     fill=Colors.TEAL, outline=Colors.TEXT)
    fb.label(tile_x + 10, tile_y + 70, "Way 1", Colors.SUBTEXT)
    tile_x2 = 350
    draw_rounded_rect(fb.draw, (tile_x2, tile_y, tile_x2+64, tile_y+28), 4,
                     fill=Colors.PEACH, outline=Colors.TEXT)
    draw_rounded_rect(fb.draw, (tile_x2, tile_y+32, tile_x2+64, tile_y+64), 4,
                     fill=Colors.MAUVE, outline=Colors.TEXT)
    fb.label(tile_x2 + 10, tile_y + 70, "Way 2", Colors.SUBTEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Fill DP for i >= 3
    for i in range(3, target + 1):
        dp[i] = (2 * dp[i - 1] + dp[i - 3]) % MOD
        dp_vals[i] = dp[i]

        # Frame: show which cells we're looking at
        states_pre = {j: CellState.FOUND for j in range(i)}
        states_pre[i - 1] = CellState.CHECKING
        if i - 3 >= 0:
            states_pre[i - 3] = CellState.CHECKING

        fb = FrameBuilder()
        fb.title("#790 Domino and Tromino Tiling")
        fb.description(f"Computing dp[{i}]: need dp[{i-1}] and dp[{i-3}]")
        dp_renderer.draw(fb.draw, dp_vals, states=states_pre, col_labels=dp_labels)
        fb.label(50, 290, f"dp[{i-1}] = {dp[i-1]}, dp[{i-3}] = {dp[i-3]}", Colors.YELLOW)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Frame: show the calculation result
        states = {j: CellState.FOUND for j in range(i)}
        states[i] = CellState.CURRENT
        states[i - 1] = CellState.CHECKING
        if i - 3 >= 0:
            states[i - 3] = CellState.CHECKING

        arrows = [((0, i - 1), (0, i))]
        if i - 3 >= 0:
            arrows.append(((0, i - 3), (0, i)))

        fb = FrameBuilder()
        fb.title("#790 Domino and Tromino Tiling")
        fb.description(f"dp[{i}] = 2*{dp[i-1]} + {dp[i-3]} = {dp[i]}")
        dp_renderer.draw(fb.draw, dp_vals, states=states,
                        arrows=arrows, col_labels=dp_labels)
        fb.label(50, 290, f"2*dp[{i-1}] = {2*dp[i-1]} (domino extensions)", Colors.ACCENT)
        fb.label(50, 320, f"dp[{i-3}] = {dp[i-3]} (tromino pair)", Colors.MAUVE)
        fb.label(50, 350, f"Total: {dp[i]} ways", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Summary
    fb = FrameBuilder()
    fb.title("#790 Domino and Tromino Tiling")
    fb.description("All values computed!")
    final_states = {i: CellState.FOUND for i in range(target + 1)}
    dp_renderer.draw(fb.draw, dp_vals, states=final_states, col_labels=dp_labels)
    fb.label(50, 290, "Sequence: " + ", ".join([str(dp[i]) for i in range(target + 1)]), Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#790 Domino and Tromino Tiling")
    fb.description("Complete!")
    dp_renderer.draw(fb.draw, dp_vals, states=final_states, col_labels=dp_labels)
    fb.result_banner(f"Result: dp[{target}] = {dp[target]}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = domino_tromino_tiling(5)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
