"""
2215. 找出两个数组的不同
哈希集合：找出各自独有的元素
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate_frames():
    nums1 = [1, 2, 3]
    nums2 = [2, 4, 6]

    arr1 = ArrayRenderer(nums1, y=110, cell_w=60, cell_h=52,
                         label="nums1[]", canvas_width=WIDTH)
    arr2 = ArrayRenderer(nums2, y=210, cell_w=60, cell_h=52,
                         label="nums2[]", canvas_width=WIDTH)

    # Frame 1: show both arrays
    def draw_init(fb):
        arr1.draw(fb.draw)
        arr2.draw(fb.draw)
        fb.label(30, 480, "找出两个数组中各自独有的元素", Colors.TEXT)
    yield "初始两个数组", draw_init, DURATION_NORMAL

    # Frame 2: build set1
    set1 = set(nums1)
    def draw_set1(fb):
        arr1.draw(fb.draw, states={i: CellState.CURRENT for i in range(len(nums1))})
        arr2.draw(fb.draw)
        fb.label(30, 340, f"set1 = {set1}", Colors.ACCENT)
        fb.label(30, 480, "将 nums1 转换为集合 set1", Colors.TEXT)
    yield "构建 set1", draw_set1, DURATION_NORMAL

    # Frame 3: build set2
    set2 = set(nums2)
    def draw_set2(fb):
        arr1.draw(fb.draw, states={i: CellState.CURRENT for i in range(len(nums1))})
        arr2.draw(fb.draw, states={i: CellState.CURRENT for i in range(len(nums2))})
        fb.label(30, 340, f"set1 = {set1}", Colors.ACCENT)
        fb.label(30, 370, f"set2 = {set2}", Colors.PEACH)
        fb.label(30, 480, "将 nums2 转换为集合 set2", Colors.TEXT)
    yield "构建 set2", draw_set2, DURATION_NORMAL

    # Frame 4-6: check each element in set1
    diff1 = []
    for val in sorted(set1):
        in_set2 = val in set2
        s1_states = {}
        for i, v in enumerate(nums1):
            if v == val:
                s1_states[i] = CellState.FOUND if not in_set2 else CellState.CHECKING
            else:
                s1_states[i] = CellState.DEFAULT

        s2_states = {}
        for i, v in enumerate(nums2):
            if v == val:
                s2_states[i] = CellState.FOUND
        if not in_set2:
            diff1.append(val)

        cur_val = val
        cur_in = in_set2
        cur_diff1 = list(diff1)
        def draw_check1(fb, s1=s1_states, s2=s2_states, v=cur_val,
                        ins2=cur_in, d1=cur_diff1):
            arr1.draw(fb.draw, states=s1)
            arr2.draw(fb.draw, states=s2)
            found_txt = "在 set2 中" if ins2 else "不在 set2 中"
            fb.label(30, 340, f"检查 {v}: {found_txt}", Colors.ACCENT)
            fb.label(30, 370, f"diff1 = {d1}", Colors.GREEN)
            fb.label(30, 480, f"在 set1 中查找不在 set2 中的元素", Colors.TEXT)
        yield f"检查 set1 中的 {val}", draw_check1, DURATION_NORMAL

    # Frame 7-9: check each element in set2
    diff2 = []
    for val in sorted(set2):
        in_set1 = val in set1
        s2_states = {}
        for i, v in enumerate(nums2):
            if v == val:
                s2_states[i] = CellState.FOUND if not in_set1 else CellState.CHECKING
            else:
                s2_states[i] = CellState.DEFAULT

        s1_states = {}
        for i, v in enumerate(nums1):
            if v == val:
                s1_states[i] = CellState.FOUND
        if not in_set1:
            diff2.append(val)

        cur_val = val
        cur_in = in_set1
        cur_diff2 = list(diff2)
        def draw_check2(fb, s1=s1_states, s2=s2_states, v=cur_val,
                        ins1=cur_in, d1=diff1, d2=cur_diff2):
            arr1.draw(fb.draw, states=s1)
            arr2.draw(fb.draw, states=s2)
            found_txt = "在 set1 中" if ins1 else "不在 set1 中"
            fb.label(30, 340, f"检查 {v}: {found_txt}", Colors.PEACH)
            fb.label(30, 370, f"diff1 = {d1}", Colors.GREEN)
            fb.label(30, 400, f"diff2 = {d2}", Colors.TEAL)
            fb.label(30, 480, f"在 set2 中查找不在 set1 中的元素", Colors.TEXT)
        yield f"检查 set2 中的 {val}", draw_check2, DURATION_NORMAL

    # Final result
    def draw_result(fb):
        # Highlight unique elements
        s1 = {}
        for i, v in enumerate(nums1):
            s1[i] = CellState.FOUND if v in diff1 else CellState.INACTIVE
        s2 = {}
        for i, v in enumerate(nums2):
            s2[i] = CellState.FOUND if v in diff2 else CellState.INACTIVE
        arr1.draw(fb.draw, states=s1)
        arr2.draw(fb.draw, states=s2)
        fb.label(30, 370, f"diff1 = {diff1}", Colors.GREEN)
        fb.label(30, 400, f"diff2 = {diff2}", Colors.TEAL)
        fb.result_banner(f"结果 = [{diff1}, {diff2}]")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("2215. 找出两个数组的不同", generate_frames, out)
