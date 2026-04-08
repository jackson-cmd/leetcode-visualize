"""
1004. 最大连续1的个数 III — 可视化
使用 ArrayRenderer + 可变滑动窗口展示最多翻转 k 个 0 后的最长连续 1。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    nums = [1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0]
    k = 2
    n = len(nums)

    # Frame 1: initial
    def draw_init(fb):
        r = ArrayRenderer(nums, y=160, cell_w=52, canvas_width=WIDTH)
        states = {}
        for i in range(n):
            if nums[i] == 0:
                states[i] = CellState.REMOVED
        r.draw(fb.draw, states=states)
        fb.label(30, 280, f"数组长度={n}, 最多翻转 k={k} 个 0", Colors.YELLOW)
    yield f"初始数组, k={k}", draw_init, DURATION_NORMAL

    left = 0
    zeros = 0
    best_len = 0
    best_l = 0
    best_r = 0

    for right in range(n):
        if nums[right] == 0:
            zeros += 1

        # Shrink window if too many zeros
        while zeros > k:
            if nums[left] == 0:
                zeros -= 1
            left += 1

        current_len = right - left + 1
        if current_len > best_len:
            best_len = current_len
            best_l = left
            best_r = right

        # Show this step
        def draw_step(fb, l=left, r=right, z=zeros, cl=current_len,
                      bl=best_len, b_l=best_l, b_r=best_r):
            rend = ArrayRenderer(nums, y=160, cell_w=52, canvas_width=WIDTH)
            states = {}
            for j in range(n):
                if l <= j <= r:
                    if nums[j] == 1:
                        states[j] = CellState.FOUND
                    else:
                        states[j] = CellState.CHECKING  # flipped 0
                elif nums[j] == 0:
                    states[j] = CellState.REMOVED
            pointers = {l: ("L", Colors.SKY), r: ("R", Colors.PEACH)}
            rend.draw(fb.draw, states=states, pointers=pointers, window=(l, r))
            fb.label(30, 280, f"窗口 [{l}..{r}], 长度={cl}, 翻转0数={z}", Colors.TEAL)
            fb.label(30, 310, f"最大长度 = {bl} (窗口 [{b_l}..{b_r}])", Colors.GREEN)
        yield f"R={right}, 窗口[{left}..{right}], 长度={current_len}", draw_step, DURATION_NORMAL

    # Final
    def draw_final(fb, bl=best_len, b_l=best_l, b_r=best_r):
        rend = ArrayRenderer(nums, y=160, cell_w=52, canvas_width=WIDTH)
        states = {}
        for j in range(n):
            if b_l <= j <= b_r:
                states[j] = CellState.FOUND
            elif nums[j] == 0:
                states[j] = CellState.REMOVED
            else:
                states[j] = CellState.INACTIVE
        rend.draw(fb.draw, states=states, window=(b_l, b_r))
        fb.result_banner(f"最大连续1的个数 = {bl}")
    yield "计算完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1004. 最大连续1的个数 III", generate, output_path)
