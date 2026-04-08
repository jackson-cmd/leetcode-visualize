import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *

def number_of_provinces(isConnected):
    """Visualize finding connected components (provinces) in a graph."""
    n = len(isConnected)
    frames, durations = [], []

    # Build edges from adjacency matrix
    edges = []
    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                edges.append((i, j))

    graph = GraphRenderer(n, edges, radius=140,
                          canvas_width=WIDTH, canvas_height=HEIGHT)

    # Color palette for provinces
    province_colors = [
        (CellState.FOUND, Colors.GREEN),
        (("#4a2d5a", Colors.MAUVE), Colors.MAUVE),
        (("#2d4a5a", Colors.SKY), Colors.SKY),
        (("#5a4a2d", Colors.PEACH), Colors.PEACH),
    ]

    node_labels = {i: f"C{i}" for i in range(n)}

    # Frame 0: Initial
    fb = FrameBuilder()
    fb.title("#547 Number of Provinces")
    fb.description(f"Adjacency matrix: {n} cities, find provinces")
    graph.draw(fb.draw, node_labels=node_labels)
    fb.label(30, HEIGHT - 45, "Provinces found: 0", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    visited = set()
    provinces = 0
    component_map = {}  # node -> province id

    for i in range(n):
        if i in visited:
            continue
        provinces += 1
        prov_state, prov_edge_color = province_colors[(provinces - 1) % len(province_colors)]

        # BFS/DFS to find all in this component
        queue = [i]
        component = []
        while queue:
            node = queue.pop(0)
            if node in visited:
                continue
            visited.add(node)
            component.append(node)
            component_map[node] = provinces - 1

            # Show visiting this node
            node_states = {}
            edge_states = {}
            for v, pid in component_map.items():
                ps, _ = province_colors[pid % len(province_colors)]
                node_states[v] = ps
            node_states[node] = CellState.CURRENT

            for u, v in edges:
                if u in component_map and v in component_map:
                    _, ec = province_colors[component_map[u] % len(province_colors)]
                    edge_states[(u, v)] = ec

            fb = FrameBuilder()
            fb.title("#547 Number of Provinces")
            fb.description(f"Province {provinces}: visiting city {node}")
            graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
                       node_labels=node_labels)
            fb.label(30, HEIGHT - 45,
                     f"Provinces found: {provinces}   Visited: {sorted(visited)}",
                     Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            for j in range(n):
                if isConnected[node][j] == 1 and j not in visited:
                    queue.append(j)

    # Final frame
    fb = FrameBuilder()
    fb.title("#547 Number of Provinces")
    fb.description("All cities explored!")
    node_states = {}
    edge_states = {}
    for v, pid in component_map.items():
        ps, _ = province_colors[pid % len(province_colors)]
        node_states[v] = ps
    for u, v in edges:
        if u in component_map and v in component_map and component_map[u] == component_map[v]:
            _, ec = province_colors[component_map[u] % len(province_colors)]
            edge_states[(u, v)] = ec
    graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
               node_labels=node_labels)
    fb.result_banner(f"Total provinces: {provinces}")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    matrix = [[1, 1, 0], [1, 1, 0], [0, 0, 1]]
    frames, durations = number_of_provinces(matrix)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
