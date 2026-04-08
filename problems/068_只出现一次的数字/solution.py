"""
136. 只出现一次的数字 — 可视化
BitRenderer 展示 XOR 操作逐步消除重复元素的过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def generate():
    nums = [2, 2, 1]
    n = len(nums)

    arr = ArrayRenderer(nums, y=100, cell_w=80, cell_h=52,
                        label="nums", canvas_width=WIDTH)
    result_bits = BitRenderer(num_bits=8, y=220, canvas_width=WIDTH, label="result (XOR累积)")
    current_bits = BitRenderer(num_bits=8, y=330, canvas_width=WIDTH, label="nums[i] 二进制")

    # Frame 1: initial
    def draw_init(fb):
        arr.draw(fb.draw)
        result_bits.draw(fb.draw, 0)
        fb.label(30, 440, "XOR性质: a^a=0, a^0=a, 所以重复元素会被消除", Colors.SUBTEXT)
    yield "初始化: result = 0", draw_init, DURATION_NORMAL

    result = 0
    for i in range(n):
        old_result = result
        result ^= nums[i]

        def make_draw(idx, val, old_r, new_r):
            def draw_fn(fb):
                arr_states = {}
                for j in range(idx):
                    arr_states[j] = CellState.FOUND
                arr_states[idx] = CellState.CURRENT
                arr.draw(fb.draw, states=arr_states,
                         pointers={idx: (f"i={idx}", Colors.ACCENT)})

                # Highlight XOR differences
                old_bits = format(old_r, '08b')
                new_bits = format(new_r, '08b')
                val_bits = format(val, '08b')
                res_states = {}
                val_states = {}
                for b in range(8):
                    pos = 7 - b
                    if old_bits[b] != new_bits[b]:
                        res_states[pos] = CellState.CURRENT
                    if val_bits[b] == '1':
                        val_states[pos] = CellState.CHECKING

                result_bits.draw(fb.draw, new_r, bit_states=res_states)
                current_bits.draw(fb.draw, val, bit_states=val_states)

                fb.label(30, 440,
                         f"result = {old_r} ^ {val} = {new_r}   "
                         f"(二进制: {old_bits} ^ {val_bits} = {format(new_r, '08b')})",
                         Colors.YELLOW)
            return draw_fn

        yield (f"result ^= nums[{i}]={nums[i]} -> {result}",
               make_draw(i, nums[i], old_result, result), DURATION_NORMAL)

    # Final frame
    def draw_final(fb):
        arr_states = {i: CellState.FOUND for i in range(n)}
        arr.draw(fb.draw, states=arr_states)
        result_bits.draw(fb.draw, result)
        fb.result_banner(f"只出现一次的数字 = {result}")
    yield "完成!", draw_final, DURATION_RESULT


if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("136. 只出现一次的数字", generate, output_path)
