"""
1732. 找到最高海拔
前缀和：从海拔 0 出发，依次累加 gain，记录最大海拔
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate_frames():
    gain = [-5, 1, 5, 0, -7]
    n = len(gain)
    altitudes = [0]  # altitude[0] = 0
    for g in gain:
        altitudes.append(altitudes[-1] + g)
    # altitudes = [0, -5, -4, 1, 1, -6]

    gain_arr = ArrayRenderer(gain, y=110, cell_w=60, cell_h=52, label="gain[]")
    alt_arr = ArrayRenderer([None] * (n + 1), y=260, cell_w=60, cell_h=52,
                            label="altitude[]")

    # Frame 1: show gain array and empty altitude
    def draw_init(fb):
        gain_arr.draw(fb.draw)
        alt_vals = [None] * (n + 1)
        alt_vals[0] = 0
        alt_arr.draw(fb.draw, values_override=alt_vals)
        fb.label(30, 480, "altitude[0] = 0, max_alt = 0", Colors.TEXT)
    yield "初始状态：海拔从 0 开始", draw_init, DURATION_NORMAL

    current_alt = 0
    max_alt = 0

    for i in range(n):
        current_alt += gain[i]
        max_alt = max(max_alt, current_alt)

        # Build altitude display
        alt_vals = [None] * (n + 1)
        alt_vals[0] = 0
        for j in range(i + 1):
            alt_vals[j + 1] = altitudes[j + 1]

        gain_states = {i: CellState.CURRENT}
        alt_states = {i + 1: CellState.CURRENT}

        # Highlight the max altitude cell
        for j in range(i + 2):
            if alt_vals[j] is not None and alt_vals[j] == max_alt:
                alt_states[j] = CellState.FOUND

        gain_ptrs = {i: ("i", Colors.ACCENT)}

        cur_a = current_alt
        cur_m = max_alt
        cur_g = gain[i]
        def draw_step(fb, gs=gain_states, als=alt_states, av=alt_vals,
                      gp=gain_ptrs, idx=i, ca=cur_a, cm=cur_m, cg=cur_g):
            gain_arr.draw(fb.draw, states=gs, pointers=gp)
            alt_arr.draw(fb.draw, states=als, values_override=av)
            # Draw arrow showing addition
            gx, _ = gain_arr.cell_bottom(idx)
            ax, _ = alt_arr.cell_top(idx + 1)
            draw_arrow(fb.draw, gx, gain_arr.y + gain_arr.cell_h + 5,
                       ax, alt_arr.y - 5, Colors.YELLOW)
            info = f"altitude[{idx+1}] = altitude[{idx}] + gain[{idx}] = {ca}, max_alt = {cm}"
            fb.label(30, 480, info, Colors.TEXT)
        yield f"加上 gain[{i}]={gain[i]}", draw_step, DURATION_NORMAL

    # Final result
    final_alt_states = {}
    for j in range(n + 1):
        if altitudes[j] == max(altitudes):
            final_alt_states[j] = CellState.FOUND
        else:
            final_alt_states[j] = CellState.DEFAULT
    final_max = max(altitudes)
    def draw_result(fb):
        gain_arr.draw(fb.draw, states={i: CellState.INACTIVE for i in range(n)})
        alt_arr.draw(fb.draw, states=final_alt_states,
                     values_override=altitudes)
        fb.result_banner(f"最高海拔 = {final_max}")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1732. 找到最高海拔", generate_frames, out)
