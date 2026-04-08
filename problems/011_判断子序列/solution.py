"""
392. 判断子序列 — 可视化
使用两个 StringRenderer 展示双指针匹配过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    s = "abc"
    t = "ahbgdc"

    s_renderer = StringRenderer(s, y=140, canvas_width=WIDTH, label="s")
    t_renderer = StringRenderer(t, y=280, canvas_width=WIDTH, label="t")

    # Frame 1: initial
    def draw_init(fb):
        sr = StringRenderer(s, y=140, canvas_width=WIDTH, label="s (子序列)")
        tr = StringRenderer(t, y=280, canvas_width=WIDTH, label="t (主串)")
        sr.draw(fb.draw, pointers={0: ("i", Colors.ACCENT)})
        tr.draw(fb.draw, pointers={0: ("j", Colors.GREEN)})
        fb.label(30, 400, "i=0, j=0  开始匹配", Colors.YELLOW)
    yield "初始状态: s='abc', t='ahbgdc'", draw_init, DURATION_NORMAL

    i, j = 0, 0
    matched = []

    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            # Match found
            mi, mj = i, j
            matched.append((mi, mj))

            def draw_match(fb, ci=mi, cj=mj, m=list(matched)):
                sr = StringRenderer(s, y=140, canvas_width=WIDTH, label="s (子序列)")
                tr = StringRenderer(t, y=280, canvas_width=WIDTH, label="t (主串)")
                s_states = {}
                t_states = {}
                for pi, pj in m:
                    s_states[pi] = CellState.FOUND
                    t_states[pj] = CellState.FOUND
                s_states[ci] = CellState.CURRENT
                t_states[cj] = CellState.CURRENT
                s_pointers = {ci: ("i", Colors.ACCENT)}
                t_pointers = {cj: ("j", Colors.GREEN)}
                sr.draw(fb.draw, states=s_states, pointers=s_pointers)
                tr.draw(fb.draw, states=t_states, pointers=t_pointers)
                fb.label(30, 400, f"s[{ci}]='{s[ci]}' == t[{cj}]='{t[cj]}' 匹配! i++, j++", Colors.GREEN)
            yield f"匹配: s[{i}]='{s[i]}' == t[{j}]='{t[j]}'", draw_match, DURATION_NORMAL
            i += 1
            j += 1
        else:
            # No match
            ci, cj = i, j

            def draw_no_match(fb, ci=ci, cj=cj, m=list(matched)):
                sr = StringRenderer(s, y=140, canvas_width=WIDTH, label="s (子序列)")
                tr = StringRenderer(t, y=280, canvas_width=WIDTH, label="t (主串)")
                s_states = {}
                t_states = {}
                for pi, pj in m:
                    s_states[pi] = CellState.FOUND
                    t_states[pj] = CellState.FOUND
                s_states[ci] = CellState.CURRENT
                t_states[cj] = CellState.CHECKING
                s_pointers = {ci: ("i", Colors.ACCENT)}
                t_pointers = {cj: ("j", Colors.GREEN)}
                sr.draw(fb.draw, states=s_states, pointers=s_pointers)
                tr.draw(fb.draw, states=t_states, pointers=t_pointers)
                fb.label(30, 400, f"s[{ci}]='{s[ci]}' != t[{cj}]='{t[cj]}' 不匹配, j++", Colors.PEACH)
            yield f"不匹配: s[{ci}] != t[{cj}], j++", draw_no_match, DURATION_NORMAL
            j += 1

    # Final result
    is_sub = i == len(s)
    def draw_final(fb, m=list(matched), result=is_sub):
        sr = StringRenderer(s, y=140, canvas_width=WIDTH, label="s (子序列)")
        tr = StringRenderer(t, y=280, canvas_width=WIDTH, label="t (主串)")
        s_states = {pi: CellState.FOUND for pi, _ in m}
        t_states = {pj: CellState.FOUND for _, pj in m}
        sr.draw(fb.draw, states=s_states)
        tr.draw(fb.draw, states=t_states)
        # Draw lines connecting matched chars
        for pi, pj in m:
            sx, sy = sr.cell_bottom(pi)
            tx, ty = tr.cell_top(pj)
            draw_arrow(fb.draw, sx, sy + 5, tx, ty - 5, Colors.GREEN, width=2)
        fb.result_banner(f"结果: {'true' if result else 'false'} — s 是 t 的子序列")
    yield "判断完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("392. 判断子序列", generate, output_path)
