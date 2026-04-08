"""
72. 编辑距离 — 可视化
DPTableRenderer 2D 展示编辑距离表格，显示 insert/delete/replace 三种操作取最小。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    word1 = "horse"
    word2 = "ros"
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Initialize base cases
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    renderer = DPTableRenderer(rows=m + 1, cols=n + 1, y=110, cell_size=56,
                                canvas_width=WIDTH, label="dp[i][j] = 编辑距离")
    col_labels = ["''"] + list(word2)
    row_labels = ["''"] + list(word1)

    # Frame 1: initial base cases
    def draw_init(fb):
        states = {}
        for i in range(m + 1):
            states[(i, 0)] = CellState.FOUND
        for j in range(n + 1):
            states[(0, j)] = CellState.FOUND
        renderer.draw(fb.draw, dp, states=states,
                      col_labels=col_labels, row_labels=row_labels)
        fb.label(30, 460, "边界: dp[i][0]=i(删i次), dp[0][j]=j(插j次)", Colors.SUBTEXT)
    yield "初始化边界条件", draw_init, DURATION_NORMAL

    # Fill DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],      # delete
                                   dp[i][j - 1],      # insert
                                   dp[i - 1][j - 1])  # replace

            def make_draw(ci, cj, is_same, snap):
                def draw_fn(fb):
                    states = {}
                    for r in range(m + 1):
                        for c in range(n + 1):
                            if r == 0 or c == 0:
                                states[(r, c)] = CellState.FOUND
                            elif (r < ci) or (r == ci and c < cj):
                                states[(r, c)] = CellState.FOUND
                    states[(ci, cj)] = CellState.CURRENT
                    arrows = []
                    if is_same:
                        states[(ci - 1, cj - 1)] = CellState.CHECKING
                        arrows = [((ci - 1, cj - 1), (ci, cj))]
                    else:
                        states[(ci - 1, cj)] = CellState.CHECKING      # delete
                        states[(ci, cj - 1)] = CellState.CHECKING      # insert
                        states[(ci - 1, cj - 1)] = CellState.CHECKING  # replace
                        arrows = [((ci - 1, cj), (ci, cj)),
                                  ((ci, cj - 1), (ci, cj)),
                                  ((ci - 1, cj - 1), (ci, cj))]
                    renderer.draw(fb.draw, snap, states=states, arrows=arrows,
                                  col_labels=col_labels, row_labels=row_labels)
                    c1 = word1[ci - 1]
                    c2 = word2[cj - 1]
                    if is_same:
                        fb.label(30, 460,
                                 f"'{c1}'=='{c2}': dp[{ci}][{cj}] = dp[{ci-1}][{cj-1}] = {snap[ci][cj]}",
                                 Colors.GREEN)
                    else:
                        fb.label(30, 460,
                                 f"'{c1}'!='{c2}': 1+min(del={snap[ci-1][cj]}, ins={snap[ci][cj-1]}, rep={snap[ci-1][cj-1]}) = {snap[ci][cj]}",
                                 Colors.YELLOW)
                return draw_fn

            is_same = word1[i - 1] == word2[j - 1]
            snap = [row[:] for row in dp]
            c1 = word1[i - 1]
            c2 = word2[j - 1]
            if is_same:
                desc = f"'{c1}'=='{c2}' -> {dp[i][j]}"
            else:
                desc = f"'{c1}'!='{c2}' -> {dp[i][j]}"
            yield desc, make_draw(i, j, is_same, snap), DURATION_NORMAL

    # Final frame
    def draw_final(fb):
        states = {(r, c): CellState.FOUND for r in range(m + 1) for c in range(n + 1)}
        states[(m, n)] = CellState.CURRENT
        renderer.draw(fb.draw, dp, states=states,
                      col_labels=col_labels, row_labels=row_labels)
        fb.result_banner(f'编辑距离("{word1}", "{word2}") = {dp[m][n]}')
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("72. 编辑距离", generate, output_path)
