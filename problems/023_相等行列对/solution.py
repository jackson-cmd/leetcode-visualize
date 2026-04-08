"""
2352. 相等行列对
遍历每对 (row, col)，比较是否相等
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate_frames():
    grid_vals = [
        [3, 2, 1],
        [1, 7, 6],
        [2, 7, 7],
    ]
    n = len(grid_vals)
    grid = GridRenderer(n, n, y=100, cell_size=55)

    # Frame 1: show grid
    def draw_init(fb):
        grid.draw(fb.draw, values=grid_vals)
        # Row/col labels
        font_sm = get_font(14)
        for r in range(n):
            fb.draw.text((grid.x - 35, grid.y + r * grid.cell_size + 18),
                         f"R{r}", fill=Colors.ACCENT, font=font_sm)
        for c in range(n):
            fb.draw.text((grid.x + c * grid.cell_size + 18, grid.y - 18),
                         f"C{c}", fill=Colors.PEACH, font=font_sm)
        fb.label(30, 480, "比较每一行与每一列是否相等", Colors.TEXT)
    yield "初始网格", draw_init, DURATION_NORMAL

    total_pairs = 0
    matched_pairs = []

    for r in range(n):
        for c in range(n):
            # Extract row r and column c
            row = grid_vals[r]
            col = [grid_vals[i][c] for i in range(n)]
            is_match = (row == col)

            if is_match:
                total_pairs += 1
                matched_pairs.append((r, c))

            cur_r = r
            cur_c = c
            cur_match = is_match
            cur_total = total_pairs
            cur_row = list(row)
            cur_col = list(col)
            def draw_check(fb, rr=cur_r, cc=cur_c, m=cur_match, t=cur_total,
                           rv=cur_row, cv=cur_col):
                states = {}
                # Highlight row r (blue)
                for j in range(n):
                    states[(rr, j)] = CellState.LEFT_PTR
                # Highlight column c (peach/orange)
                for i in range(n):
                    if (i, cc) not in states:
                        states[(i, cc)] = CellState.RIGHT_PTR
                    else:
                        # Intersection cell
                        states[(i, cc)] = CellState.SELECTED

                # If match, highlight green
                if m:
                    for j in range(n):
                        states[(rr, j)] = CellState.FOUND
                    for i in range(n):
                        states[(i, cc)] = CellState.FOUND

                grid.draw(fb.draw, values=grid_vals, states=states)

                # Labels
                font_sm = get_font(14)
                for ri in range(n):
                    fb.draw.text((grid.x - 35, grid.y + ri * grid.cell_size + 18),
                                 f"R{ri}", fill=Colors.ACCENT, font=font_sm)
                for ci in range(n):
                    fb.draw.text((grid.x + ci * grid.cell_size + 18, grid.y - 18),
                                 f"C{ci}", fill=Colors.PEACH, font=font_sm)

                fb.label(30, 340, f"Row {rr}: {rv}", Colors.SKY)
                fb.label(30, 365, f"Col {cc}: {cv}", Colors.PEACH)
                match_txt = "匹配!" if m else "不匹配"
                match_color = Colors.GREEN if m else Colors.RED
                fb.label(30, 395, f"结果: {match_txt}", match_color)
                fb.label(30, 480, f"匹配对数 = {t}", Colors.TEXT)
            yield f"比较 Row{r} vs Col{c}", draw_check, DURATION_NORMAL

    # Final result - highlight all matched pairs
    def draw_result(fb):
        states = {}
        for r, c in matched_pairs:
            for j in range(n):
                states[(r, j)] = CellState.FOUND
            for i in range(n):
                states[(i, c)] = CellState.FOUND
        grid.draw(fb.draw, values=grid_vals, states=states)
        font_sm = get_font(14)
        for ri in range(n):
            fb.draw.text((grid.x - 35, grid.y + ri * grid.cell_size + 18),
                         f"R{ri}", fill=Colors.ACCENT, font=font_sm)
        for ci in range(n):
            fb.draw.text((grid.x + ci * grid.cell_size + 18, grid.y - 18),
                         f"C{ci}", fill=Colors.PEACH, font=font_sm)
        if matched_pairs:
            pairs_str = ", ".join(f"(R{r},C{c})" for r, c in matched_pairs)
            fb.label(30, 340, f"匹配的行列对: {pairs_str}", Colors.GREEN)
        fb.result_banner(f"相等行列对数 = {total_pairs}")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("2352. 相等行列对", generate_frames, out)
