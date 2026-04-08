import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def reverse_words_viz(s):
    """Visualize Reverse Words in a String."""
    frames = []
    durations = []

    # Frame 0: Original string
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#151 Reverse Words in a String")
    fb.description(f'Input: "{s}"')
    sr = StringRenderer(s, y=130, cell_w=36, cell_h=42, canvas_width=WIDTH_WIDE)
    sr.draw(fb.draw, states={}, show_indices=False)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 1: Highlight spaces and words in original string
    states = {}
    words = s.split()
    pos = 0
    word_positions = []
    for word in words:
        idx = s.index(word, pos)
        word_positions.append((idx, idx + len(word)))
        pos = idx + len(word)

    # Highlight each word differently
    color_cycle = [CellState.LEFT_PTR, CellState.RIGHT_PTR, CellState.SELECTED, CellState.WINDOW]
    for wi, (start, end) in enumerate(word_positions):
        for ci in range(start, end):
            states[ci] = color_cycle[wi % len(color_cycle)]

    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#151 Reverse Words in a String")
    fb.description("Step 1: Identify words in the string")
    sr.draw(fb.draw, states=states, show_indices=False)
    fb.label(50, 250, f"Found {len(words)} words: {words}", Colors.ACCENT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame 2: Split into separate word arrays
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#151 Reverse Words in a String")
    fb.description("Step 2: Split into word array")
    y_pos = 120
    for i, word in enumerate(words):
        wr = StringRenderer(word, y=y_pos, cell_w=36, cell_h=42,
                            label=f"words[{i}]", canvas_width=WIDTH_WIDE)
        wr.draw(fb.draw, states={k: color_cycle[i % len(color_cycle)] for k in range(len(word))},
                show_indices=False)
        y_pos += 70
    fb.label(50, y_pos + 10, f"words = {words}", Colors.ACCENT)
    frames.append(fb.build())
    durations.append(DURATION_SLOW)

    # Frames: Show reversing process step by step
    n = len(words)
    for step in range(n // 2 + n % 2):
        left = step
        right = n - 1 - step
        if left > right:
            break

        # Show which pair we're looking at
        fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
        fb.title("#151 Reverse Words in a String")
        if left == right:
            fb.description(f'Step 3: Middle word "{words[left]}" stays in place')
        else:
            fb.description(f'Step 3: Swap words[{left}]="{words[left]}" <-> words[{right}]="{words[right]}"')

        y_pos = 120
        for i, word in enumerate(words):
            wr = StringRenderer(word, y=y_pos, cell_w=36, cell_h=42,
                                label=f"words[{i}]", canvas_width=WIDTH_WIDE)
            if i == left:
                st = {k: CellState.LEFT_PTR for k in range(len(word))}
            elif i == right:
                st = {k: CellState.RIGHT_PTR for k in range(len(word))}
            elif i < left or i > right:
                st = {k: CellState.FOUND for k in range(len(word))}
            else:
                st = {}
            wr.draw(fb.draw, states=st, show_indices=False)
            y_pos += 70
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Perform the swap
        if left != right:
            words[left], words[right] = words[right], words[left]

            fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
            fb.title("#151 Reverse Words in a String")
            fb.description(f"After swap: words = {words}")

            y_pos = 120
            for i, word in enumerate(words):
                wr = StringRenderer(word, y=y_pos, cell_w=36, cell_h=42,
                                    label=f"words[{i}]", canvas_width=WIDTH_WIDE)
                if i <= left or i >= right:
                    st = {k: CellState.FOUND for k in range(len(word))}
                else:
                    st = {}
                wr.draw(fb.draw, states=st, show_indices=False)
                y_pos += 70
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Show fully reversed list
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#151 Reverse Words in a String")
    fb.description("Reverse complete!")
    y_pos = 120
    for i, word in enumerate(words):
        wr = StringRenderer(word, y=y_pos, cell_w=36, cell_h=42,
                            label=f"words[{i}]", canvas_width=WIDTH_WIDE)
        wr.draw(fb.draw, states={k: CellState.FOUND for k in range(len(word))},
                show_indices=False)
        y_pos += 70
    fb.label(50, y_pos + 10, f"words = {words}", Colors.GREEN)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Frame: Join result
    result = " ".join(words)
    result_sr = StringRenderer(result, y=200, cell_w=36, cell_h=42, canvas_width=WIDTH_WIDE)
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#151 Reverse Words in a String")
    fb.description('Step 4: Join words with " "')
    result_sr.draw(fb.draw, states={k: CellState.FOUND for k in range(len(result))},
                   show_indices=False)
    fb.result_banner(f'Result: "{result}"')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = reverse_words_viz("the sky is blue")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output, optimize=True)
