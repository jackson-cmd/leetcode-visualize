import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def merge_alternately(word1, word2):
    """Merge two strings alternately, visualized step by step."""
    result = []
    i, j = 0, 0
    frames = []
    durations = []

    sr1 = StringRenderer(word1, y=120, label="word1")
    sr2 = StringRenderer(word2, y=210, label="word2")
    res_renderer = None

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#1768 Merge Strings Alternately")
    fb.description(f'word1 = "{word1}", word2 = "{word2}"')
    sr1.draw(fb.draw, states={})
    sr2.draw(fb.draw, states={})
    fb.label(50, 310, 'result = ""', Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    while i < len(word1) or j < len(word2):
        # Take from word1
        if i < len(word1):
            result.append(word1[i])
            states1 = {i: CellState.CURRENT}
            # Mark already-taken chars
            for k in range(i):
                states1[k] = CellState.FOUND
            states2 = {}
            for k in range(j):
                states2[k] = CellState.FOUND

            fb = FrameBuilder()
            fb.title("#1768 Merge Strings Alternately")
            fb.description(f'Take word1[{i}] = "{word1[i]}"')
            sr1.draw(fb.draw, states=states1,
                     pointers={i: ("i", Colors.ACCENT)})
            sr2.draw(fb.draw, states=states2)
            fb.label(50, 310, f'result = "{"".join(result)}"', Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            i += 1

        # Take from word2
        if j < len(word2):
            result.append(word2[j])
            states1 = {}
            for k in range(i):
                states1[k] = CellState.FOUND
            states2 = {j: CellState.CURRENT}
            for k in range(j):
                states2[k] = CellState.FOUND

            fb = FrameBuilder()
            fb.title("#1768 Merge Strings Alternately")
            fb.description(f'Take word2[{j}] = "{word2[j]}"')
            sr1.draw(fb.draw, states=states1)
            sr2.draw(fb.draw, states=states2,
                     pointers={j: ("j", Colors.PEACH)})
            fb.label(50, 310, f'result = "{"".join(result)}"', Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            j += 1

    # Final frame
    fb = FrameBuilder()
    fb.title("#1768 Merge Strings Alternately")
    fb.description("Done!")
    states1 = {k: CellState.FOUND for k in range(len(word1))}
    states2 = {k: CellState.FOUND for k in range(len(word2))}
    sr1.draw(fb.draw, states=states1)
    sr2.draw(fb.draw, states=states2)
    merged = "".join(result)
    fb.result_banner(f'Result: "{merged}"')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = merge_alternately("abc", "pqrs")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
