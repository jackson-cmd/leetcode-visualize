import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *


def asteroid_collision(asteroids):
    """Asteroid collision using a stack, visualized step by step."""
    frames = []
    durations = []
    stack = []

    ar = ArrayRenderer(asteroids, y=120, cell_w=60, cell_h=52, label="Asteroids")
    stk = StackRenderer(x=580, y=120, cell_w=70, cell_h=36, max_visible=8, label="Stack")

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#735 Asteroid Collision")
    fb.description(f'asteroids = {asteroids}')
    ar.draw(fb.draw, states={})
    stk.draw(fb.draw, [])
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    for i, ast in enumerate(asteroids):
        ar_states = {k: CellState.FOUND for k in range(i)}
        ar_states[i] = CellState.CURRENT

        # Process collisions
        destroyed = False
        collision_happened = True
        while collision_happened:
            collision_happened = False
            if ast < 0 and stack and stack[-1] > 0:
                # Collision!
                top = stack[-1]
                if top < abs(ast):
                    # Top is destroyed
                    stk_states = {len(stack) - 1: CellState.REMOVED}
                    fb = FrameBuilder()
                    fb.title("#735 Asteroid Collision")
                    fb.description(f'Collision! |{top}| < |{ast}| -> {top} destroyed')
                    ar.draw(fb.draw, states=ar_states,
                            pointers={i: ("i", Colors.ACCENT)})
                    stk.draw(fb.draw, stack, states=stk_states)
                    frames.append(fb.build())
                    durations.append(DURATION_NORMAL)
                    stack.pop()
                    collision_happened = True
                elif top == abs(ast):
                    # Both destroyed
                    stk_states = {len(stack) - 1: CellState.REMOVED}
                    fb = FrameBuilder()
                    fb.title("#735 Asteroid Collision")
                    fb.description(f'Collision! |{top}| == |{ast}| -> Both destroyed')
                    ar.draw(fb.draw, states=ar_states,
                            pointers={i: ("i", Colors.ACCENT)})
                    stk.draw(fb.draw, stack, states=stk_states)
                    frames.append(fb.build())
                    durations.append(DURATION_NORMAL)
                    stack.pop()
                    destroyed = True
                    break
                else:
                    # Incoming is destroyed
                    fb = FrameBuilder()
                    fb.title("#735 Asteroid Collision")
                    fb.description(f'Collision! |{top}| > |{ast}| -> {ast} destroyed')
                    ar.draw(fb.draw, states=ar_states,
                            pointers={i: ("i", Colors.ACCENT)})
                    stk.draw(fb.draw, stack, states={len(stack) - 1: CellState.CURRENT})
                    frames.append(fb.build())
                    durations.append(DURATION_NORMAL)
                    destroyed = True
                    break

        if not destroyed:
            stack.append(ast)
            stk_states = {len(stack) - 1: CellState.CURRENT}
            fb = FrameBuilder()
            fb.title("#735 Asteroid Collision")
            fb.description(f'Push {ast} to stack (no collision)')
            ar.draw(fb.draw, states=ar_states,
                    pointers={i: ("i", Colors.ACCENT)})
            stk.draw(fb.draw, stack, states=stk_states)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder()
    fb.title("#735 Asteroid Collision")
    fb.description("All collisions resolved!")
    ar_states = {k: CellState.FOUND for k in range(len(asteroids))}
    ar.draw(fb.draw, states=ar_states)
    stk_states = {k: CellState.FOUND for k in range(len(stack))}
    stk.draw(fb.draw, stack, states=stk_states)
    fb.result_banner(f'Result: {stack}')
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = asteroid_collision([8, 3, -5, 6, -2, -8])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
