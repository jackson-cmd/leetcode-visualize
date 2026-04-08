import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def remove_stars(s):
    """Remove stars from string using a stack, visualized step by step."""
    frames = []
    durations = []
    stack = []

    sr = StringRenderer(s, y=120, label="Input")
    stk = StackRenderer(x=550, y=120, cell_w=60, cell_h=36, max_visible=8, label="Stack")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#2390 Remove Stars From a String")
    fb.description(f's = "{s}"')
    sr.draw(fb.draw, states={})
    stk.draw(fb.draw, [])
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for i, ch in enumerate(s):
        sr_states = {k: CellState.FOUND for k in range(i)}
        sr_states[i] = CellState.CURRENT

        if ch == '*':
            # Pop from stack
            popped = stack.pop() if stack else ''
            stk_states = {len(stack): CellState.REMOVED}

            fb = FrameBuilder()
            fb.title("#2390 Remove Stars From a String")
            fb.description(f's[{i}] = "*" -> Pop "{popped}" from stack')
            sr.draw(fb.draw, states=sr_states,
                    pointers={i: ("i", Colors.ACCENT)})
            # Show stack before pop (with the element being removed highlighted)
            stk.draw(fb.draw, stack + [popped] if popped else stack, states=stk_states)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
        else:
            # Push to stack
            stack.append(ch)
            stk_states = {len(stack) - 1: CellState.CURRENT}

            fb = FrameBuilder()
            fb.title("#2390 Remove Stars From a String")
            fb.description(f's[{i}] = "{ch}" -> Push "{ch}" to stack')
            sr.draw(fb.draw, states=sr_states,
                    pointers={i: ("i", Colors.ACCENT)})
            stk.draw(fb.draw, stack, states=stk_states)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    result = "".join(stack)
    fb = FrameBuilder()
    fb.title("#2390 Remove Stars From a String")
    fb.description("Done! Read stack bottom to top")
    sr_states = {k: CellState.FOUND for k in range(len(s))}
    sr.draw(fb.draw, states=sr_states)
    stk_states = {k: CellState.FOUND for k in range(len(stack))}
    stk.draw(fb.draw, stack, states=stk_states)
    fb.result_banner(f'Result: "{result}"')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = remove_stars("leet**cod*e")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
