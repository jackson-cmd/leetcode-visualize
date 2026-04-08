"""
1318. 或运算的最小翻转次数 — 可视化
BitRenderer 展示三个数字的二进制，逐位检查需要翻转的位。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    a, b, c = 2, 6, 5
    num_bits = 4

    bits_a = BitRenderer(num_bits=num_bits, y=120, canvas_width=WIDTH, label=f"a = {a}")
    bits_b = BitRenderer(num_bits=num_bits, y=210, canvas_width=WIDTH, label=f"b = {b}")
    bits_c = BitRenderer(num_bits=num_bits, y=300, canvas_width=WIDTH, label=f"c = {c} (目标)")
    bits_or = BitRenderer(num_bits=num_bits, y=390, canvas_width=WIDTH, label="a | b (当前)")

    # Frame 1: show all three numbers
    def draw_init(fb):
        bits_a.draw(fb.draw, a)
        bits_b.draw(fb.draw, b)
        bits_c.draw(fb.draw, c)
        bits_or.draw(fb.draw, a | b)
        fb.label(30, 470, f"需要使 a|b == c, 当前 a|b = {a|b}, c = {c}", Colors.SUBTEXT)
    yield f"a={a}, b={b}, c={c}, 目标: a|b==c", draw_init, DURATION_NORMAL

    # Check bit by bit
    flips = 0
    for pos in range(num_bits - 1, -1, -1):
        bit_a = (a >> pos) & 1
        bit_b = (b >> pos) & 1
        bit_c = (c >> pos) & 1
        cur_or = bit_a | bit_b
        need_flip = 0

        if bit_c == 1:
            if cur_or == 0:
                need_flip = 1  # flip either a or b
        else:  # bit_c == 0
            need_flip = bit_a + bit_b  # flip both if both are 1

        flips += need_flip

        def make_draw(p, ba, bb, bc, nf, total_flips):
            def draw_fn(fb):
                # Highlight current bit position
                a_states = {p: CellState.CURRENT}
                b_states = {p: CellState.CURRENT}
                c_states = {p: CellState.CURRENT}

                if nf > 0:
                    # Need to flip - mark red
                    if bc == 0:
                        if ba == 1:
                            a_states[p] = CellState.REMOVED
                        if bb == 1:
                            b_states[p] = CellState.REMOVED
                    else:  # bc == 1 and cur_or == 0
                        a_states[p] = CellState.CHECKING
                        b_states[p] = CellState.CHECKING
                    c_states[p] = CellState.CHECKING
                else:
                    a_states[p] = CellState.FOUND
                    b_states[p] = CellState.FOUND
                    c_states[p] = CellState.FOUND

                bits_a.draw(fb.draw, a, bit_states=a_states)
                bits_b.draw(fb.draw, b, bit_states=b_states)
                bits_c.draw(fb.draw, c, bit_states=c_states)
                bits_or.draw(fb.draw, a | b)

                if nf == 0:
                    fb.label(30, 470,
                             f"位{p}: a={ba}, b={bb}, c={bc} -> a|b={ba|bb}=={bc} OK",
                             Colors.GREEN)
                else:
                    fb.label(30, 470,
                             f"位{p}: a={ba}, b={bb}, c={bc} -> a|b={ba|bb}!={bc}, 需翻转{nf}次 (累计{total_flips})",
                             Colors.RED)
            return draw_fn

        desc = f"检查位{pos}: a={bit_a}, b={bit_b}, c={bit_c}"
        yield desc, make_draw(pos, bit_a, bit_b, bit_c, need_flip, flips), DURATION_NORMAL

    # Final frame
    def draw_final(fb):
        bits_a.draw(fb.draw, a)
        bits_b.draw(fb.draw, b)
        bits_c.draw(fb.draw, c)
        fb.result_banner(f"最小翻转次数 = {flips}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1318. 或运算的最小翻转次数", generate, output_path)
