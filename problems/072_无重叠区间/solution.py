"""
435. 无重叠区间 — 可视化
IntervalRenderer 展示按结束时间排序后的贪心选择过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    intervals = [[1, 2], [2, 3], [3, 4], [1, 3]]

    # Sort by end time
    sorted_intervals = sorted(intervals, key=lambda x: x[1])
    n = len(sorted_intervals)

    min_val = min(s for s, e in sorted_intervals)
    max_val = max(e for s, e in sorted_intervals)
    renderer = IntervalRenderer(min_val, max_val, y=140, canvas_width=WIDTH)

    # Frame 1: original intervals
    def draw_orig(fb):
        orig_renderer = IntervalRenderer(min_val, max_val, y=140, canvas_width=WIDTH)
        orig_renderer.draw(fb.draw, intervals, label="原始区间")
        fb.label(30, 320, f"区间: {intervals}", Colors.SUBTEXT)
    yield "原始区间", draw_orig, DURATION_NORMAL

    # Frame 2: sorted by end time
    def draw_sorted(fb):
        renderer.draw(fb.draw, sorted_intervals, label="按结束时间排序")
        fb.label(30, 320, f"排序后: {sorted_intervals}", Colors.YELLOW)
    yield "按结束时间排序", draw_sorted, DURATION_NORMAL

    # Greedy selection
    kept = [0]  # Keep first interval
    removed = []
    end = sorted_intervals[0][1]

    # Frame 3: select first
    def draw_first(fb):
        states = {0: CellState.FOUND}
        renderer.draw(fb.draw, sorted_intervals, states=states,
                      label="贪心选择")
        fb.label(30, 320, f"选择第1个区间 {sorted_intervals[0]}, end={end}", Colors.GREEN)
    yield f"选择 {sorted_intervals[0]}", draw_first, DURATION_NORMAL

    for i in range(1, n):
        s, e = sorted_intervals[i]
        if s >= end:
            kept.append(i)
            end = e
            action = "keep"
        else:
            removed.append(i)
            action = "remove"

        def make_draw(idx, act, kept_list, removed_list, cur_end):
            def draw_fn(fb):
                states = {}
                for k in kept_list:
                    states[k] = CellState.FOUND
                for r in removed_list:
                    states[r] = CellState.REMOVED
                states[idx] = CellState.CURRENT if act == "keep" else CellState.REMOVED
                if act == "keep":
                    states[idx] = CellState.FOUND
                renderer.draw(fb.draw, sorted_intervals, states=states,
                              label="贪心选择")
                intv = sorted_intervals[idx]
                if act == "keep":
                    fb.label(30, 320,
                             f"区间{intv}: start={intv[0]} >= end={cur_end} -> 保留, 更新end={intv[1]}",
                             Colors.GREEN)
                else:
                    fb.label(30, 320,
                             f"区间{intv}: start={intv[0]} < end={cur_end} -> 移除(重叠)",
                             Colors.RED)
            return draw_fn

        intv = sorted_intervals[i]
        if action == "keep":
            desc = f"保留 {intv}"
        else:
            desc = f"移除 {intv}"
        yield desc, make_draw(i, action, kept[:], removed[:], end if action == "remove" else sorted_intervals[i - 1][1] if i > 0 else end), DURATION_NORMAL

    # Final frame
    num_removed = len(removed)
    def draw_final(fb):
        states = {}
        for k in kept:
            states[k] = CellState.FOUND
        for r in removed:
            states[r] = CellState.REMOVED
        renderer.draw(fb.draw, sorted_intervals, states=states,
                      label="最终结果")
        fb.result_banner(f"最少移除 {num_removed} 个区间即可无重叠")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("435. 无重叠区间", generate, output_path)
