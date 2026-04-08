import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def keys_and_rooms(rooms):
    """Visualize DFS traversal through rooms with keys."""
    n = len(rooms)
    frames, durations = [], []

    # Build edges from rooms (room -> key destinations)
    edges = []
    for i, keys in enumerate(rooms):
        for k in keys:
            edges.append((i, k))

    graph = GraphRenderer(n, edges, radius=140,
                          canvas_width=WIDTH, canvas_height=HEIGHT)

    visited = set()
    stack = [0]
    visit_order = {}
    order = 0

    # Frame 0: Initial state
    fb = FrameBuilder()
    fb.title("#841 Keys and Rooms")
    fb.description(f"rooms = {rooms}, start from room 0")
    node_labels = {i: f"R{i}" for i in range(n)}
    graph.draw(fb.draw, node_labels=node_labels, directed=True)
    fb.label(30, HEIGHT - 45, "Stack: [0]   Visited: {}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    while stack:
        room = stack.pop()
        if room in visited:
            continue
        visited.add(room)
        visit_order[room] = order
        order += 1

        # Show visiting this room
        node_states = {}
        edge_states = {}
        for v in visited:
            node_states[v] = CellState.FOUND
        node_states[room] = CellState.CURRENT

        # Highlight edges from visited nodes
        for u, v in edges:
            if u in visited and v in visited:
                edge_states[(u, v)] = Colors.GREEN

        fb = FrameBuilder()
        fb.title("#841 Keys and Rooms")
        keys_str = str(rooms[room]) if rooms[room] else "[]"
        fb.description(f"Visit room {room}, find keys: {keys_str}")
        graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
                   node_labels=node_labels, directed=True, visit_order=visit_order)
        fb.label(30, HEIGHT - 45,
                 f"Stack: {stack}   Visited: {sorted(visited)}", Colors.TEXT)
        frames.append(fb.build())
        durations.append(DURATION_NORMAL)

        # Add keys to stack
        for key in rooms[room]:
            if key not in visited:
                stack.append(key)

        # Show keys being added
        if rooms[room]:
            new_keys = [k for k in rooms[room] if k not in visited]
            if new_keys:
                # Highlight the edges for newly discovered keys
                for k in rooms[room]:
                    edge_states[(room, k)] = Colors.ACCENT

                fb = FrameBuilder()
                fb.title("#841 Keys and Rooms")
                fb.description(f"Room {room} unlocks access to rooms {new_keys}")
                graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
                           node_labels=node_labels, directed=True, visit_order=visit_order)
                fb.label(30, HEIGHT - 45,
                         f"Stack: {stack}   Visited: {sorted(visited)}", Colors.TEXT)
                frames.append(fb.build())
                durations.append(DURATION_NORMAL)

    # Final frame
    can_visit_all = len(visited) == n
    fb = FrameBuilder()
    fb.title("#841 Keys and Rooms")
    fb.description("DFS complete!")
    node_states = {i: CellState.FOUND for i in visited}
    edge_states = {}
    for u, v in edges:
        if u in visited and v in visited:
            edge_states[(u, v)] = Colors.GREEN
    graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
               node_labels=node_labels, directed=True, visit_order=visit_order)
    fb.result_banner(f"Can visit all rooms: {can_visit_all}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = keys_and_rooms([[1], [2], [3], []])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
