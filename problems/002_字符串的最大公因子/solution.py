import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
from math import gcd

def gcd_of_strings_viz(str1, str2):
    """Visualize GCD of Strings algorithm."""
    frames = []
    durations = []

    sr1 = StringRenderer(str1, y=120, label="str1")
    sr2 = StringRenderer(str2, y=220, label="str2")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#1071 GCD of Strings")
    fb.description(f'str1 = "{str1}", str2 = "{str2}"')
    sr1.draw(fb.draw, states={})
    sr2.draw(fb.draw, states={})
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Check str1 + str2 == str2 + str1
    concat1 = str1 + str2
    concat2 = str2 + str1
    valid = concat1 == concat2

    fb = FrameBuilder()
    fb.title("#1071 GCD of Strings")
    fb.description(f'Check: str1+str2 == str2+str1 ?')
    sr1.draw(fb.draw, states={})
    sr2.draw(fb.draw, states={})
    color = Colors.GREEN if valid else Colors.RED
    fb.label(50, 320, f'str1+str2 = "{concat1}"', color)
    fb.label(50, 345, f'str2+str1 = "{concat2}"', color)
    fb.label(50, 375, f'Equal: {valid}', color)
    frames.append(fb.build())
    durations.append(DURATION_SLOW)

    if not valid:
        fb = FrameBuilder()
        fb.title("#1071 GCD of Strings")
        fb.description("Strings not compatible")
        sr1.draw(fb.draw, states={})
        sr2.draw(fb.draw, states={})
        fb.result_banner('Result: "" (no GCD)')
        frames.append(fb.build())
        durations.append(DURATION_RESULT)
        return frames, durations

    # Frame 2: Compute GCD of lengths
    g = gcd(len(str1), len(str2))
    fb = FrameBuilder()
    fb.title("#1071 GCD of Strings")
    fb.description(f'gcd(len={len(str1)}, len={len(str2)}) = {g}')
    sr1.draw(fb.draw, states={})
    sr2.draw(fb.draw, states={})
    fb.label(50, 320, f'gcd({len(str1)}, {len(str2)}) = {g}', Colors.ACCENT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frames 3+: Show GCD substring check on str1
    candidate = str1[:g]
    for step in range(len(str1) // g):
        start = step * g
        end = start + g
        states1 = {}
        for i in range(start, end):
            states1[i] = CellState.CURRENT
        for i in range(start):
            states1[i] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#1071 GCD of Strings")
        fb.description(f'Verify: str1[{start}:{end}] == "{candidate}" ?')
        sr1.draw(fb.draw, states=states1)
        sr2.draw(fb.draw, states={})
        fb.label(50, 320, f'GCD candidate = "{candidate}"', Colors.ACCENT)
        chunk = str1[start:end]
        match = chunk == candidate
        fb.label(50, 350, f'str1[{start}:{end}] = "{chunk}" -> {"Match" if match else "No match"}',
                 Colors.GREEN if match else Colors.RED)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Verify on str2
    for step in range(len(str2) // g):
        start = step * g
        end = start + g
        states2 = {}
        for i in range(start, end):
            states2[i] = CellState.CURRENT
        for i in range(start):
            states2[i] = CellState.FOUND

        fb = FrameBuilder()
        fb.title("#1071 GCD of Strings")
        fb.description(f'Verify: str2[{start}:{end}] == "{candidate}" ?')
        sr1.draw(fb.draw, states={k: CellState.FOUND for k in range(len(str1))})
        sr2.draw(fb.draw, states=states2)
        fb.label(50, 320, f'GCD candidate = "{candidate}"', Colors.ACCENT)
        chunk = str2[start:end]
        match = chunk == candidate
        fb.label(50, 350, f'str2[{start}:{end}] = "{chunk}" -> {"Match" if match else "No match"}',
                 Colors.GREEN if match else Colors.RED)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    result = str1[:g]
    fb = FrameBuilder()
    fb.title("#1071 GCD of Strings")
    fb.description("All chunks match!")
    states1 = {k: CellState.FOUND for k in range(len(str1))}
    states2 = {k: CellState.FOUND for k in range(len(str2))}
    sr1.draw(fb.draw, states=states1)
    sr2.draw(fb.draw, states=states2)
    fb.result_banner(f'GCD = "{result}"')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = gcd_of_strings_viz("ABABAB", "ABAB")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
