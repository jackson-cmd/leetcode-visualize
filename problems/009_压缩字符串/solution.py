"""
443. 压缩字符串 — 可视化
使用 StringRenderer 展示读/写指针的压缩过程。
"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def generate():
    chars = list("aabbccc")
    n = len(chars)

    # Frame 1: initial
    def draw_init(fb):
        r = StringRenderer("aabbccc", y=140, canvas_width=WIDTH)
        pointers = {0: ("w/r", Colors.GREEN)}
        r.draw(fb.draw, pointers=pointers)
        fb.label(30, 240, "write=0, read=0  开始压缩", Colors.YELLOW)
    yield "初始数组, write=0, read=0", draw_init, DURATION_NORMAL

    # Simulate step by step
    write = 0
    read = 0
    output = [" "] * n

    while read < n:
        ch = chars[read]
        count = 0
        group_start = read

        # Show start of group scan
        def draw_group_start(fb, r_pos=read, w_pos=write, c=ch):
            r = StringRenderer("aabbccc", y=140, canvas_width=WIDTH)
            states = {r_pos: CellState.CURRENT}
            pointers = {}
            if w_pos == r_pos:
                pointers[r_pos] = ("w/r", Colors.GREEN)
            else:
                pointers[w_pos] = ("w", Colors.GREEN)
                pointers[r_pos] = ("r", Colors.ACCENT)
            r.draw(fb.draw, states=states, pointers=pointers)
            # Show output so far
            if w_pos > 0:
                out_r = StringRenderer("".join(output).ljust(n)[:n], y=330, canvas_width=WIDTH,
                                       label="输出")
                out_states = {i: CellState.FOUND for i in range(w_pos)}
                out_r.draw(fb.draw, states=out_states)
            fb.label(30, 240, f"开始扫描字符 '{c}'", Colors.YELLOW)
        yield f"扫描字符 '{ch}'", draw_group_start, DURATION_NORMAL

        while read < n and chars[read] == ch:
            scan_pos = read
            count += 1

            # Show each char being counted
            def draw_count(fb, sp=scan_pos, gs=group_start, cnt=count, w_pos=write, c=ch):
                r = StringRenderer("aabbccc", y=140, canvas_width=WIDTH)
                states = {}
                for j in range(gs, sp + 1):
                    states[j] = CellState.CURRENT
                pointers = {}
                pointers[w_pos] = ("w", Colors.GREEN)
                pointers[sp] = ("r", Colors.ACCENT)
                r.draw(fb.draw, states=states, pointers=pointers)
                if w_pos > 0:
                    out_r = StringRenderer("".join(output).ljust(n)[:n], y=330, canvas_width=WIDTH,
                                           label="输出")
                    out_states = {i: CellState.FOUND for i in range(w_pos)}
                    out_r.draw(fb.draw, states=out_states)
                fb.label(30, 240, f"'{c}' 计数 = {cnt}", Colors.TEAL)
            yield f"'{ch}' 出现第 {count} 次", draw_count, DURATION_FAST

            read += 1

        # Write char
        output[write] = ch
        w_char = write
        write += 1

        # Write count if > 1
        if count > 1:
            for d in str(count):
                output[write] = d
                write += 1

        # Show write result
        def draw_write_result(fb, gs=group_start, ge=read-1, w_pos=write,
                              c=ch, cnt=count, out=list(output)):
            r = StringRenderer("aabbccc", y=140, canvas_width=WIDTH)
            states = {}
            for j in range(gs, ge + 1):
                states[j] = CellState.CHECKING
            pointers = {}
            if read < n:
                pointers[read] = ("r", Colors.ACCENT)
            pointers[w_pos] = ("w", Colors.GREEN)
            r.draw(fb.draw, states=states, pointers=pointers)
            out_str = "".join(out).ljust(n)[:n]
            out_r = StringRenderer(out_str, y=330, canvas_width=WIDTH, label="输出")
            out_states = {i: CellState.FOUND for i in range(w_pos)}
            out_r.draw(fb.draw, states=out_states)
            desc = f"写入 '{c}'"
            if cnt > 1:
                desc += f" + '{cnt}'"
            fb.label(30, 240, desc + f" => write={w_pos}", Colors.GREEN)
        yield f"写入结果: '{ch}'" + (f"'{count}'" if count > 1 else ""), draw_write_result, DURATION_NORMAL

    # Final frame
    final_len = write
    def draw_final(fb, fl=final_len, out=list(output)):
        out_str = "".join(out[:fl])
        padded = out_str.ljust(n)[:n]
        r = StringRenderer(padded, y=200, canvas_width=WIDTH)
        states = {i: CellState.FOUND for i in range(fl)}
        for i in range(fl, n):
            states[i] = CellState.INACTIVE
        r.draw(fb.draw, states=states)
        fb.result_banner(f"压缩后长度 = {fl}, 结果: {list(out_str)}")
    yield "压缩完成!", draw_final, DURATION_RESULT

if __name__ == "__main__":
    output_path = os.path.join(os.path.dirname(__file__), "solution.gif")
    build_visualization("443. 压缩字符串", generate, output_path)
