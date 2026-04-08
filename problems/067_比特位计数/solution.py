"""
338. 比特位计数 — 可视化
BitRenderer + DPTableRenderer 展示 dp[i] = dp[i>>1] + (i&1) 的递推过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    n = 5
    dp = [0] * (n + 1)

    dp_renderer = DPTableRenderer(rows=1, cols=n + 1, y=380, cell_size=70,
                                   canvas_width=WIDTH, label="dp[i] = i的二进制中1的个数")
    bit_renderer = BitRenderer(num_bits=4, y=150, canvas_width=WIDTH, label="当前数字的二进制")
    shift_renderer = BitRenderer(num_bits=4, y=250, canvas_width=WIDTH, label="i >> 1 的二进制")

    col_labels = [str(i) for i in range(n + 1)]

    # Frame 1: initial
    def draw_init(fb):
        vals = [None] * (n + 1)
        vals[0] = 0
        dp_renderer.draw(fb.draw, vals, col_labels=col_labels)
        fb.label(30, 460, "dp[i] = dp[i>>1] + (i&1)", Colors.SUBTEXT)
    yield "初始化: dp[0]=0", draw_init, DURATION_NORMAL

    dp[0] = 0
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)

        def make_draw(ci, snap):
            def draw_fn(fb):
                # Show current number in binary
                bit_states = {}
                if ci & 1:
                    bit_states[0] = CellState.CHECKING  # LSB highlighted
                bit_renderer.draw(fb.draw, ci, bit_states=bit_states)
                fb.label(30, 130, f"i = {ci}", Colors.ACCENT)

                # Show i>>1 in binary
                shift_renderer.draw(fb.draw, ci >> 1)
                fb.label(30, 230, f"i>>1 = {ci >> 1}", Colors.PEACH)

                # Show DP table
                vals = list(snap)
                for j in range(ci + 1, n + 1):
                    vals[j] = None
                dp_states = {ci: CellState.CURRENT}
                if ci >> 1 <= ci:
                    dp_states[ci >> 1] = CellState.CHECKING
                for j in range(ci):
                    if j not in dp_states:
                        dp_states[j] = CellState.FOUND
                dp_renderer.draw(fb.draw, vals, states=dp_states,
                                 col_labels=col_labels)

                lsb = ci & 1
                fb.label(30, 460,
                         f"dp[{ci}] = dp[{ci}>>1] + ({ci}&1) = dp[{ci>>1}] + {lsb} = {snap[ci>>1]} + {lsb} = {snap[ci]}",
                         Colors.YELLOW)
            return draw_fn

        snap = dp[:]
        yield (f"i={i}: dp[{i}] = dp[{i>>1}] + {i&1} = {dp[i]}",
               make_draw(i, snap), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        dp_states = {i: CellState.FOUND for i in range(n + 1)}
        dp_renderer.draw(fb.draw, dp, states=dp_states,
                         col_labels=col_labels)
        fb.result_banner(f"countBits({n}) = {dp}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("338. 比特位计数", generate, output_path)
