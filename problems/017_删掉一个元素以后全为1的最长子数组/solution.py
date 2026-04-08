"""
1493. 删掉一个元素以后全为1的最长子数组
滑动窗口：维护窗口内最多一个 0，记录最长长度
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate_frames():
    nums = [0, 1, 1, 1, 0, 1, 1, 0, 1]
    arr = ArrayRenderer(nums, cell_w=55, cell_h=52)
    left = 0
    zero_count = 0
    best = 0
    best_l, best_r = 0, 0

    # Frame 1: initial state
    def draw_init(fb):
        arr.draw(fb.draw, states={i: CellState.DEFAULT for i in range(len(nums))})
        fb.label(30, 480, "left=0, right=0, zero_count=0, best=0", Colors.TEXT)
    yield "初始数组 nums", draw_init, DURATION_NORMAL

    for right in range(len(nums)):
        if nums[right] == 0:
            zero_count += 1

        # shrink window if needed
        while zero_count > 1:
            if nums[left] == 0:
                zero_count -= 1
            left += 1

        window_len = right - left + 1 - 1  # subtract deleted element
        if window_len > best:
            best = window_len
            best_l, best_r = left, right

        # Build states
        states = {}
        for i in range(len(nums)):
            if left <= i <= right:
                if nums[i] == 0:
                    states[i] = CellState.REMOVED
                else:
                    states[i] = CellState.WINDOW
            else:
                states[i] = CellState.DEFAULT

        pointers = {
            left: ("L", Colors.SKY),
            right: ("R", Colors.PEACH),
        }

        cur_best = best
        cur_left, cur_right = left, right
        cur_zero = zero_count
        def draw_step(fb, s=states, p=pointers, l=cur_left, r=cur_right,
                      z=cur_zero, b=cur_best):
            arr.draw(fb.draw, states=s, pointers=p, window=(l, r))
            info = f"left={l}, right={r}, zero_count={z}, window_len={r-l+1-1}, best={b}"
            fb.label(30, 480, info, Colors.TEXT)
        yield f"right={right}, 检查 nums[{right}]={nums[right]}", draw_step, DURATION_NORMAL

    # Final result
    final_states = {}
    for i in range(len(nums)):
        if best_l <= i <= best_r:
            if nums[i] == 0:
                final_states[i] = CellState.REMOVED
            else:
                final_states[i] = CellState.FOUND
        else:
            final_states[i] = CellState.INACTIVE
    def draw_result(fb):
        arr.draw(fb.draw, states=final_states, window=(best_l, best_r))
        fb.result_banner(f"最长子数组长度 = {best}")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1493. 删掉一个元素以后全为1的最长子数组",
                        generate_frames, out)
