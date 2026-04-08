"""
739. 每日温度 — 可视化
ArrayRenderer (temperatures) + StackRenderer (单调递减栈) 展示栈操作过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    temperatures = [73, 74, 75, 71, 69, 72, 76, 73]
    n = len(temperatures)
    answer = [0] * n

    arr = ArrayRenderer(temperatures, y=100, cell_w=65, cell_h=48,
                        label="temperatures", canvas_width=WIDTH)
    ans_arr = ArrayRenderer(answer, y=370, cell_w=65, cell_h=48,
                            label="answer", canvas_width=WIDTH)
    stack_renderer = StackRenderer(x=680, y=110, cell_w=70, cell_h=36,
                                   max_visible=8, canvas_width=WIDTH,
                                   label="Stack(索引)")

    stack = []  # monotonic decreasing stack of indices

    # Frame 1: initial
    def draw_init(fb):
        arr.draw(fb.draw)
        ans_arr.draw(fb.draw, values_override=[0] * n)
        stack_renderer.draw(fb.draw, [])
        fb.label(30, 460, "单调递减栈: 栈中保存索引, 对应温度递减", Colors.SUBTEXT)
    yield "初始化: 单调递减栈", draw_init, DURATION_NORMAL

    for i in range(n):
        # Pop elements while current temp > stack top temp
        popped = []
        while stack and temperatures[i] > temperatures[stack[-1]]:
            idx = stack.pop()
            answer[idx] = i - idx
            popped.append(idx)

        if popped:
            def make_draw_pop(ci, popped_list, stk, ans):
                def draw_fn(fb):
                    arr_states = {}
                    for j in range(ci):
                        if j not in popped_list:
                            arr_states[j] = CellState.FOUND
                    for p in popped_list:
                        arr_states[p] = CellState.CHECKING
                    arr_states[ci] = CellState.CURRENT
                    arr.draw(fb.draw, states=arr_states,
                             pointers={ci: (f"i={ci}", Colors.ACCENT)})

                    ans_vals = list(ans)
                    ans_states = {}
                    for p in popped_list:
                        ans_states[p] = CellState.FOUND
                    ans_arr.draw(fb.draw, values_override=ans_vals, states=ans_states)

                    stk_vals = [f"{s}:{temperatures[s]}" for s in stk]
                    stack_renderer.draw(fb.draw, stk_vals if stk_vals else ["empty"])
                    fb.label(30, 460,
                             f"T[{ci}]={temperatures[ci]} > 栈顶 -> 弹出{popped_list}, 更新answer",
                             Colors.YELLOW)
                return draw_fn

            yield (f"i={i}: T={temperatures[i]}, 弹出{popped}",
                   make_draw_pop(i, popped[:], stack[:], answer[:]), DURATION_NORMAL)

        stack.append(i)

        def make_draw_push(ci, stk, ans):
            def draw_fn(fb):
                arr_states = {}
                for j in range(ci + 1):
                    arr_states[j] = CellState.FOUND
                arr_states[ci] = CellState.CURRENT
                arr.draw(fb.draw, states=arr_states,
                         pointers={ci: (f"i={ci}", Colors.ACCENT)})

                ans_arr.draw(fb.draw, values_override=list(ans))

                stk_vals = [f"{s}:{temperatures[s]}" for s in stk]
                stk_states = {len(stk) - 1: CellState.CURRENT}
                stack_renderer.draw(fb.draw, stk_vals, states=stk_states)
                fb.label(30, 460,
                         f"将索引{ci}(T={temperatures[ci]})压入栈",
                         Colors.GREEN)
            return draw_fn

        yield (f"压入 i={i}(T={temperatures[i]})",
               make_draw_push(i, stack[:], answer[:]), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        arr_states = {i: CellState.FOUND for i in range(n)}
        arr.draw(fb.draw, states=arr_states)
        ans_states = {i: CellState.FOUND for i in range(n)}
        ans_arr.draw(fb.draw, values_override=answer, states=ans_states)
        stack_renderer.draw(fb.draw, ["empty"])
        fb.result_banner(f"answer = {answer}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("739. 每日温度", generate, output_path)
