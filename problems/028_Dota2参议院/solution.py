import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

from collections import deque


def dota2_senate(senate):
    """Dota2 Senate using two queues, visualized step by step."""
    frames = []
    durations = []
    n = len(senate)
    radiant = deque()
    dire = deque()

    for i, ch in enumerate(senate):
        if ch == 'R':
            radiant.append(i)
        else:
            dire.append(i)

    qr_r = QueueRenderer(y=160, cell_w=50, cell_h=44, max_visible=8,
                         label="Radiant Queue (R)")
    qr_d = QueueRenderer(y=280, cell_w=50, cell_h=44, max_visible=8,
                         label="Dire Queue (D)")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#649 Dota2 Senate")
    fb.description(f'senate = "{senate}"')
    qr_r.draw(fb.draw, list(radiant))
    qr_d.draw(fb.draw, list(dire))
    fb.label(50, 110, f"Radiant count: {len(radiant)}, Dire count: {len(dire)}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Show initial queue setup
    fb = FrameBuilder()
    fb.title("#649 Dota2 Senate")
    fb.description("Each senator bans one opponent by index order")
    r_states = {k: CellState.LEFT_PTR for k in range(len(radiant))}
    d_states = {k: CellState.RIGHT_PTR for k in range(len(dire))}
    qr_r.draw(fb.draw, list(radiant), states=r_states)
    qr_d.draw(fb.draw, list(dire), states=d_states)
    fb.label(50, 110, "Smaller index acts first, winner re-enters queue", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    round_num = 0
    while radiant and dire:
        r_idx = radiant[0]
        d_idx = dire[0]
        round_num += 1

        # Frame: Show comparison
        fb = FrameBuilder()
        fb.title("#649 Dota2 Senate")
        fb.description(f'Round {round_num}: Compare R({r_idx}) vs D({d_idx})')
        qr_r.draw(fb.draw, list(radiant), states={0: CellState.CURRENT})
        qr_d.draw(fb.draw, list(dire), states={0: CellState.CURRENT})
        winner = "R" if r_idx < d_idx else "D"
        fb.label(50, 110, f"R index={r_idx}, D index={d_idx} -> {winner} acts first", Colors.YELLOW)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        radiant.popleft()
        dire.popleft()

        if r_idx < d_idx:
            # Radiant bans Dire, Radiant re-enters
            radiant.append(r_idx + n)

            fb = FrameBuilder()
            fb.title("#649 Dota2 Senate")
            fb.description(f'R({r_idx}) bans D({d_idx}), R re-enters as {r_idx + n}')
            r_st = {len(radiant) - 1: CellState.FOUND}
            qr_r.draw(fb.draw, list(radiant), states=r_st)
            qr_d.draw(fb.draw, list(dire))
            fb.label(50, 110, f"Radiant: {len(radiant)} left, Dire: {len(dire)} left", Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
        else:
            # Dire bans Radiant, Dire re-enters
            dire.append(d_idx + n)

            fb = FrameBuilder()
            fb.title("#649 Dota2 Senate")
            fb.description(f'D({d_idx}) bans R({r_idx}), D re-enters as {d_idx + n}')
            qr_r.draw(fb.draw, list(radiant))
            d_st = {len(dire) - 1: CellState.FOUND}
            qr_d.draw(fb.draw, list(dire), states=d_st)
            fb.label(50, 110, f"Radiant: {len(radiant)} left, Dire: {len(dire)} left", Colors.RED)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    winner = "Radiant" if radiant else "Dire"

    # Final frame
    fb = FrameBuilder()
    fb.title("#649 Dota2 Senate")
    fb.description(f'{winner} wins! All opponents eliminated.')
    if radiant:
        qr_r.draw(fb.draw, list(radiant),
                  states={k: CellState.FOUND for k in range(len(radiant))})
        qr_d.draw(fb.draw, [])
    else:
        qr_r.draw(fb.draw, [])
        qr_d.draw(fb.draw, list(dire),
                  states={k: CellState.FOUND for k in range(len(dire))})
    fb.result_banner(f'Winner: {winner}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = dota2_senate("RDDRDRD")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
