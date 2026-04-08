"""
1207. 独一无二的出现次数
哈希表计数 + 集合判重
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate_frames():
    arr_vals = [1, 2, 2, 1, 1, 3]
    arr = ArrayRenderer(arr_vals, y=110, cell_w=55, cell_h=52, label="arr[]")
    hmap = HashMapRenderer(y=310, cols=3, entry_w=160, entry_h=36)

    # Frame 1: initial
    def draw_init(fb):
        arr.draw(fb.draw)
        hmap.draw(fb.draw, {}, label="count { }")
        fb.label(30, 480, "统计每个元素的出现次数", Colors.TEXT)
    yield "初始数组", draw_init, DURATION_NORMAL

    # Count occurrences step by step
    count = {}
    for i, val in enumerate(arr_vals):
        count[val] = count.get(val, 0) + 1

        states = {i: CellState.CURRENT}
        # Highlight same values already seen
        for j in range(i):
            if arr_vals[j] == val:
                states[j] = CellState.WINDOW

        pointers = {i: ("i", Colors.ACCENT)}
        cur_count = dict(count)
        cur_val = val
        def draw_count(fb, s=states, p=pointers, cc=cur_count, cv=cur_val):
            arr.draw(fb.draw, states=s, pointers=p)
            hmap.draw(fb.draw, cc, highlight_key=cv,
                      label="count { value -> times }")
            fb.label(30, 480, f"count[{cv}] = {cc[cv]}", Colors.TEXT)
        yield f"处理 arr[{i}]={val}", draw_count, DURATION_NORMAL

    # Frame: show all counts done
    final_count = dict(count)
    def draw_counts_done(fb):
        arr.draw(fb.draw,
                 states={i: CellState.INACTIVE for i in range(len(arr_vals))})
        hmap.draw(fb.draw, final_count, label="count { value -> times }")
        fb.label(30, 480, "计数完成，检查出现次数是否唯一", Colors.TEXT)
    yield "计数完成", draw_counts_done, DURATION_NORMAL

    # Check uniqueness
    freq_values = list(count.values())
    is_unique = len(freq_values) == len(set(freq_values))

    # Show the frequency check
    freq_set = set()
    for key in sorted(count.keys()):
        freq = count[key]
        duplicate = freq in freq_set
        freq_set.add(freq)

        cur_key = key
        cur_freq = freq
        cur_dup = duplicate
        cur_fset = set(freq_set)
        def draw_check(fb, ck=cur_key, cf=cur_freq, cd=cur_dup,
                       cfs=cur_fset):
            arr.draw(fb.draw,
                     states={i: CellState.INACTIVE for i in range(len(arr_vals))})
            hmap.draw(fb.draw, final_count, highlight_key=ck,
                      label="count { value -> times }")
            status = "重复!" if cd else "唯一"
            color = Colors.RED if cd else Colors.GREEN
            fb.label(30, 430, f"频率集合: {sorted(cfs)}", Colors.TEAL)
            fb.label(30, 460, f"count[{ck}]={cf} -> {status}", color)
            fb.label(30, 480, "检查每个出现次数是否唯一", Colors.TEXT)
        yield f"检查 count[{key}]={freq}", draw_check, DURATION_NORMAL

    # Final result
    def draw_result(fb):
        arr.draw(fb.draw,
                 states={i: CellState.INACTIVE for i in range(len(arr_vals))})
        hmap.draw(fb.draw, final_count, label="count { value -> times }")
        fb.label(30, 430, f"频率值: {sorted(freq_values)}", Colors.TEAL)
        result_text = "true" if is_unique else "false"
        fb.result_banner(f"出现次数是否唯一: {result_text}")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1207. 独一无二的出现次数", generate_frames, out)
