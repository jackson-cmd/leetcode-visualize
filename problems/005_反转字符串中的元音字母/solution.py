import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def reverse_vowels_viz(s):
    """Visualize Reverse Vowels of a String with two pointers."""
    frames = []
    durations = []
    vowels = set("aeiouAEIOU")
    chars = list(s)

    sr = StringRenderer(s, y=160, label="string")

    # Frame 0: Initial state - highlight vowels
    fb = FrameBuilder()
    fb.title("#345 Reverse Vowels")
    fb.description(f's = "{s}"')
    states = {}
    for i, c in enumerate(chars):
        if c in vowels:
            states[i] = CellState.SELECTED
    sr.draw(fb.draw, states=states)
    fb.label(50, 270, "Purple = vowels to swap", Colors.MAUVE)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    left, right = 0, len(chars) - 1

    while left < right:
        # Move left pointer to next vowel
        while left < right and chars[left] not in vowels:
            states = {}
            for i, c in enumerate(chars):
                if c in vowels:
                    states[i] = CellState.SELECTED
            states[left] = CellState.LEFT_PTR

            fb = FrameBuilder()
            fb.title("#345 Reverse Vowels")
            fb.description(f'left={left}: "{chars[left]}" is not a vowel, move right')
            sr.draw(fb.draw, states=states, values_override=chars,
                    pointers={left: ("L", Colors.SKY), right: ("R", Colors.PEACH)})
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            left += 1

        # Move right pointer to next vowel
        while left < right and chars[right] not in vowels:
            states = {}
            for i, c in enumerate(chars):
                if c in vowels:
                    states[i] = CellState.SELECTED
            states[right] = CellState.RIGHT_PTR

            fb = FrameBuilder()
            fb.title("#345 Reverse Vowels")
            fb.description(f'right={right}: "{chars[right]}" is not a vowel, move left')
            sr.draw(fb.draw, states=states, values_override=chars,
                    pointers={left: ("L", Colors.SKY), right: ("R", Colors.PEACH)})
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            right -= 1

        if left < right:
            # Show the swap
            states = {}
            for i, c in enumerate(chars):
                if c in vowels and i != left and i != right:
                    states[i] = CellState.SELECTED
            states[left] = CellState.LEFT_PTR
            states[right] = CellState.RIGHT_PTR

            fb = FrameBuilder()
            fb.title("#345 Reverse Vowels")
            fb.description(f'Swap: "{chars[left]}" (L={left}) <-> "{chars[right]}" (R={right})')
            sr.draw(fb.draw, states=states, values_override=chars,
                    pointers={left: ("L", Colors.SKY), right: ("R", Colors.PEACH)})
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            # Perform swap
            chars[left], chars[right] = chars[right], chars[left]

            # Show after swap
            states[left] = CellState.FOUND
            states[right] = CellState.FOUND

            fb = FrameBuilder()
            fb.title("#345 Reverse Vowels")
            fb.description(f'After swap: "{chars[left]}" <-> "{chars[right]}"')
            sr.draw(fb.draw, states=states, values_override=chars,
                    pointers={left: ("L", Colors.SKY), right: ("R", Colors.PEACH)})
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            left += 1
            right -= 1

    # Final frame
    fb = FrameBuilder()
    fb.title("#345 Reverse Vowels")
    fb.description("Pointers crossed - done!")
    states = {i: CellState.FOUND for i in range(len(chars))}
    sr.draw(fb.draw, states=states, values_override=chars)
    result = "".join(chars)
    fb.result_banner(f'Result: "{result}"')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = reverse_vowels_viz("leetcode")
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
