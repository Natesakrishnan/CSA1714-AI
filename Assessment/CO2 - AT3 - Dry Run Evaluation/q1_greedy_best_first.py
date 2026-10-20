"""
Question 1 - Greedy Best-First Search (S to G)
Course: Artificial Intelligence (CSA17) - Assessment Tool 3
Priority of the open list = h(n) only.
"""

# Road network (undirected) with step costs
EDGES = [("S", "A", 2), ("S", "B", 3), ("A", "C", 4), ("A", "D", 7),
         ("B", "D", 2), ("B", "E", 6), ("C", "G", 6), ("D", "G", 3),
         ("E", "G", 2)]
# Heuristic values h(n) = estimated cost to goal G
H = {"S": 7, "A": 8, "B": 4, "C": 5, "D": 3, "E": 2, "G": 0}

GRAPH = {n: {} for n in H}
for u, v, c in EDGES:
    GRAPH[u][v] = c
    GRAPH[v][u] = c


def path_cost(path):
    return sum(GRAPH[a][b] for a, b in zip(path, path[1:]))


def greedy_best_first(start, goal):
    open_list = {start: H[start]}        # node -> h
    parent = {start: None}
    closed = set()
    steps = []
    while open_list:
        # expand the node with the smallest h (ties -> alphabetical)
        node = min(open_list, key=lambda n: (open_list[n], n))
        del open_list[node]
        closed.add(node)
        if node == goal:
            steps.append((node, dict(open_list)))
            break
        for nb in GRAPH[node]:
            if nb not in closed and nb not in open_list:
                open_list[nb] = H[nb]
                parent[nb] = node
        steps.append((node, dict(open_list)))
    # rebuild the path
    path, n = [], goal
    while n is not None:
        path.append(n)
        n = parent[n]
    return path[::-1], steps


def fmt_open(open_list):
    items = sorted(open_list.items(), key=lambda kv: (kv[1], kv[0]))
    return ", ".join(f"{n}:{h}" for n, h in items) or "(empty)"


if __name__ == "__main__":
    print("Initial open list: S:7\n")
    path, steps = greedy_best_first("S", "G")
    print(f"{'Step':<6}{'Node expanded':<16}Open list after expansion (node: h)")
    for i, (node, op) in enumerate(steps, 1):
        print(f"{i:<6}{node:<16}{fmt_open(op)}")

    print("\n(b) Path found :", " -> ".join(path), "| total cost =", path_cost(path))

    alt = ["S", "B", "D", "G"]
    print("(c) Alternative:", " -> ".join(alt), "| total cost =", path_cost(alt))
    print("    Greedy path optimal?", path_cost(path) <= path_cost(alt))
