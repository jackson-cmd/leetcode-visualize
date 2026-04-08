"""
643. 子数组最大平均数 I — 可视化
使用 ArrayRenderer + 滑动窗口展示定长窗口滑动求最大平均数。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    nums = [1, 12, -5, -6, 50, 3]
    k = 4
    n = len(nums)

    # Frame 1: initial array
    def draw_init(fb):
        r = ArrayRenderer(nums, y=160, cell_w=65, canvas_width=WIDTH)
        r.draw(fb.draw)
        fb.label(30, 280, f"数组长度={n}, 窗口大小 k={k}", Colors.YELLOW)
    yield f"初始数组, k={k}", draw_init, DURATION_NORMAL

    # Compute initial window sum
    # Show building up the initial window step by step
    partial_sum = 0
    for step in range(k):
        partial_sum += nums[step]

        def draw_build(fb, s=step, ps=partial_sum):
            r = ArrayRenderer(nums, y=160, cell_w=65, canvas_width=WIDTH)
            states = {}
            for j in range(s + 1):
                states[j] = CellState.WINDOW
            states[s] = CellState.CURRENT
            r.draw(fb.draw, states=states, window=(0, s))
            fb.label(30, 280, f"构建初始窗口: 加入 nums[{s}]={nums[s]}", Colors.TEAL)
            fb.label(30, 310, f"当前窗口和 = {ps}", Colors.TEXT)
        yield f"加入 nums[{step}]={nums[step]}", draw_build, DURATION_NORMAL

    window_sum = partial_sum
    best_sum = window_sum
    best_start = 0

    # Frame: first complete window
    def draw_first_window(fb, ws=window_sum):
        r = ArrayRenderer(nums, y=160, cell_w=65, canvas_width=WIDTH)
        states = {i: CellState.WINDOW for i in range(k)}
        r.draw(fb.draw, states=states, window=(0, k - 1))
        avg = ws / k
        fb.label(30, 280, f"初始窗口 [0..{k-1}]: 和={ws}, 平均={avg:.2f}", Colors.TEAL)
        fb.label(30, 310, f"最大平均数 = {avg:.2f}", Colors.GREEN)
    yield f"初始窗口完成, 和={window_sum}", draw_first_window, DURATION_NORMAL

    # Slide the window
    for i in range(k, n):
        old_val = nums[i - k]
        new_val = nums[i]
        window_sum = window_sum - old_val + new_val
        start = i - k + 1
        end = i

        is_best = window_sum > best_sum
        if is_best:
            best_sum = window_sum
            best_start = start

        # Show removing old element
        def draw_remove(fb, s=start, e=end, ov=old_val, ws=window_sum + old_val - new_val):
            r = ArrayRenderer(nums, y=160, cell_w=65, canvas_width=WIDTH)
            states = {}
            for j in range(s - 1, e + 1):
                states[j] = CellState.WINDOW
            states[s - 1] = CellState.REMOVED
            r.draw(fb.draw, states=states)
            fb.label(30, 280, f"移除 nums[{s-1}]={ov}", Colors.RED)
        yield f"移除 {old_val}", draw_remove, DURATION_FAST

        # Show adding new element
        def draw_add(fb, s=start, e=end, nv=new_val, ws=window_sum, bs=best_sum, ib=is_best):
            r = ArrayRenderer(nums, y=160, cell_w=65, canvas_width=WIDTH)
            states = {}
            for j in range(s, e + 1):
                states[j] = CellState.WINDOW
            states[e] = CellState.CURRENT
            r.draw(fb.draw, states=states, window=(s, e))
            avg = ws / k
            best_avg = bs / k
            fb.label(30, 280, f"加入 nums[{e}]={nv} => 窗口和={ws}, 平均={avg:.2f}", Colors.TEAL)
            color = Colors.GREEN if ib else Colors.YELLOW
            fb.label(30, 310, f"最大平均数 = {best_avg:.2f}" +
                     (" (更新!)" if ib else ""), color)
        yield f"加入 {new_val}, 窗口[{start}..{end}]", draw_add, DURATION_NORMAL

    # Final
    best_avg = best_sum / k
    def draw_final(fb, bs=best_start, ba=best_avg):
        r = ArrayRenderer(nums, y=160, cell_w=65, canvas_width=WIDTH)
        states = {i: CellState.FOUND for i in range(bs, bs + k)}
        r.draw(fb.draw, states=states, window=(bs, bs + k - 1))
        fb.result_banner(f"最大平均数 = {ba:.2f}")
    yield "计算完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("643. 子数组最大平均数 I", generate, output_path)
