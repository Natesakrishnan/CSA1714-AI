"""
Assignment 1 – CSA17 Artificial Intelligence
Hospital Medicine-Delivery Robot – Search Strategy Implementation
Author : Krishna
Seed   : 42 (all experiments)
"""

import random
import time
import heapq
import sys
from collections import deque

# =============================================================
# GRAPH GENERATION
# =============================================================

def generate_hospital_graph(num_states: int, seed: int = 42,
                              avg_degree: int = 4) -> dict:
    """
    Generate a weighted undirected graph modelling a hospital floor plan.
    Nodes  : 0 … num_states-1
    Edges  : each node connected to avg_degree neighbours on average
    Weight : travel time 1-10 (integer)
    Returns adjacency list: {node: [(neighbour, cost), ...]}
    """
    rng = random.Random(seed)
    adj = {i: [] for i in range(num_states)}

    # Ensure connectivity with a spanning chain
    nodes = list(range(num_states))
    rng.shuffle(nodes)
    for i in range(1, num_states):
        cost = rng.randint(1, 10)
        u, v = nodes[i - 1], nodes[i]
        adj[u].append((v, cost))
        adj[v].append((u, cost))

    # Add extra random edges for avg_degree ≈ avg_degree
    extra_edges = (avg_degree * num_states) // 2 - (num_states - 1)
    extra_edges = max(0, extra_edges)
    for _ in range(extra_edges):
        u = rng.randint(0, num_states - 1)
        v = rng.randint(0, num_states - 1)
        if u != v:
            cost = rng.randint(1, 10)
            adj[u].append((v, cost))
            adj[v].append((u, cost))

    return adj


# =============================================================
# ALGORITHM 1 – BREADTH-FIRST SEARCH (BFS)  [Iterative, FIFO queue]
# =============================================================

def bfs(adj: dict, start: int, goal: int) -> dict:
    """
    BFS finds the shallowest path (minimum number of hops).
    Returns a result dict with path, nodes generated, nodes expanded,
    max frontier size, path cost, and solution depth.
    """
    if start == goal:
        return _make_result([start], 0, 0, 1, 0, 0)

    frontier = deque([(start, [start], 0)])   # (node, path, cost)
    explored = {start}
    nodes_generated = 1
    nodes_expanded  = 0
    max_frontier    = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        node, path, cost = frontier.popleft()
        nodes_expanded += 1

        for neighbour, edge_cost in adj.get(node, []):
            if neighbour == goal:
                nodes_generated += 1
                final_path = path + [neighbour]
                return _make_result(final_path, nodes_generated,
                                    nodes_expanded, max_frontier,
                                    cost + edge_cost, len(final_path) - 1)
            if neighbour not in explored:
                explored.add(neighbour)
                frontier.append((neighbour, path + [neighbour], cost + edge_cost))
                nodes_generated += 1

    return _make_result(None, nodes_generated, nodes_expanded, max_frontier, -1, -1)


# =============================================================
# ALGORITHM 2 – UNIFORM-COST SEARCH (UCS)  [Iterative, min-heap]
# =============================================================

def ucs(adj: dict, start: int, goal: int) -> dict:
    """
    UCS expands the lowest-cost path first (Dijkstra-style).
    Guarantees an optimal (minimum cost) solution.
    """
    if start == goal:
        return _make_result([start], 0, 0, 1, 0, 0)

    # (cumulative_cost, tie_break_id, node, path)
    counter = 0
    frontier = [(0, counter, start, [start])]
    heapq.heapify(frontier)
    explored = {}
    nodes_generated = 1
    nodes_expanded  = 0
    max_frontier    = 1

    while frontier:
        max_frontier = max(max_frontier, len(frontier))
        g_cost, _, node, path = heapq.heappop(frontier)
        nodes_expanded += 1

        if node == goal:
            return _make_result(path, nodes_generated, nodes_expanded,
                                max_frontier, g_cost, len(path) - 1)

        if node in explored and explored[node] <= g_cost:
            continue
        explored[node] = g_cost

        for neighbour, edge_cost in adj.get(node, []):
            new_cost = g_cost + edge_cost
            if neighbour not in explored:
                counter += 1
                heapq.heappush(frontier,
                               (new_cost, counter, neighbour, path + [neighbour]))
                nodes_generated += 1

    return _make_result(None, nodes_generated, nodes_expanded, max_frontier, -1, -1)


