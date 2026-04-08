"""
283. 移动零 — 可视化
使用 ArrayRenderer 展示快慢双指针移动零到末尾的过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    nums = [0, 1, 0, 3, 12]
    n = len(nums)
    arr = list(nums)

    renderer = ArrayRenderer(arr, y=180, cell_w=70, canvas_width=WIDTH)

    # Frame 1: initial
    def draw_init(fb):
        r = ArrayRenderer(nums, y=180, cell_w=70, canvas_width=WIDTH)
        pointers = {0: ("s/f", Colors.GREEN)}
        r.draw(fb.draw, pointers=pointers)
        fb.label(30, 300, "slow=0, fast=0  初始状态", Colors.YELLOW)
    yield "初始数组, slow=0, fast=0", draw_init, DURATION_NORMAL

    slow = 0
    current = list(nums)

    for fast in range(n):
        if current[fast] != 0:
            # Show checking non-zero
            def draw_found(fb, s=slow, f=fast, a=list(current)):
                r = ArrayRenderer(a, y=180, cell_w=70, canvas_width=WIDTH)
                states = {f: CellState.CURRENT}
                pointers = {}
                if s != f:
                    pointers[s] = ("slow", Colors.GREEN)
                    pointers[f] = ("fast", Colors.ACCENT)
                else:
                    pointers[f] = ("s/f", Colors.GREEN)
                r.draw(fb.draw, states=states, pointers=pointers)
                fb.label(30, 300, f"nums[{f}]={a[f]} != 0, 交换 nums[{s}] 和 nums[{f}]", Colors.YELLOW)
            yield f"fast={fast}, 发现非零值 {current[fast]}", draw_found, DURATION_NORMAL

            # Swap
            current[slow], current[fast] = current[fast], current[slow]

            # Show after swap
            def draw_swap(fb, s=slow, f=fast, a=list(current)):
                r = ArrayRenderer(a, y=180, cell_w=70, canvas_width=WIDTH)
                states = {s: CellState.FOUND}
                if f != s:
                    states[f] = CellState.CHECKING
                pointers = {}
                if s + 1 != f + 1 and s + 1 < n:
                    pointers[s + 1] = ("slow", Colors.GREEN)
                elif s + 1 < n:
                    pointers[s + 1] = ("s/f", Colors.GREEN)
                pointers[f] = ("fast", Colors.ACCENT)
                r.draw(fb.draw, states=states, pointers=pointers)
                fb.label(30, 300, f"交换后: slow 前进到 {s + 1}", Colors.GREEN)
            yield f"交换完成, slow -> {slow + 1}", draw_swap, DURATION_NORMAL

            slow += 1
        else:
            # Show skipping zero
            def draw_skip(fb, s=slow, f=fast, a=list(current)):
                r = ArrayRenderer(a, y=180, cell_w=70, canvas_width=WIDTH)
                states = {f: CellState.REMOVED}
                pointers = {}
                if s != f:
                    pointers[s] = ("slow", Colors.GREEN)
                    pointers[f] = ("fast", Colors.ACCENT)
                else:
                    pointers[f] = ("s/f", Colors.GREEN)
                r.draw(fb.draw, states=states, pointers=pointers)
                fb.label(30, 300, f"nums[{f}]=0, fast 跳过", Colors.YELLOW)
            yield f"fast={fast}, nums[{fast}]=0 跳过", draw_skip, DURATION_NORMAL

    # Final
    def draw_final(fb, a=list(current)):
        r = ArrayRenderer(a, y=180, cell_w=70, canvas_width=WIDTH)
        states = {}
        for i in range(n):
            if a[i] != 0:
                states[i] = CellState.FOUND
            else:
                states[i] = CellState.INACTIVE
        r.draw(fb.draw, states=states)
        fb.result_banner(f"结果: {a}")
    yield "移动零完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("283. 移动零", generate, output_path)
