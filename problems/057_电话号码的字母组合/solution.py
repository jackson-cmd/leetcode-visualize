import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def letter_combinations(digits):
    """Backtracking to generate letter combinations, visualized."""
    frames = []
    durations = []

    phone = {
        '2': 'abc', '3': 'def', '4': 'ghi', '5': 'jkl',
        '6': 'mno', '7': 'pqrs', '8': 'tuv', '9': 'wxyz'
    }

    if not digits:
        return frames, durations

    # Frame 0: Show the mapping
    fb = FrameBuilder(WIDTH, HEIGHT)
    fb.title("#17 Letter Combinations")
    fb.description(f'digits = "{digits}"')
    font = get_font(18)
    font_sm = get_font(14)
    y_pos = 110
    for i, d in enumerate(digits):
        letters = phone[d]
        fb.draw.text((50, y_pos + i * 35),
                     f'{d} -> "{letters}"', fill=Colors.YELLOW, font=font)
    fb.label(50, y_pos + len(digits) * 35 + 20,
             "Build combinations using backtracking", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    results = []
    # Track backtracking steps
    steps = []

    def backtrack(idx, path):
        if idx == len(digits):
            results.append("".join(path))
            steps.append(("result", list(path), list(results)))
            return
        for letter in phone[digits[idx]]:
            path.append(letter)
            steps.append(("choose", idx, letter, list(path), list(results)))
            backtrack(idx + 1, path)
            path.pop()

    backtrack(0, [])

    # Render each step (limit frames)
    max_frames = 15
    if len(steps) > max_frames:
        step_indices = [int(i * len(steps) / max_frames) for i in range(max_frames)]
    else:
        step_indices = list(range(len(steps)))

    for si in step_indices:
        s = steps[si]
        fb = FrameBuilder(WIDTH, HEIGHT)
        fb.title("#17 Letter Combinations")

        if s[0] == "choose":
            _, idx, letter, path, cur_results = s
            fb.description(f'Depth {idx}: choose "{letter}", path = "{"".join(path)}"')

            # Show digit mapping
            y_pos = 110
            for i, d in enumerate(digits):
                letters = phone[d]
                color = Colors.ACCENT if i == idx else Colors.SUBTEXT
                prefix = "-> " if i == idx else "   "
                fb.draw.text((50, y_pos + i * 35),
                             f'{prefix}{d} -> "{letters}"', fill=color, font=font)
                if i == idx:
                    # Highlight the chosen letter
                    letter_idx = letters.index(letter)
                    x_offset = 50 + len(f'{prefix}{d} -> "') * 10
                    for li, l in enumerate(letters):
                        color_l = Colors.GREEN if li == letter_idx else Colors.SUBTEXT
                        fb.draw.text((180 + li * 20, y_pos + i * 35),
                                     l, fill=color_l, font=font)

            # Show current path
            fb.label(50, 240, f'Current: "{"".join(path)}"', Colors.GREEN)
            if cur_results:
                fb.label(50, 270, f'Found: {cur_results}', Colors.TEAL)

        elif s[0] == "result":
            _, path, cur_results = s
            fb.description(f'Complete combination: "{"".join(path)}"')

            y_pos = 110
            for i, d in enumerate(digits):
                letters = phone[d]
                fb.draw.text((50, y_pos + i * 35),
                             f'   {d} -> "{letters}"', fill=Colors.SUBTEXT, font=font)

            fb.label(50, 240, f'Added "{"".join(path)}" to results', Colors.GREEN)
            fb.label(50, 270, f'Results: {cur_results}', Colors.TEAL)

        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder(WIDTH, HEIGHT)
    fb.title("#17 Letter Combinations")
    fb.description("All combinations generated!")

    # Display results in grid
    cols = 3
    for i, combo in enumerate(results):
        row, col = i // cols, i % cols
        x = 100 + col * 180
        y = 130 + row * 45
        draw_rounded_rect(fb.draw, (x, y, x + 140, y + 36),
                         8, fill="#2d5a2d", outline=Colors.GREEN)
        draw_text_centered(fb.draw, x, y, 140, 36, f'"{combo}"', Colors.TEXT, font)

    fb.result_banner(f"Result: {len(results)} combinations")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = letter_combinations("23")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
