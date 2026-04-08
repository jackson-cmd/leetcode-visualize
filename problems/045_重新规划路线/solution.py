import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def reorder_routes(n, connections):
    """Visualize reordering routes so all cities can reach city 0."""
    frames, durations = [], []

    # Build adjacency list with direction info
    adj = [[] for _ in range(n)]
    original_dirs = set()
    for u, v in connections:
        adj[u].append(v)
        adj[v].append(u)
        original_dirs.add((u, v))

    # All edges for GraphRenderer (undirected for layout)
    all_edges = [(u, v) for u, v in connections]
    graph = GraphRenderer(n, all_edges, radius=150,
                          canvas_width=WIDTH_WIDE, canvas_height=HEIGHT_TALL,
                          node_r=24)

    node_labels = {i: str(i) for i in range(n)}

    # Frame 0: Initial state showing original directions
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#1466 Reorder Routes")
    fb.description(f"n={n}, make all cities reach city 0")
    edge_states = {(u, v): Colors.OVERLAY for u, v in connections}
    graph.draw(fb.draw, node_labels=node_labels, directed=True,
               edge_states=edge_states)
    fb.label(30, HEIGHT_TALL - 45, "Reversed: 0", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # BFS from city 0
    visited = {0}
    queue = [0]
    reversed_count = 0
    reversed_edges = set()
    correct_edges = set()

    while queue:
        city = queue.pop(0)
        for neighbor in adj[city]:
            if neighbor in visited:
                continue
            visited.add(neighbor)
            queue.append(neighbor)

            # Check if this edge needs reversing
            # Original direction: city->neighbor means it goes AWAY from 0 (needs reverse)
            # Original direction: neighbor->city means it goes TOWARD 0 (correct)
            needs_reverse = (city, neighbor) in original_dirs

            node_states = {}
            for v in visited:
                node_states[v] = CellState.FOUND
            node_states[city] = CellState.CURRENT
            node_states[neighbor] = CellState.CHECKING

            # Build edge states
            edge_states = {}
            for u, v in connections:
                if (u, v) in reversed_edges:
                    edge_states[(u, v)] = Colors.RED
                elif (u, v) in correct_edges:
                    edge_states[(u, v)] = Colors.GREEN
                else:
                    edge_states[(u, v)] = Colors.OVERLAY

            if needs_reverse:
                reversed_count += 1
                reversed_edges.add((city, neighbor))
                edge_states[(city, neighbor)] = Colors.RED
                desc = f"Edge {city}->{neighbor}: away from 0, REVERSE needed!"
            else:
                correct_edges.add((neighbor, city))
                edge_states[(neighbor, city)] = Colors.GREEN
                desc = f"Edge {neighbor}->{city}: toward 0, OK"

            fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
            fb.title("#1466 Reorder Routes")
            fb.description(desc)
            graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
                       node_labels=node_labels, directed=True)
            fb.label(30, HEIGHT_TALL - 45,
                     f"Reversed: {reversed_count}   Visited: {sorted(visited)}",
                     Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

    # Final frame
    fb = FrameBuilder(WIDTH_WIDE, HEIGHT_TALL)
    fb.title("#1466 Reorder Routes")
    fb.description("BFS complete - all routes checked!")
    node_states = {i: CellState.FOUND for i in range(n)}
    node_states[0] = CellState.CURRENT
    edge_states = {}
    for u, v in connections:
        if (u, v) in reversed_edges:
            edge_states[(u, v)] = Colors.RED
        elif (u, v) in correct_edges:
            edge_states[(u, v)] = Colors.GREEN
        else:
            edge_states[(u, v)] = Colors.GREEN
    graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
               node_labels=node_labels, directed=True)
    fb.result_banner(f"Edges to reverse: {reversed_count}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    frames, durations = reorder_routes(6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]])
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
