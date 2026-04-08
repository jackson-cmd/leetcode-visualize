"""
724. 寻找数组的中心下标
前缀和：左侧和等于右侧和的下标
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate_frames():
    nums = [1, 7, 3, 6, 5, 6]
    n = len(nums)
    total = sum(nums)  # 28
    arr = ArrayRenderer(nums, y=130, cell_w=60, cell_h=52)

    # Frame 1: show array and total sum
    def draw_init(fb):
        arr.draw(fb.draw)
        fb.label(30, 480, f"total_sum = {total}", Colors.TEXT)
    yield "初始数组，计算总和", draw_init, DURATION_NORMAL

    left_sum = 0
    pivot_found = -1

    for i in range(n):
        right_sum = total - left_sum - nums[i]

        states = {}
        for j in range(n):
            if j < i:
                states[j] = CellState.LEFT_PTR
            elif j == i:
                states[j] = CellState.CURRENT
            else:
                states[j] = CellState.RIGHT_PTR

        is_pivot = (left_sum == right_sum)
        if is_pivot and pivot_found == -1:
            pivot_found = i
            states[i] = CellState.FOUND

        pointers = {i: ("pivot?", Colors.ACCENT)}
        ls = left_sum
        rs = right_sum
        idx = i
        found = is_pivot
        def draw_step(fb, s=states, p=pointers, l=ls, r=rs, ii=idx, f=found):
            arr.draw(fb.draw, states=s, pointers=p)
            # Draw left_sum label
            if ii > 0:
                lx1 = arr.x
                lx2 = arr.x + ii * (arr.cell_w + arr.spacing) - arr.spacing
                ly = arr.y + arr.cell_h + 45
                draw_bracket(fb.draw, lx1, lx2, ly, Colors.SKY,
                             f"left_sum={l}")
            # Draw right_sum label
            if ii < n - 1:
                rx1 = arr.x + (ii + 1) * (arr.cell_w + arr.spacing)
                rx2 = arr.x + n * (arr.cell_w + arr.spacing) - arr.spacing
                ry = arr.y + arr.cell_h + 45
                draw_bracket(fb.draw, rx1, rx2, ry, Colors.PEACH,
                             f"right_sum={r}")
            status = "FOUND!" if f else f"left_sum({l}) {'==' if f else '!='} right_sum({r})"
            fb.label(30, 480, f"i={ii}, nums[{ii}]={nums[ii]}, {status}", Colors.TEXT)
        desc = f"检查 i={i}: left_sum={ls}, right_sum={rs}"
        yield desc, draw_step, DURATION_NORMAL

        left_sum += nums[i]

    # Final result
    def draw_result(fb):
        states = {}
        for j in range(n):
            if j == pivot_found:
                states[j] = CellState.FOUND
            elif j < pivot_found:
                states[j] = CellState.LEFT_PTR
            else:
                states[j] = CellState.RIGHT_PTR
        pointers = {pivot_found: ("pivot", Colors.GREEN)}
        arr.draw(fb.draw, states=states, pointers=pointers)
        fb.result_banner(f"中心下标 = {pivot_found}")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("724. 寻找数组的中心下标", generate_frames, out)
