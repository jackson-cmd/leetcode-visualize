"""
714. 买卖股票的最佳时机含手续费 — 可视化
ArrayRenderer 展示价格, 追踪 hold/cash 两种状态的 DP 转移。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    prices = [1, 3, 2, 8, 4, 9]
    fee = 2
    n = len(prices)

    arr = ArrayRenderer(prices, y=120, cell_w=70, cell_h=52,
                        label="prices", canvas_width=WIDTH)
    dp_renderer = DPTableRenderer(rows=2, cols=n, y=310, cell_size=70,
                                   canvas_width=WIDTH, label="DP状态")

    cash = [0] * n
    hold = [0] * n
    cash[0] = 0
    hold[0] = -prices[0]

    # Frame 1: initial
    def draw_init(fb):
        arr.draw(fb.draw)
        states = {}
        dp_vals = [cash[:], hold[:]]
        dp_renderer.draw(fb.draw, dp_vals,
                         row_labels=["cash", "hold"],
                         col_labels=[str(i) for i in range(n)])
        fb.label(30, 470, f"fee={fee}, cash[0]=0, hold[0]=-prices[0]=-{prices[0]}", Colors.SUBTEXT)
    yield "初始化: cash=不持股利润, hold=持股利润", draw_init, DURATION_NORMAL

    # Frame 2: day 0
    def draw_day0(fb):
        arr.draw(fb.draw, states={0: CellState.CURRENT},
                 pointers={0: ("day0", Colors.ACCENT)})
        dp_vals = [[cash[0]] + [None] * (n - 1),
                   [hold[0]] + [None] * (n - 1)]
        dp_states = {(0, 0): CellState.CURRENT, (1, 0): CellState.CURRENT}
        dp_renderer.draw(fb.draw, dp_vals, states=dp_states,
                         row_labels=["cash", "hold"],
                         col_labels=[str(i) for i in range(n)])
        fb.label(30, 470, f"Day 0: cash=0, hold=-{prices[0]}", Colors.YELLOW)
    yield f"Day 0: 价格={prices[0]}", draw_day0, DURATION_NORMAL

    # Fill day by day
    for i in range(1, n):
        cash[i] = max(cash[i - 1], hold[i - 1] + prices[i] - fee)
        hold[i] = max(hold[i - 1], cash[i - 1] - prices[i])

        def make_draw(day, c_list, h_list):
            def draw_fn(fb):
                arr_states = {}
                for d in range(day):
                    arr_states[d] = CellState.FOUND
                arr_states[day] = CellState.CURRENT
                arr.draw(fb.draw, states=arr_states,
                         pointers={day: (f"day{day}", Colors.ACCENT)})

                dp_vals = [c_list[:], h_list[:]]
                # Fill None for unfilled days
                for j in range(day + 1, n):
                    dp_vals[0][j] = None
                    dp_vals[1][j] = None
                dp_states = {(0, day): CellState.CURRENT, (1, day): CellState.CURRENT}
                dp_renderer.draw(fb.draw, dp_vals, states=dp_states,
                                 row_labels=["cash", "hold"],
                                 col_labels=[str(j) for j in range(n)])

                sell_profit = h_list[day - 1] + prices[day] - fee
                buy_profit = c_list[day - 1] - prices[day]
                fb.label(30, 470,
                         f"cash[{day}]=max(cash[{day-1}], hold[{day-1}]+{prices[day]}-{fee})"
                         f"=max({c_list[day-1]},{sell_profit})={c_list[day]}",
                         Colors.YELLOW)
            return draw_fn

        yield (f"Day {i}: 价格={prices[i]}",
               make_draw(i, cash[:], hold[:]), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        arr_states = {i: CellState.FOUND for i in range(n)}
        arr.draw(fb.draw, states=arr_states)
        dp_vals = [cash[:], hold[:]]
        dp_states = {(0, n - 1): CellState.CURRENT}
        dp_renderer.draw(fb.draw, dp_vals, states=dp_states,
                         row_labels=["cash", "hold"],
                         col_labels=[str(i) for i in range(n)])
        fb.result_banner(f"最大利润 = {cash[n-1]}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("714. 买卖股票的最佳时机含手续费", generate, output_path)
