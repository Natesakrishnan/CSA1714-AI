"""
Question 2 - A* Search (S to G) with f(n) = g(n) + h(n)
Also checks whether h(n) is admissible.
Course: Artificial Intelligence (CSA17) - Assessment Tool 3
"""
import heapq
from math import inf

EDGES = [("S", "A", 2), ("S", "B", 3), ("A", "C", 4), ("A", "D", 7),
         ("B", "D", 2), ("B", "E", 6), ("C", "G", 6), ("D", "G", 3),
         ("E", "G", 2)]
H = {"S": 7, "A": 8, "B": 4, "C": 5, "D": 3, "E": 2, "G": 0}

GRAPH = {n: {} for n in H}
for u, v, c in EDGES:
    GRAPH[u][v] = c
    GRAPH[v][u] = c


def a_star(start, goal):
    g = {start: 0}
    parent = {start: None}
    open_list = {start: H[start]}        # node -> f
    closed = set()
    steps = []
    while open_list:
        node = min(open_list, key=lambda n: (open_list[n], n))
        del open_list[node]
        if node == goal:
            steps.append((node, {n: (g[n], H[n]) for n in open_list}))
            break
        closed.add(node)
        for nb, cost in GRAPH[node].items():
            new_g = g[node] + cost
            if new_g < g.get(nb, inf):
                g[nb] = new_g
                parent[nb] = node
                open_list[nb] = new_g + H[nb]
                closed.discard(nb)
        steps.append((node, {n: (g[n], H[n]) for n in open_list}))
    path, n = [], goal
    while n is not None:
        path.append(n)
        n = parent[n]
    return path[::-1], g[goal], steps


def fmt_open(open_list):
    items = sorted(open_list.items(), key=lambda kv: (kv[1][0] + kv[1][1], kv[0]))
    return ", ".join(f"{n}: {g}+{h}={g + h}" for n, (g, h) in items) or "(empty)"


def true_costs(goal):
    """True remaining cost h*(n) = cheapest path to goal (Dijkstra from goal)."""
    dist = {n: inf for n in GRAPH}
    dist[goal] = 0
    pq = [(0, goal)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, c in GRAPH[u].items():
            if d + c < dist[v]:
                dist[v] = d + c
                heapq.heappush(pq, (dist[v], v))
    return dist


if __name__ == "__main__":
    print("Initial open list: S: 0+7=7\n")
    path, cost, steps = a_star("S", "G")
    print(f"{'Step':<6}{'Node expanded':<16}Open list after expansion (node: g+h=f)")
    for i, (node, op) in enumerate(steps, 1):
        print(f"{i:<6}{node:<16}{fmt_open(op)}")
    print("\n(b) Path found:", " -> ".join(path), "| cost =", cost)
    print("    (Greedy search in Q1 gave S -> B -> E -> G with cost 11)")

    print("\n(c) Admissibility check: h(n) <= h*(n) ?")
    true = true_costs("G")
    print(f"{'Node':<6}{'h(n)':<7}{'h*(n)':<8}admissible?")
    for n in "SABCDEG":
        print(f"{n:<6}{H[n]:<7}{true[n]:<8}{H[n] <= true[n]}")
    print("h is admissible:", all(H[n] <= true[n] for n in H))
    consistent = all(H[u] <= c + H[v] for u in GRAPH for v, c in GRAPH[u].items())
    print("h is consistent:", consistent)
