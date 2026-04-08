import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

from collections import deque


def recent_counter(pings):
    """Number of recent calls using a queue, visualized step by step."""
    frames = []
    durations = []
    queue = deque()
    results = []

    qr = QueueRenderer(y=200, cell_w=62, cell_h=48, max_visible=8, label="Queue (time window)")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#933 Number of Recent Calls")
    fb.description("RecentCounter: count pings in [t-3000, t]")
    qr.draw(fb.draw, [])
    fb.label(50, 350, "Pings: " + str(pings), Colors.TEXT)
    fb.label(50, 380, "Results: []", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for idx, t in enumerate(pings):
        # Add ping
        queue.append(t)
        q_states = {len(queue) - 1: CellState.CURRENT}

        fb = FrameBuilder()
        fb.title("#933 Number of Recent Calls")
        fb.description(f'ping({t}): Add {t} to queue')
        qr.draw(fb.draw, list(queue), states=q_states)
        fb.label(50, 350, f"Window: [{t - 3000}, {t}]", Colors.TEAL)
        fb.label(50, 380, f"Results: {results}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Remove old pings
        removed_any = False
        while queue and queue[0] < t - 3000:
            old = queue.popleft()
            removed_any = True

        if removed_any:
            fb = FrameBuilder()
            fb.title("#933 Number of Recent Calls")
            fb.description(f'Remove pings before {t - 3000}')
            q_states_after = {}
            qr.draw(fb.draw, list(queue), states=q_states_after)
            fb.label(50, 350, f"Window: [{t - 3000}, {t}]", Colors.TEAL)
            fb.label(50, 380, f"Results: {results}", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

        # Count
        count = len(queue)
        results.append(count)
        q_states_all = {k: CellState.FOUND for k in range(len(queue))}

        fb = FrameBuilder()
        fb.title("#933 Number of Recent Calls")
        fb.description(f'ping({t}) returns {count} (queue size)')
        qr.draw(fb.draw, list(queue), states=q_states_all)
        fb.label(50, 350, f"Window: [{t - 3000}, {t}]", Colors.TEAL)
        fb.label(50, 380, f"Results: {results}", Colors.GREEN)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#933 Number of Recent Calls")
    fb.description("All pings processed!")
    qr.draw(fb.draw, list(queue), states={k: CellState.FOUND for k in range(len(queue))})
    fb.result_banner(f'Results: {results}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = recent_counter([1, 100, 3001, 3002])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
