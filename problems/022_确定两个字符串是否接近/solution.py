"""
1657. 确定两个字符串是否接近
比较字符种类和频率排序
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
from collections import Counter

def generate_frames():
    word1 = "abc"
    word2 = "bca"

    str1 = StringRenderer(word1, y=110, label="word1", cell_w=50, cell_h=50)
    str2 = StringRenderer(word2, y=210, label="word2", cell_w=50, cell_h=50)

    # Frame 1: show both strings
    def draw_init(fb):
        str1.draw(fb.draw)
        str2.draw(fb.draw)
        fb.label(30, 480, "判断两个字符串是否接近", Colors.TEXT)
    yield "初始两个字符串", draw_init, DURATION_NORMAL

    # Frame 2: count frequencies of word1
    count1 = Counter(word1)
    def draw_count1(fb):
        str1.draw(fb.draw,
                  states={i: CellState.CURRENT for i in range(len(word1))})
        str2.draw(fb.draw)
        fb.label(30, 310, f"word1 频率: {dict(count1)}", Colors.ACCENT)
        fb.label(30, 480, "统计 word1 的字符频率", Colors.TEXT)
    yield "统计 word1 频率", draw_count1, DURATION_NORMAL

    # Frame 3: count frequencies of word2
    count2 = Counter(word2)
    def draw_count2(fb):
        str1.draw(fb.draw,
                  states={i: CellState.CURRENT for i in range(len(word1))})
        str2.draw(fb.draw,
                  states={i: CellState.CURRENT for i in range(len(word2))})
        fb.label(30, 310, f"word1 频率: {dict(count1)}", Colors.ACCENT)
        fb.label(30, 340, f"word2 频率: {dict(count2)}", Colors.PEACH)
        fb.label(30, 480, "统计 word2 的字符频率", Colors.TEXT)
    yield "统计 word2 频率", draw_count2, DURATION_NORMAL

    # Frame 4: check same character set
    keys1 = set(count1.keys())
    keys2 = set(count2.keys())
    same_keys = keys1 == keys2
    def draw_keys(fb):
        s1 = {}
        s2 = {}
        for i, ch in enumerate(word1):
            s1[i] = CellState.FOUND if ch in keys2 else CellState.REMOVED
        for i, ch in enumerate(word2):
            s2[i] = CellState.FOUND if ch in keys1 else CellState.REMOVED
        str1.draw(fb.draw, states=s1)
        str2.draw(fb.draw, states=s2)
        fb.label(30, 310, f"word1 字符集: {sorted(keys1)}", Colors.ACCENT)
        fb.label(30, 340, f"word2 字符集: {sorted(keys2)}", Colors.PEACH)
        result = "相同" if same_keys else "不同"
        color = Colors.GREEN if same_keys else Colors.RED
        fb.label(30, 370, f"字符种类 {result}", color)
        fb.label(30, 480, "条件1: 两个字符串必须包含相同的字符种类", Colors.TEXT)
    yield "检查字符种类", draw_keys, DURATION_NORMAL

    # Frame 5: sort frequencies
    sorted1 = sorted(count1.values())
    sorted2 = sorted(count2.values())

    # Show frequency arrays
    freq1_arr = ArrayRenderer(sorted1, y=310, cell_w=50, cell_h=45,
                              label="word1 频率排序")
    freq2_arr = ArrayRenderer(sorted2, y=400, cell_w=50, cell_h=45,
                              label="word2 频率排序")

    same_freq = sorted1 == sorted2
    def draw_freq_sort(fb):
        str1.draw(fb.draw,
                  states={i: CellState.INACTIVE for i in range(len(word1))})
        str2.draw(fb.draw,
                  states={i: CellState.INACTIVE for i in range(len(word2))})
        freq_states = {}
        for i in range(len(sorted1)):
            if i < len(sorted2) and sorted1[i] == sorted2[i]:
                freq_states[i] = CellState.FOUND
            else:
                freq_states[i] = CellState.REMOVED
        freq1_arr.draw(fb.draw, states=freq_states, show_indices=False)
        freq2_arr.draw(fb.draw, states=freq_states, show_indices=False)
        result = "相同" if same_freq else "不同"
        color = Colors.GREEN if same_freq else Colors.RED
        fb.label(30, 480, f"条件2: 排序后的频率 {result}", color)
    yield "比较排序后的频率", draw_freq_sort, DURATION_NORMAL

    # Frame 6: compare element by element
    for i in range(max(len(sorted1), len(sorted2))):
        v1 = sorted1[i] if i < len(sorted1) else None
        v2 = sorted2[i] if i < len(sorted2) else None
        match = v1 == v2

        idx = i
        m = match
        def draw_cmp(fb, ii=idx, mm=m):
            str1.draw(fb.draw,
                      states={j: CellState.INACTIVE for j in range(len(word1))})
            str2.draw(fb.draw,
                      states={j: CellState.INACTIVE for j in range(len(word2))})
            fs1 = {}
            fs2 = {}
            for j in range(len(sorted1)):
                if j < ii:
                    fs1[j] = CellState.FOUND
                    fs2[j] = CellState.FOUND
                elif j == ii:
                    fs1[j] = CellState.CURRENT
                    fs2[j] = CellState.CURRENT
            freq1_arr.draw(fb.draw, states=fs1, show_indices=False)
            freq2_arr.draw(fb.draw, states=fs2, show_indices=False)
            status = "匹配" if mm else "不匹配"
            color = Colors.GREEN if mm else Colors.RED
            fb.label(30, 480, f"位置 {ii}: {sorted1[ii]} vs {sorted2[ii]} -> {status}", color)
        yield f"比较频率位置 {i}", draw_cmp, DURATION_NORMAL

    # Final result
    is_close = same_keys and same_freq
    def draw_result(fb):
        s1 = {i: CellState.FOUND for i in range(len(word1))} if is_close else \
             {i: CellState.REMOVED for i in range(len(word1))}
        s2 = {i: CellState.FOUND for i in range(len(word2))} if is_close else \
             {i: CellState.REMOVED for i in range(len(word2))}
        str1.draw(fb.draw, states=s1)
        str2.draw(fb.draw, states=s2)
        fb.label(30, 310, f"字符种类相同: {same_keys}", Colors.TEXT)
        fb.label(30, 340, f"频率排序相同: {same_freq}", Colors.TEXT)
        result_text = "true" if is_close else "false"
        fb.result_banner(f"两个字符串是否接近: {result_text}")
    yield "最终结果", draw_result, DURATION_RESULT

if __name__ == "__main__":
    out = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("1657. 确定两个字符串是否接近",
                        generate_frames, out)
