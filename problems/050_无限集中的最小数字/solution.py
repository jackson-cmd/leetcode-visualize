import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def smallest_infinite_set():
    """Visualize SmallestInfiniteSet operations."""
    frames, durations = [], []

    # Simulate operations
    operations = [
        ("init", None),
        ("popSmallest", None),
        ("popSmallest", None),
        ("popSmallest", None),
        ("addBack", 1),
        ("popSmallest", None),
        ("popSmallest", None),
        ("popSmallest", None),
        ("addBack", 2),
        ("addBack", 3),
        ("popSmallest", None),
        ("popSmallest", None),
    ]

    # State: track which numbers are available
    max_display = 10  # Show numbers 1-10
    popped = set()
    added_back = set()
    pop_results = []
    next_natural = 1  # Smallest number never popped

    def get_available():
        """Get sorted list of available numbers in display range."""
        avail = []
        for i in range(1, max_display + 1):
            if i not in popped or i in added_back:
                avail.append(i)
        return avail

    def draw_number_line(fb, highlight=None, highlight_type=None):
        """Draw the number line showing available numbers."""
        arr_vals = list(range(1, max_display + 1))
        arr = ArrayRenderer(arr_vals, y=160, cell_w=55, cell_h=50,
                            label="Number Set (1 to ...)")
        states = {}
        for i, v in enumerate(arr_vals):
            if v in popped and v not in added_back:
                states[i] = CellState.REMOVED
            elif v == highlight and highlight_type == "pop":
                states[i] = CellState.CURRENT
            elif v == highlight and highlight_type == "add":
                states[i] = CellState.FOUND
            else:
                states[i] = CellState.DEFAULT

        pointers = {}
        # Find the smallest available
        avail = get_available()
        if avail:
            smallest_idx = avail[0] - 1  # 0-indexed
            pointers[smallest_idx] = ("min", Colors.ACCENT)

        arr.draw(fb.draw, states=states, pointers=pointers, show_indices=False,
                 values_override=arr_vals)

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#2336 Smallest Infinite Set")
    fb.description("Initialize: numbers {1, 2, 3, 4, ...}")
    draw_number_line(fb)
    fb.label(30, HEIGHT - 65, "Operations: init", Colors.TEXT)
    fb.label(30, HEIGHT - 40, "Results: []", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for op, val in operations[1:]:
        if op == "popSmallest":
            avail = get_available()
            if avail:
                smallest = avail[0]
                pop_results.append(smallest)
                popped.add(smallest)
                added_back.discard(smallest)

                fb = FrameBuilder()
                fb.title("#2336 Smallest Infinite Set")
                fb.description(f"popSmallest() -> {smallest}")
                draw_number_line(fb, highlight=smallest, highlight_type="pop")
                fb.label(30, HEIGHT - 65, f"Operation: popSmallest()",
                         Colors.ACCENT)
                fb.label(30, HEIGHT - 40,
                         f"Results: {pop_results}", Colors.TEXT)
                frames.append(fb.build())
                durations.append(DURATION_NORMAL)

        elif op == "addBack":
            added_back.add(val)
            fb = FrameBuilder()
            fb.title("#2336 Smallest Infinite Set")
            fb.description(f"addBack({val}): restore {val} to set")
            draw_number_line(fb, highlight=val, highlight_type="add")
            fb.label(30, HEIGHT - 65, f"Operation: addBack({val})",
                     Colors.GREEN)
            fb.label(30, HEIGHT - 40,
                     f"Results: {pop_results}", Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#2336 Smallest Infinite Set")
    fb.description("All operations complete!")
    draw_number_line(fb)
    fb.result_banner(f"Pop results: {pop_results}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = smallest_infinite_set()
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
