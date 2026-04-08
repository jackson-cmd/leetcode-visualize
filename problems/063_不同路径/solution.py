"""
62. 不同路径 — 可视化
DPTableRenderer 展示 2D 表格逐步填充过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    m, n = 3, 7
    dp = [[0] * n for _ in range(m)]

    # Initialize first row and column
    for i in range(m):
        dp[i][0] = 1
    for j in range(n):
        dp[0][j] = 1

    renderer = DPTableRenderer(rows=m, cols=n, y=130, cell_size=52,
                                canvas_width=WIDTH, label="dp[i][j]")
    col_labels = [str(j) for j in range(n)]
    row_labels = [str(i) for i in range(m)]

    # Frame 1: empty table
    def draw_empty(fb):
        empty = [[0] * n for _ in range(m)]
        renderer.draw(fb.draw, empty, col_labels=col_labels, row_labels=row_labels)
        fb.label(30, 420, "dp[i][j] = 从(0,0)到(i,j)的路径数", Colors.SUBTEXT)
    yield "初始化 3x7 网格", draw_empty, DURATION_NORMAL

    # Frame 2: fill first row and column
    def draw_base(fb):
        states = {}
        for i in range(m):
            states[(i, 0)] = CellState.FOUND
        for j in range(n):
            states[(0, j)] = CellState.FOUND
        renderer.draw(fb.draw, dp, states=states,
                      col_labels=col_labels, row_labels=row_labels)
        fb.label(30, 420, "第一行和第一列都只有1条路径", Colors.SUBTEXT)
    yield "初始化边界: dp[i][0]=1, dp[0][j]=1", draw_base, DURATION_NORMAL

    # Fill DP table row by row
    for i in range(1, m):
        for j in range(1, n):
            dp[i][j] = dp[i - 1][j] + dp[i][j - 1]

            def draw_fill(fb, ci=i, cj=j, snap=[[row[:] for row in dp]]):
                table = snap[0]
                states = {}
                # Already filled
                for r in range(m):
                    for c in range(n):
                        if r == 0 or c == 0:
                            states[(r, c)] = CellState.FOUND
                        elif (r < ci) or (r == ci and c < cj):
                            states[(r, c)] = CellState.FOUND
                states[(ci, cj)] = CellState.CURRENT
                # Dependencies
                states[(ci - 1, cj)] = CellState.CHECKING
                states[(ci, cj - 1)] = CellState.CHECKING
                arrows = [((ci - 1, cj), (ci, cj)), ((ci, cj - 1), (ci, cj))]
                renderer.draw(fb.draw, table, states=states, arrows=arrows,
                              col_labels=col_labels, row_labels=row_labels)
                fb.label(30, 420,
                         f"dp[{ci}][{cj}] = dp[{ci-1}][{cj}] + dp[{ci}][{cj-1}]"
                         f" = {table[ci-1][cj]} + {table[ci][cj-1]} = {table[ci][cj]}",
                         Colors.YELLOW)

            # Capture snapshot
            snap = [row[:] for row in dp]

            def make_draw(ci, cj, snap):
                def draw_fn(fb):
                    states = {}
                    for r in range(m):
                        for c in range(n):
                            if r == 0 or c == 0:
                                states[(r, c)] = CellState.FOUND
                            elif (r < ci) or (r == ci and c < cj):
                                states[(r, c)] = CellState.FOUND
                    states[(ci, cj)] = CellState.CURRENT
                    states[(ci - 1, cj)] = CellState.CHECKING
                    states[(ci, cj - 1)] = CellState.CHECKING
                    arrows = [((ci - 1, cj), (ci, cj)), ((ci, cj - 1), (ci, cj))]
                    renderer.draw(fb.draw, snap, states=states, arrows=arrows,
                                  col_labels=col_labels, row_labels=row_labels)
                    fb.label(30, 420,
                             f"dp[{ci}][{cj}] = dp[{ci-1}][{cj}] + dp[{ci}][{cj-1}]"
                             f" = {snap[ci-1][cj]} + {snap[ci][cj-1]} = {snap[ci][cj]}",
                             Colors.YELLOW)
                return draw_fn

            yield (f"dp[{i}][{j}] = {dp[i-1][j]} + {dp[i][j-1]} = {dp[i][j]}",
                   make_draw(i, j, [row[:] for row in dp]), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        states = {(r, c): CellState.FOUND for r in range(m) for c in range(n)}
        states[(m - 1, n - 1)] = CellState.CURRENT
        renderer.draw(fb.draw, dp, states=states,
                      col_labels=col_labels, row_labels=row_labels)
        fb.result_banner(f"从(0,0)到({m-1},{n-1})共有 {dp[m-1][n-1]} 条不同路径")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("62. 不同路径", generate, output_path)
