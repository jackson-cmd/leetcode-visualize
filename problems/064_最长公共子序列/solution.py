"""
1143. 最长公共子序列 — 可视化
DPTableRenderer 2D 展示 LCS 表格填充，行列标签为字符。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    text1 = "abcde"
    text2 = "ace"
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    renderer = DPTableRenderer(rows=m + 1, cols=n + 1, y=120, cell_size=52,
                                canvas_width=WIDTH, label="dp[i][j] = LCS长度")
    col_labels = [""] + list(text2)
    row_labels = [""] + list(text1)

    # Frame 1: initial
    def draw_init(fb):
        renderer.draw(fb.draw, dp, col_labels=col_labels, row_labels=row_labels)
        fb.label(30, 440, f'text1="{text1}", text2="{text2}"', Colors.SUBTEXT)
    yield "初始化DP表格, 全部为0", draw_init, DURATION_NORMAL

    # Fill DP
    fill_steps = []
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
                fill_steps.append((i, j, True, [row[:] for row in dp]))
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
                fill_steps.append((i, j, False, [row[:] for row in dp]))

    # Show selected steps (every step for this small example)
    for i, j, matched, snap in fill_steps:
        def make_draw(ci, cj, is_match, table):
            def draw_fn(fb):
                states = {}
                for r in range(m + 1):
                    for c in range(n + 1):
                        if r == 0 or c == 0:
                            states[(r, c)] = CellState.INACTIVE
                        elif (r < ci) or (r == ci and c < cj):
                            states[(r, c)] = CellState.FOUND
                states[(ci, cj)] = CellState.CURRENT
                if is_match:
                    states[(ci - 1, cj - 1)] = CellState.CHECKING
                    arrows = [((ci - 1, cj - 1), (ci, cj))]
                else:
                    states[(ci - 1, cj)] = CellState.CHECKING
                    states[(ci, cj - 1)] = CellState.CHECKING
                    arrows = [((ci - 1, cj), (ci, cj)), ((ci, cj - 1), (ci, cj))]
                renderer.draw(fb.draw, table, states=states, arrows=arrows,
                              col_labels=col_labels, row_labels=row_labels)
                c1 = text1[ci - 1]
                c2 = text2[cj - 1]
                if is_match:
                    fb.label(30, 440,
                             f"'{c1}'=='{c2}': dp[{ci}][{cj}] = dp[{ci-1}][{cj-1}]+1 = {table[ci][cj]}",
                             Colors.GREEN)
                else:
                    fb.label(30, 440,
                             f"'{c1}'!='{c2}': dp[{ci}][{cj}] = max(dp[{ci-1}][{cj}], dp[{ci}][{cj-1}]) = {table[ci][cj]}",
                             Colors.YELLOW)
            return draw_fn

        c1 = text1[i - 1]
        c2 = text2[j - 1]
        if matched:
            desc = f"'{c1}'=='{c2}' -> dp[{i}][{j}]={snap[i][j]}"
        else:
            desc = f"'{c1}'!='{c2}' -> dp[{i}][{j}]={snap[i][j]}"
        yield desc, make_draw(i, j, matched, snap), DURATION_NORMAL

    # Final frame
    def draw_final(fb):
        states = {}
        for r in range(m + 1):
            for c in range(n + 1):
                states[(r, c)] = CellState.FOUND
        states[(m, n)] = CellState.CURRENT
        renderer.draw(fb.draw, dp, states=states,
                      col_labels=col_labels, row_labels=row_labels)
        fb.result_banner(f"最长公共子序列长度 = {dp[m][n]}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1143. 最长公共子序列", generate, output_path)
