"""
901. 在线股票跨度 — 可视化
ArrayRenderer 展示价格 + StackRenderer 展示单调栈逻辑。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    prices = [100, 80, 60, 70, 60, 75, 85]
    expected_spans = [1, 1, 1, 2, 1, 4, 6]
    n = len(prices)

    arr = ArrayRenderer(prices, y=100, cell_w=70, cell_h=48,
                        label="prices", canvas_width=WIDTH)
    span_arr = ArrayRenderer([0] * n, y=370, cell_w=70, cell_h=48,
                              label="spans", canvas_width=WIDTH)
    stack_renderer = StackRenderer(x=660, y=110, cell_w=100, cell_h=36,
                                   max_visible=7, canvas_width=WIDTH,
                                   label="Stack(idx,price)")

    stack = []  # (index, price)
    spans = []

    # Frame 1: initial
    def draw_init(fb):
        arr.draw(fb.draw)
        span_arr.draw(fb.draw, values_override=[0] * n)
        stack_renderer.draw(fb.draw, [])
        fb.label(30, 460, "跨度 = 当前价格之前连续<=它的天数+1", Colors.SUBTEXT)
    yield "初始化: 单调栈求股票跨度", draw_init, DURATION_NORMAL

    for i in range(n):
        # Pop elements while current price >= stack top price
        span = 1
        popped = []
        while stack and prices[i] >= stack[-1][1]:
            idx, price = stack.pop()
            popped.append(idx)

        if stack:
            span = i - stack[-1][0]
        else:
            span = i + 1

        spans.append(span)

        # Show popping phase if any
        if popped:
            def make_draw_pop(ci, popped_list, stk, sp_list):
                def draw_fn(fb):
                    arr_states = {}
                    for j in range(ci):
                        arr_states[j] = CellState.FOUND
                    for p in popped_list:
                        arr_states[p] = CellState.CHECKING
                    arr_states[ci] = CellState.CURRENT
                    arr.draw(fb.draw, states=arr_states,
                             pointers={ci: (f"${prices[ci]}", Colors.ACCENT)})

                    span_vals = sp_list + [0] * (n - len(sp_list))
                    span_arr.draw(fb.draw, values_override=span_vals)

                    stk_vals = [f"{s[0]}:${s[1]}" for s in stk]
                    if not stk_vals:
                        stk_vals = ["empty"]
                    stack_renderer.draw(fb.draw, stk_vals)
                    fb.label(30, 460,
                             f"prices[{ci}]=${prices[ci]} >= 栈顶 -> 弹出索引{popped_list}",
                             Colors.YELLOW)
                return draw_fn

            yield (f"i={i}: ${prices[i]}, 弹出{popped}",
                   make_draw_pop(i, popped[:], stack[:], spans[:-1]), DURATION_NORMAL)

        stack.append((i, prices[i]))

        # Show push and span result
        def make_draw_push(ci, sp, stk, sp_list):
            def draw_fn(fb):
                arr_states = {}
                for j in range(ci + 1):
                    arr_states[j] = CellState.FOUND
                arr_states[ci] = CellState.CURRENT
                # Highlight the span range
                for j in range(ci - sp + 1, ci + 1):
                    arr_states[j] = CellState.WINDOW
                arr_states[ci] = CellState.CURRENT
                arr.draw(fb.draw, states=arr_states,
                         pointers={ci: (f"${prices[ci]}", Colors.ACCENT)})

                span_vals = sp_list + [0] * (n - len(sp_list))
                span_states = {ci: CellState.CURRENT}
                span_arr.draw(fb.draw, values_override=span_vals, states=span_states)

                stk_vals = [f"{s[0]}:${s[1]}" for s in stk]
                stk_states = {len(stk) - 1: CellState.CURRENT}
                stack_renderer.draw(fb.draw, stk_vals, states=stk_states)
                fb.label(30, 460,
                         f"span[{ci}] = {sp} (连续{sp}天价格 <= ${prices[ci]})",
                         Colors.GREEN)
            return draw_fn

        yield (f"span[{i}]={span}",
               make_draw_push(i, span, stack[:], spans[:]), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        arr_states = {i: CellState.FOUND for i in range(n)}
        arr.draw(fb.draw, states=arr_states)
        span_states = {i: CellState.FOUND for i in range(n)}
        span_arr.draw(fb.draw, values_override=spans, states=span_states)
        stack_renderer.draw(fb.draw, ["empty"])
        fb.result_banner(f"spans = {spans}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("901. 在线股票跨度", generate, output_path)
