<<<<<<< HEAD
import heapq

def astar(graph, heuristic, start, goal):
    pq = [(heuristic[start], 0, start, [start])]
    visited = set()

    while pq:
        f, g, current, path = heapq.heappop(pq)

        if current == goal:
            print("Path:", " -> ".join(path))
            print("Total Cost:", g)
            return

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(
                    pq, (new_f, new_g, neighbor, path + [neighbor])
                )

    print("No path found")


graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'D': 3}
}

heuristic = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 3,
    'E': 0
}

astar(graph, heuristic, 'A', 'E')
=======
import heapq

def astar(graph, heuristic, start, goal):
    pq = [(heuristic[start], 0, start, [start])]
    visited = set()

    while pq:
        f, g, current, path = heapq.heappop(pq)

        if current == goal:
            print("Path:", " -> ".join(path))
            print("Total Cost:", g)
            return

        if current in visited:
            continue

        visited.add(current)

        for neighbor, cost in graph[current].items():
            if neighbor not in visited:
                new_g = g + cost
                new_f = new_g + heuristic[neighbor]
                heapq.heappush(
                    pq, (new_f, new_g, neighbor, path + [neighbor])
                )

    print("No path found")


graph = {
    'A': {'B': 1, 'C': 4},
    'B': {'A': 1, 'C': 2, 'D': 5},
    'C': {'A': 4, 'B': 2, 'D': 1},
    'D': {'B': 5, 'C': 1, 'E': 3},
    'E': {'D': 3}
}

heuristic = {
    'A': 7,
    'B': 6,
    'C': 4,
    'D': 3,
    'E': 0
}

astar(graph, heuristic, 'A', 'E')
>>>>>>> origin/main
