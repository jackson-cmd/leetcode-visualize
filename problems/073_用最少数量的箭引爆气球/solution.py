"""
452. 用最少数量的箭引爆气球 — 可视化
IntervalRenderer 展示排序后的气球区间，箭放在重叠交点处。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    points = [[10, 16], [2, 8], [1, 6], [7, 12]]

    # Sort by end
    sorted_points = sorted(points, key=lambda x: x[1])
    n = len(sorted_points)

    min_val = min(s for s, e in sorted_points)
    max_val = max(e for s, e in sorted_points)
    renderer = IntervalRenderer(min_val, max_val, y=130, canvas_width=WIDTH)

    # Frame 1: original balloons
    def draw_orig(fb):
        orig_renderer = IntervalRenderer(min_val, max_val, y=130, canvas_width=WIDTH)
        orig_renderer.draw(fb.draw, points, label="气球区间(原始)")
        fb.label(30, 350, f"气球: {points}", Colors.SUBTEXT)
    yield "原始气球区间", draw_orig, DURATION_NORMAL

    # Frame 2: sorted by end
    def draw_sorted(fb):
        renderer.draw(fb.draw, sorted_points, label="按右端点排序")
        fb.label(30, 350, f"排序后: {sorted_points}", Colors.YELLOW)
    yield "按右端点排序", draw_sorted, DURATION_NORMAL

    # Greedy: place arrows
    arrows_pos = []
    arrow_end = sorted_points[0][1]
    arrows_pos.append(arrow_end)
    groups = [[0]]  # which balloons each arrow bursts

    for i in range(1, n):
        if sorted_points[i][0] > arrow_end:
            arrow_end = sorted_points[i][1]
            arrows_pos.append(arrow_end)
            groups.append([i])
        else:
            groups[-1].append(i)

    # Show arrow placement step by step
    current_arrows = []
    burst = set()

    # First arrow
    current_arrows.append(arrows_pos[0])
    for idx in groups[0]:
        burst.add(idx)

    def draw_arrow1(fb):
        states = {}
        for idx in groups[0]:
            states[idx] = CellState.FOUND
        renderer.draw(fb.draw, sorted_points, states=states,
                      arrows=current_arrows[:], label="放置箭")
        fb.label(30, 350,
                 f"箭1: x={arrows_pos[0]}, 引爆气球 {[sorted_points[i] for i in groups[0]]}",
                 Colors.GREEN)
    yield f"箭1在x={arrows_pos[0]}", draw_arrow1, DURATION_NORMAL

    # Process remaining balloons
    for gi in range(1, len(groups)):
        # Show checking non-burst balloon
        first_in_group = groups[gi][0]

        def make_draw_check(idx, prev_arrow):
            def draw_fn(fb):
                states = {}
                for b in burst:
                    states[b] = CellState.FOUND
                states[idx] = CellState.CHECKING
                renderer.draw(fb.draw, sorted_points, states=states,
                              arrows=current_arrows[:], label="检查气球")
                fb.label(30, 350,
                         f"气球{sorted_points[idx]}: start={sorted_points[idx][0]} > 上一箭={prev_arrow} -> 需要新箭",
                         Colors.RED)
            return draw_fn

        yield (f"气球{sorted_points[first_in_group]}需要新箭",
               make_draw_check(first_in_group, current_arrows[-1]), DURATION_NORMAL)

        current_arrows.append(arrows_pos[gi])
        for idx in groups[gi]:
            burst.add(idx)

        def make_draw_new_arrow(arrow_idx, arrow_x, grp):
            def draw_fn(fb):
                states = {}
                for b in burst:
                    states[b] = CellState.FOUND
                renderer.draw(fb.draw, sorted_points, states=states,
                              arrows=current_arrows[:], label="放置新箭")
                fb.label(30, 350,
                         f"箭{arrow_idx+1}: x={arrow_x}, 引爆 {[sorted_points[i] for i in grp]}",
                         Colors.GREEN)
            return draw_fn

        yield (f"箭{gi+1}在x={arrows_pos[gi]}",
               make_draw_new_arrow(gi, arrows_pos[gi], groups[gi]), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        states = {i: CellState.FOUND for i in range(n)}
        renderer.draw(fb.draw, sorted_points, states=states,
                      arrows=arrows_pos, label="所有气球已引爆")
        fb.result_banner(f"最少需要 {len(arrows_pos)} 支箭")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("452. 用最少数量的箭引爆气球", generate, output_path)
