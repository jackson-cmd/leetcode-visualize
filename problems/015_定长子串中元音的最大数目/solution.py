"""
1456. 定长子串中元音的最大数目 — 可视化
使用 StringRenderer + 滑动窗口展示定长子串中元音计数。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    s = "abciiidef"
    k = 3
    n = len(s)
    vowels = set("aeiou")

    # Frame 1: initial
    def draw_init(fb):
        r = StringRenderer(s, y=160, canvas_width=WIDTH)
        states = {}
        for i, ch in enumerate(s):
            if ch in vowels:
                states[i] = CellState.SELECTED
        r.draw(fb.draw, states=states)
        fb.label(30, 280, f"字符串长度={n}, k={k}, 元音用紫色标记", Colors.YELLOW)
    yield f"初始字符串, k={k}", draw_init, DURATION_NORMAL

    # Initial window
    vowel_count = sum(1 for ch in s[:k] if ch in vowels)
    best_count = vowel_count
    best_start = 0

    # Frame 2: first window
    def draw_first(fb, vc=vowel_count):
        r = StringRenderer(s, y=160, canvas_width=WIDTH)
        states = {}
        for i in range(n):
            if i < k:
                if s[i] in vowels:
                    states[i] = CellState.FOUND
                else:
                    states[i] = CellState.WINDOW
            elif s[i] in vowels:
                states[i] = CellState.SELECTED
        r.draw(fb.draw, states=states, window=(0, k - 1))
        fb.label(30, 280, f"窗口 [0..{k-1}]: 元音数={vc}", Colors.TEAL)
        fb.label(30, 310, f"最大元音数 = {vc}", Colors.GREEN)
    yield f"初始窗口, 元音数={vowel_count}", draw_first, DURATION_NORMAL

    # Slide window
    for i in range(k, n):
        old_ch = s[i - k]
        new_ch = s[i]
        if old_ch in vowels:
            vowel_count -= 1
        if new_ch in vowels:
            vowel_count += 1

        start = i - k + 1
        end = i
        is_best = vowel_count > best_count
        if is_best:
            best_count = vowel_count
            best_start = start

        def draw_slide(fb, st=start, en=end, vc=vowel_count, bc=best_count,
                       oc=old_ch, nc=new_ch, ib=is_best):
            r = StringRenderer(s, y=160, canvas_width=WIDTH)
            states = {}
            for j in range(n):
                if st <= j <= en:
                    if s[j] in vowels:
                        states[j] = CellState.FOUND
                    else:
                        states[j] = CellState.WINDOW
                elif s[j] in vowels:
                    states[j] = CellState.SELECTED
            if st > 0:
                states[st - 1] = CellState.REMOVED
            r.draw(fb.draw, states=states, window=(st, en))
            oc_type = "元音" if oc in vowels else "辅音"
            nc_type = "元音" if nc in vowels else "辅音"
            fb.label(30, 280, f"移除 '{oc}'({oc_type}), 加入 '{nc}'({nc_type}) => 元音数={vc}", Colors.TEAL)
            color = Colors.GREEN if ib else Colors.YELLOW
            fb.label(30, 310, f"最大元音数 = {bc}" + (" (更新!)" if ib else ""), color)
        yield f"窗口 [{start}..{end}], 元音={vowel_count}", draw_slide, DURATION_NORMAL

    # Final
    def draw_final(fb, bs=best_start, bc=best_count):
        r = StringRenderer(s, y=160, canvas_width=WIDTH)
        states = {}
        for j in range(n):
            if bs <= j < bs + k:
                if s[j] in vowels:
                    states[j] = CellState.FOUND
                else:
                    states[j] = CellState.WINDOW
            elif s[j] in vowels:
                states[j] = CellState.SELECTED
        r.draw(fb.draw, states=states, window=(bs, bs + k - 1))
        fb.result_banner(f"最大元音数 = {bc}")
    yield "计算完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1456. 定长子串中元音的最大数目", generate, output_path)
