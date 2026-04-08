import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../.."))
from viz_lib import *
from collections import deque

def evaluate_division(equations, values, queries):
    """Visualize building a weighted graph and evaluating division queries."""
    frames, durations = [], []

    # Build graph
    graph_adj = {}
    all_vars = set()
    for (a, b), val in zip(equations, values):
        all_vars.add(a)
        all_vars.add(b)
        if a not in graph_adj:
            graph_adj[a] = []
        if b not in graph_adj:
            graph_adj[b] = []
        graph_adj[a].append((b, val))
        graph_adj[b].append((a, 1.0 / val))

    var_list = sorted(all_vars)
    var_to_idx = {v: i for i, v in enumerate(var_list)}
    n = len(var_list)

    edges = []
    for (a, b), val in zip(equations, values):
        edges.append((var_to_idx[a], var_to_idx[b]))

    graph = GraphRenderer(n, edges, radius=120,
                          canvas_width=WIDTH, canvas_height=HEIGHT)

    node_labels = {var_to_idx[v]: v for v in var_list}

    # Frame 0: Show the graph
    fb = FrameBuilder()
    fb.title("#399 Evaluate Division")
    fb.description("Build weighted graph from equations")
    graph.draw(fb.draw, node_labels=node_labels)
    # Show edge weights
    font_sm = get_font(13)
    for (a, b), val in zip(equations, values):
        ia, ib = var_to_idx[a], var_to_idx[b]
        x1, y1 = graph.positions[ia]
        x2, y2 = graph.positions[ib]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        fb.draw.text((mx - 10, my - 15), f"{val}", fill=Colors.YELLOW, font=font_sm)
    fb.label(30, HEIGHT - 45, f"Equations: {len(equations)}", Colors.TEXT)
    frames.append(fb.build())
    durations.append(DURATION_NORMAL)

    # Process each query
    results = []
    for qi, (src, dst) in enumerate(queries):
        if src not in graph_adj or dst not in graph_adj:
            results.append(-1.0)
            fb = FrameBuilder()
            fb.title("#399 Evaluate Division")
            fb.description(f"Query: {src}/{dst} = ? (variable not found)")
            graph.draw(fb.draw, node_labels=node_labels)
            fb.label(30, HEIGHT - 45, f"Result: -1.0", Colors.RED)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            continue

        if src == dst:
            results.append(1.0)
            node_states = {var_to_idx[src]: CellState.CURRENT}
            fb = FrameBuilder()
            fb.title("#399 Evaluate Division")
            fb.description(f"Query: {src}/{dst} = 1.0 (same variable)")
            graph.draw(fb.draw, node_states=node_states, node_labels=node_labels)
            fb.label(30, HEIGHT - 45, f"Result: 1.0", Colors.GREEN)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)
            continue

        # BFS to find path
        visited = {src}
        queue = deque([(src, 1.0, [src])])
        found = False

        while queue:
            curr, product, path = queue.popleft()

            # Show current BFS state
            node_states = {}
            edge_states = {}
            for v in visited:
                node_states[var_to_idx[v]] = CellState.VISITED
            node_states[var_to_idx[src]] = CellState.CURRENT
            if var_to_idx.get(dst) is not None:
                node_states[var_to_idx[dst]] = CellState.CHECKING
            node_states[var_to_idx[curr]] = CellState.SELECTED

            # Highlight path edges
            for i in range(len(path) - 1):
                u_idx = var_to_idx[path[i]]
                v_idx = var_to_idx[path[i + 1]]
                edge_states[(u_idx, v_idx)] = Colors.ACCENT
                edge_states[(v_idx, u_idx)] = Colors.ACCENT

            fb = FrameBuilder()
            fb.title("#399 Evaluate Division")
            fb.description(f"Query {src}/{dst}: at {curr}, product={product:.2f}")
            graph.draw(fb.draw, node_states=node_states, edge_states=edge_states,
                       node_labels=node_labels)
            # Show edge weights
            for (a, b), val in zip(equations, values):
                ia, ib = var_to_idx[a], var_to_idx[b]
                x1, y1 = graph.positions[ia]
                x2, y2 = graph.positions[ib]
                mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                fb.draw.text((mx - 10, my - 15), f"{val}",
                             fill=Colors.YELLOW, font=font_sm)
            fb.label(30, HEIGHT - 45,
                     f"Path: {'->'.join(path)}  Product: {product:.2f}",
                     Colors.TEXT)
            frames.append(fb.build())
            durations.append(DURATION_NORMAL)

            if curr == dst:
                results.append(product)
                found = True

                # Show found result
                node_states = {}
                for v in path:
                    node_states[var_to_idx[v]] = CellState.FOUND
                for i in range(len(path) - 1):
                    u_idx = var_to_idx[path[i]]
                    v_idx = var_to_idx[path[i + 1]]
                    edge_states[(u_idx, v_idx)] = Colors.GREEN
                    edge_states[(v_idx, u_idx)] = Colors.GREEN

                fb = FrameBuilder()
                fb.title("#399 Evaluate Division")
                fb.description(f"Found: {src}/{dst} = {product:.2f}")
                graph.draw(fb.draw, node_states=node_states,
                           edge_states=edge_states, node_labels=node_labels)
                for (a, b), val in zip(equations, values):
                    ia, ib = var_to_idx[a], var_to_idx[b]
                    x1, y1 = graph.positions[ia]
                    x2, y2 = graph.positions[ib]
                    mx, my = (x1 + x2) // 2, (y1 + y2) // 2
                    fb.draw.text((mx - 10, my - 15), f"{val}",
                                 fill=Colors.YELLOW, font=font_sm)
                fb.label(30, HEIGHT - 45,
                         f"Path: {'->'.join(path)}  = {product:.2f}",
                         Colors.GREEN)
                frames.append(fb.build())
                durations.append(DURATION_NORMAL)
                break

            for nb, weight in graph_adj[curr]:
                if nb not in visited:
                    visited.add(nb)
                    queue.append((nb, product * weight, path + [nb]))

        if not found:
            results.append(-1.0)

    # Final frame
    fb = FrameBuilder()
    fb.title("#399 Evaluate Division")
    fb.description("All queries evaluated!")
    graph.draw(fb.draw, node_labels=node_labels)
    for (a, b), val in zip(equations, values):
        ia, ib = var_to_idx[a], var_to_idx[b]
        x1, y1 = graph.positions[ia]
        x2, y2 = graph.positions[ib]
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        fb.draw.text((mx - 10, my - 15), f"{val}",
                     fill=Colors.YELLOW, font=font_sm)
    res_strs = [f"{r:.1f}" for r in results]
    fb.result_banner(f"Results: [{', '.join(res_strs)}]")
    frames.append(fb.build())
    durations.append(DURATION_RESULT)

    return frames, durations


if __name__ == "__main__":
    equations = [["a", "b"], ["b", "c"]]
    values = [2.0, 3.0]
    queries = [["a", "c"], ["b", "a"], ["a", "e"]]
    frames, durations = evaluate_division(equations, values, queries)
    output = os.path.join(os.path.dirname(__file__), "solution.gif")
    generate_gif(frames, durations, output)
