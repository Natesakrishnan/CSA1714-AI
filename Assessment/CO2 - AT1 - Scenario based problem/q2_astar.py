# Question 2 - A* Search: f(n) = g(n) + h(n)
import heapq
from q1_greedy import roads, h  # reuse the campus map from Q1

def a_star(start, goal):
    open_list = [(h[start], 0, start, [start])]
    best_g = {start: 0}
    step = 1
    while open_list:
        f, g, node, path = heapq.heappop(open_list)
        if g > best_g.get(node, float("inf")):
            continue
        print(f"Step {step}: expand {node:<10} g={g:<4} h={h[node]:<4} f={f}")
        step += 1
        if node == goal:
            return path, g
        for nb, w in roads[node].items():
            ng = g + w
            if ng < best_g.get(nb, float("inf")):
                best_g[nb] = ng
                print(f"        generate {nb:<10} g={ng:<4} h={h[nb]:<4} f={ng + h[nb]}")
                heapq.heappush(open_list, (ng + h[nb], ng, nb, path + [nb]))
    return None, float("inf")

path, dist = a_star("Gate", "Auditorium")
print("Route:", " -> ".join(path), "| Distance:", dist, "m")

# Admissibility check: true remaining distance (Dijkstra) vs straight-line h
def true_dist(src, goal="Auditorium"):
    pq, seen = [(0, src)], {}
    while pq:
        d, n = heapq.heappop(pq)
        if n in seen: continue
        seen[n] = d
        for nb, w in roads[n].items():
            heapq.heappush(pq, (d + w, nb))
    return seen[goal]

print("\nLocation   h(n)  true  h<=true")
for n in roads:
    t = true_dist(n)
    print(f"{n:<10} {h[n]:<5} {t:<5} {h[n] <= t}")
