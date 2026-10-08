start = (1, 1)
goal = (5, 5)

blocked = {
    (2, 2), (2, 3),
    (3, 3),
    (4, 2), (4, 4)
}

moves = [
    (-1, 0),  # Up
    (1, 0),   # Down
    (0, -1),  # Left
    (0, 1)    # Right
]

stack = [start]
visited = {start}
parent = {start: None}

while stack:
    current = stack.pop()

    if current == goal:
        break

    r, c = current

    for dr, dc in reversed(moves):
        next_cell = (r + dr, c + dc)

        if (1 <= next_cell[0] <= 5 and
            1 <= next_cell[1] <= 5 and
            next_cell not in blocked and
            next_cell not in visited):

            visited.add(next_cell)
            parent[next_cell] = current
            stack.append(next_cell)

path = []
current = goal

while current is not None:
    path.append(current)
    current = parent[current]

path.reverse()

print("DFS Path:")
print(path)
print("Total Cost:", len(path) - 1)
