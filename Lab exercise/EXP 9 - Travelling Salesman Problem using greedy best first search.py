import heapq

def tsp_greedy(graph, start):
    visited = {start}
    path = [start]
    total_cost = 0
    current = start

    while len(visited) < len(graph):
        min_cost = float('inf')
        next_city = None

        for city in graph[current]:
            if city not in visited and graph[current][city] < min_cost:
                min_cost = graph[current][city]
                next_city = city

        if next_city is None:
            print("No complete tour is possible.")
            return

        path.append(next_city)
        visited.add(next_city)
        total_cost += min_cost
        current = next_city

    if start not in graph[current]:
        print("Cannot return to the starting city.")
        return

    total_cost += graph[current][start]
    path.append(start)

    print("Tour:", " -> ".join(path))
    print("Total Cost:", total_cost)


# Graph representing cities and distances
graph = {
    'A': {'B': 10, 'C': 15, 'D': 20},
    'B': {'A': 10, 'C': 35, 'D': 25},
    'C': {'A': 15, 'B': 35, 'D': 30},
    'D': {'A': 20, 'B': 25, 'C': 30}
}

tsp_greedy(graph, 'A')
