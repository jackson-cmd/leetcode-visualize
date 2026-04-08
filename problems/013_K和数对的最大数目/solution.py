"""
1679. K 和数对的最大数目 — 可视化
排序后使用左右双指针寻找和为 k 的数对。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    nums = [3, 1, 3, 4, 3]
    k = 6
    sorted_nums = sorted(nums)  # [1, 3, 3, 3, 4]
    n = len(sorted_nums)

    # Frame 1: unsorted
    def draw_unsorted(fb):
        r = ArrayRenderer(nums, y=180, cell_w=70, canvas_width=WIDTH)
        r.draw(fb.draw)
        fb.label(30, 300, f"原始数组, k={k}", Colors.YELLOW)
    yield f"原始数组, k={k}", draw_unsorted, DURATION_NORMAL

    # Frame 2: sorted
    def draw_sorted(fb):
        r = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
        r.draw(fb.draw)
        fb.label(30, 300, "排序后的数组", Colors.GREEN)
    yield "排序数组", draw_sorted, DURATION_NORMAL

    left, right = 0, n - 1
    count = 0
    arr = list(sorted_nums)
    removed = set()

    # Frame 3: initial pointers
    def draw_init(fb):
        r = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
        pointers = {0: ("L", Colors.SKY), n - 1: ("R", Colors.PEACH)}
        r.draw(fb.draw, pointers=pointers)
        fb.label(30, 300, f"左右指针, 寻找和为 {k} 的数对", Colors.YELLOW)
    yield f"初始双指针, 目标和={k}", draw_init, DURATION_NORMAL

    while left < right:
        s = arr[left] + arr[right]

        # Frame: show current comparison
        def draw_compare(fb, l=left, r=right, sm=s, c=count):
            rend = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
            states = {l: CellState.CURRENT, r: CellState.CURRENT}
            for idx in removed:
                states[idx] = CellState.INACTIVE
            pointers = {l: ("L", Colors.SKY), r: ("R", Colors.PEACH)}
            rend.draw(fb.draw, states=states, pointers=pointers)
            fb.label(30, 300, f"比较: {arr[l]} + {arr[r]} = {sm}, 目标={k}", Colors.YELLOW)
            fb.label(30, 330, f"已找到数对: {c}", Colors.TEXT)
        yield f"比较 {arr[left]}+{arr[right]}={s}", draw_compare, DURATION_NORMAL

        if s == k:
            # Found a pair
            def draw_found(fb, l=left, r=right, c=count, sm=s):
                rend = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
                states = {l: CellState.FOUND, r: CellState.FOUND}
                for idx in removed:
                    states[idx] = CellState.INACTIVE
                pointers = {l: ("L", Colors.SKY), r: ("R", Colors.PEACH)}
                rend.draw(fb.draw, states=states, pointers=pointers)
                fb.label(30, 300, f"{arr[l]}+{arr[r]}={sm}={k} 匹配! 计数={c + 1}", Colors.GREEN)
            yield f"匹配! 计数={count + 1}", draw_found, DURATION_NORMAL

            removed.add(left)
            removed.add(right)
            count += 1
            left += 1
            right -= 1
        elif s < k:
            def draw_less(fb, l=left, r=right, sm=s):
                rend = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
                states = {l: CellState.LEFT_PTR, r: CellState.RIGHT_PTR}
                for idx in removed:
                    states[idx] = CellState.INACTIVE
                pointers = {l: ("L", Colors.SKY), r: ("R", Colors.PEACH)}
                rend.draw(fb.draw, states=states, pointers=pointers)
                fb.label(30, 300, f"{arr[l]}+{arr[r]}={sm} < {k}, 和太小, 左指针右移", Colors.PEACH)
            yield f"和={s} < {k}, L++", draw_less, DURATION_NORMAL
            left += 1
        else:
            def draw_more(fb, l=left, r=right, sm=s):
                rend = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
                states = {l: CellState.LEFT_PTR, r: CellState.RIGHT_PTR}
                for idx in removed:
                    states[idx] = CellState.INACTIVE
                pointers = {l: ("L", Colors.SKY), r: ("R", Colors.PEACH)}
                rend.draw(fb.draw, states=states, pointers=pointers)
                fb.label(30, 300, f"{arr[l]}+{arr[r]}={sm} > {k}, 和太大, 右指针左移", Colors.PEACH)
            yield f"和={s} > {k}, R--", draw_more, DURATION_NORMAL
            right -= 1

    # Final
    def draw_final(fb, c=count):
        rend = ArrayRenderer(sorted_nums, y=180, cell_w=70, canvas_width=WIDTH)
        states = {}
        for idx in removed:
            states[idx] = CellState.FOUND
        for idx in range(n):
            if idx not in removed:
                states[idx] = CellState.INACTIVE
        rend.draw(fb.draw, states=states)
        fb.result_banner(f"最大数对数目 = {c}")
    yield "计算完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1679. K 和数对的最大数目", generate, output_path)