# =============================================================
# ALGORITHM 3 – ITERATIVE-DEEPENING DFS (IDDFS) [Recursive DLS]
# =============================================================

def iddfs(adj: dict, start: int, goal: int, max_depth_limit: int = 50) -> dict:
    """
    IDDFS performs depth-limited DFS recursively for increasing depth limits.
    Combines BFS optimality (on hop-count) with DFS space efficiency.
    """
    if start == goal:
        return _make_result([start], 0, 0, 1, 0, 0)

    total_generated = [0]
    total_expanded  = [0]
    max_frontier    = [1]

    def dls(node, goal, path, explored, depth_limit):
        """Recursive depth-limited search. Returns (found, cutoff)."""
        total_expanded[0] += 1
        if node == goal:
            return path, False

        if depth_limit == 0:
            return None, True   # cutoff

        cutoff_occurred = False
        for neighbour, _ in adj.get(node, []):
            if neighbour not in explored:
                explored.add(neighbour)
                total_generated[0] += 1
                max_frontier[0] = max(max_frontier[0], depth_limit)
                result, cutoff = dls(neighbour, goal,
                                     path + [neighbour],
                                     explored, depth_limit - 1)
                if result is not None:
                    return result, False
                if cutoff:
                    cutoff_occurred = True
                explored.discard(neighbour)
        return None, cutoff_occurred

    for depth in range(max_depth_limit + 1):
        explored = {start}
        total_generated[0] += 1
        result, cutoff = dls(start, goal, [start], explored, depth)
        if result is not None:
            path_cost = sum(
                min(c for n2, c in adj[result[i]] if n2 == result[i + 1])
                for i in range(len(result) - 1)
            )
            return _make_result(result, total_generated[0],
                                total_expanded[0], max_frontier[0],
                                path_cost, len(result) - 1)
        if not cutoff:
            break   # goal is unreachable

    return _make_result(None, total_generated[0], total_expanded[0],
                        max_frontier[0], -1, -1)


# =============================================================
# HELPERS
# =============================================================

def _make_result(path, generated, expanded, max_frontier, cost, depth):
    return {
        "path"        : path,
        "found"       : path is not None,
        "nodes_gen"   : generated,
        "nodes_exp"   : expanded,
        "max_frontier": max_frontier,
        "path_cost"   : cost,
        "depth"       : depth,
    }


def timed_run(func, adj, start, goal):
    """Run *func* 5 times and return (mean_time_ms, last_result)."""
    times = []
    result = None
    for _ in range(5):
        t0 = time.perf_counter()
        result = func(adj, start, goal)
        times.append((time.perf_counter() - t0) * 1000)
    return sum(times) / len(times), result


# =============================================================
# CORRECTNESS TESTS
# =============================================================

def run_correctness_tests():
    """Three mandatory test cases for each algorithm."""
    print("=" * 60)
    print("CORRECTNESS TESTS  (seed=42, 100 states)")
    print("=" * 60)
    adj = generate_hospital_graph(100, seed=42)
    algos = [("BFS", bfs), ("UCS", ucs), ("IDDFS", iddfs)]

    # Test A: reachable goal
    start, goal = 0, 99
    print(f"\nTest A – Reachable goal  (start={start}, goal={goal})")
    for name, fn in algos:
        r = fn(adj, start, goal)
        status = "PASS" if r["found"] else "FAIL"
        print(f"  {name:8s}: {status}  path_len={r['depth']}  cost={r['path_cost']:.0f}")

    # Test B: start == goal
    print(f"\nTest B – Start equals goal (node 0)")
    for name, fn in algos:
        r = fn(adj, 0, 0)
        status = "PASS" if r["found"] and r["depth"] == 0 else "FAIL"
        print(f"  {name:8s}: {status}  depth={r['depth']}")

    # Test C: unreachable goal (disconnected node)
    adj_disc = generate_hospital_graph(10, seed=42)
    adj_disc[999] = []          # isolated node
    for i in range(10):
        adj_disc[i] = [(n, c) for n, c in adj_disc[i] if n != 999]
    print(f"\nTest C – Unreachable goal (isolated node 999)")
    for name, fn in algos:
        r = fn(adj_disc, 0, 999)
        status = "PASS" if not r["found"] else "FAIL"
        print(f"  {name:8s}: {status}  found={r['found']}")

    print()


if __name__ == "__main__":
    run_correctness_tests()
