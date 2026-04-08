import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def combination_sum_iii(k, n):
    """Backtracking for combination sum III, visualized."""
    frames = []
    durations = []

    candidates = list(range(1, 10))
    cand_ar = ArrayRenderer(candidates, y=110, cell_w=52, cell_h=48, label="candidates 1-9")

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#216 Combination Sum III")
    fb.description(f"k = {k}, n = {n}: find {k} numbers from 1-9 that sum to {n}")
    cand_ar.draw(fb.draw)
    fb.label(50, 220, "Use backtracking: pick numbers in order, track sum", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    results = []
    steps = []

    def backtrack(start, path, cur_sum):
        if len(path) == k:
            if cur_sum == n:
                results.append(list(path))
                steps.append(("found", list(path), cur_sum))
            else:
                steps.append(("reject_sum", list(path), cur_sum))
            return
        if cur_sum >= n:
            steps.append(("prune", list(path), cur_sum, start))
            return
        for i in range(start, 9):
            num = i + 1
            path.append(num)
            steps.append(("choose", list(path), cur_sum + num, i))
            backtrack(i + 1, path, cur_sum + num)
            path.pop()

    backtrack(0, [], 0)

    # Select interesting frames (limit to ~15)
    max_frames = 14
    if len(steps) > max_frames:
        step_indices = list(range(min(max_frames, len(steps))))
    else:
        step_indices = list(range(len(steps)))

    font = get_font(18)

    for si in step_indices:
        s = steps[si]
        fb = FrameBuilder()
        fb.title("#216 Combination Sum III")

        cand_states = {}

        if s[0] == "choose":
            path, cur_sum, idx = s[1], s[2], s[3]
            fb.description(f"Choose {path[-1]}, path={path}, sum={cur_sum}")
            # Highlight chosen numbers
            for num in path:
                cand_states[num - 1] = CellState.CURRENT
            for i in range(idx):
                if (i + 1) not in path:
                    cand_states[i] = CellState.INACTIVE
            cand_ar.draw(fb.draw, states=cand_states)
            fb.label(50, 220, f"Path: {path}, Sum: {cur_sum}/{n}, Need {k - len(path)} more", Colors.YELLOW)

        elif s[0] == "found":
            path, cur_sum = s[1], s[2]
            fb.description(f"Found: {path}, sum = {cur_sum} == {n}")
            for num in path:
                cand_states[num - 1] = CellState.FOUND
            cand_ar.draw(fb.draw, states=cand_states)
            fb.label(50, 220, f"Valid combination: {path}", Colors.GREEN)

        elif s[0] == "reject_sum":
            path, cur_sum = s[1], s[2]
            fb.description(f"Reject: {path}, sum={cur_sum} != {n}")
            for num in path:
                cand_states[num - 1] = CellState.REMOVED
            cand_ar.draw(fb.draw, states=cand_states)
            fb.label(50, 220, f"Sum {cur_sum} != {n}, backtrack", Colors.RED)

        elif s[0] == "prune":
            path, cur_sum, start = s[1], s[2], s[3]
            fb.description(f"Prune: sum={cur_sum} >= {n}")
            for num in path:
                cand_states[num - 1] = CellState.REMOVED
            cand_ar.draw(fb.draw, states=cand_states)
            fb.label(50, 220, f"Sum already >= {n}, prune branch", Colors.RED)

        if results:
            fb.label(50, 260, f"Results found: {results}", Colors.TEAL)

        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#216 Combination Sum III")
    fb.description(f"All combinations found!")
    cand_ar.draw(fb.draw, states={i: CellState.FOUND for i in range(9)})

    if results:
        for ri, r in enumerate(results):
            y_pos = 220 + ri * 40
            draw_rounded_rect(fb.draw, (100, y_pos, 350, y_pos + 32),
                             8, fill="#2d5a2d", outline=Colors.GREEN)
            draw_text_centered(fb.draw, 100, y_pos, 250, 32,
                              str(r), Colors.TEXT, get_font(18))

    fb.result_banner(f"Result: {results}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = combination_sum_iii(3, 7)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
