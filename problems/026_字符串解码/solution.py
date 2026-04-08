import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def decode_string(s):
    """Decode string using a stack, visualized step by step."""
    frames = []
    durations = []
    stack = []  # stack of (current_string, repeat_count)
    cur_str = ""
    cur_num = 0

    sr = StringRenderer(s, y=120, cell_w=42, cell_h=46, label="Input")
    stk = StackRenderer(x=560, y=120, cell_w=120, cell_h=36, max_visible=6, label="Stack")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#394 Decode String")
    fb.description(f's = "{s}"')
    sr.draw(fb.draw, states={})
    stk.draw(fb.draw, [])
    fb.label(50, 400, f'current = ""', Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for i, ch in enumerate(s):
        sr_states = {k: CellState.FOUND for k in range(i)}
        sr_states[i] = CellState.CURRENT

        if ch.isdigit():
            cur_num = cur_num * 10 + int(ch)
            fb = FrameBuilder()
            fb.title("#394 Decode String")
            fb.description(f's[{i}] = "{ch}" -> number = {cur_num}')
            sr.draw(fb.draw, states=sr_states, pointers={i: ("i", Colors.ACCENT)})
            stk_display = [f'("{s_}", {n})' for s_, n in stack]
            stk.draw(fb.draw, stk_display)
            fb.label(50, 400, f'current = "{cur_str}", num = {cur_num}', Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

        elif ch == '[':
            stack.append((cur_str, cur_num))
            stk_display = [f'("{s_}", {n})' for s_, n in stack]
            stk_states = {len(stack) - 1: CellState.CURRENT}
            cur_str = ""
            cur_num = 0

            fb = FrameBuilder()
            fb.title("#394 Decode String")
            fb.description(f's[{i}] = "[" -> Push state, reset current')
            sr.draw(fb.draw, states=sr_states, pointers={i: ("i", Colors.ACCENT)})
            stk.draw(fb.draw, stk_display, states=stk_states)
            fb.label(50, 400, f'current = "{cur_str}"', Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

        elif ch == ']':
            prev_str, num = stack.pop()
            cur_str = prev_str + cur_str * num
            stk_display = [f'("{s_}", {n})' for s_, n in stack]

            fb = FrameBuilder()
            fb.title("#394 Decode String")
            fb.description(f's[{i}] = "]" -> Pop & repeat {num} times')
            sr.draw(fb.draw, states=sr_states, pointers={i: ("i", Colors.ACCENT)})
            stk.draw(fb.draw, stk_display)
            display_cur = cur_str if len(cur_str) <= 20 else cur_str[:17] + "..."
            fb.label(50, 400, f'current = "{display_cur}"', Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

        else:
            cur_str += ch
            fb = FrameBuilder()
            fb.title("#394 Decode String")
            fb.description(f's[{i}] = "{ch}" -> Append to current')
            sr.draw(fb.draw, states=sr_states, pointers={i: ("i", Colors.ACCENT)})
            stk_display = [f'("{s_}", {n})' for s_, n in stack]
            stk.draw(fb.draw, stk_display)
            display_cur = cur_str if len(cur_str) <= 20 else cur_str[:17] + "..."
            fb.label(50, 400, f'current = "{display_cur}"', Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#394 Decode String")
    fb.description("Decoding complete!")
    sr_states = {k: CellState.FOUND for k in range(len(s))}
    sr.draw(fb.draw, states=sr_states)
    stk.draw(fb.draw, [])
    display_result = cur_str if len(cur_str) <= 20 else cur_str[:17] + "..."
    fb.result_banner(f'Result: "{display_result}"')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = decode_string("3[a2[c]]")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
