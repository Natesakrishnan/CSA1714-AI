# Question 1 - Greedy Best-First Search (campus delivery robot)
roads = {
    "Gate":      {"Library": 120, "Canteen": 200},
    "Library":   {"Gate": 120, "Lab": 150, "Hostel": 300},
    "Canteen":   {"Gate": 200, "Hostel": 100, "Admin": 260},
    "Lab":       {"Library": 150, "Auditorium": 350},
    "Hostel":    {"Library": 300, "Canteen": 100, "Auditorium": 180},
    "Admin":     {"Canteen": 260, "Auditorium": 120},
    "Auditorium": {"Lab": 350, "Hostel": 180, "Admin": 120},
}
h = {"Gate": 400, "Library": 330, "Canteen": 240, "Lab": 280,
     "Hostel": 160, "Admin": 110, "Auditorium": 0}

def greedy(start, goal):
    current, visited, path, total = start, {start}, [start], 0
    step = 1
    while current != goal:
        cands = {n: h[n] for n in roads[current] if n not in visited}
        print(f"Step {step}: expand {current:<10} candidates (h) = {cands}")
        nxt = min(cands, key=cands.get)
        total += roads[current][nxt]
        visited.add(nxt); path.append(nxt); current = nxt; step += 1
    return path, total

if __name__ == "__main__":
    path, dist = greedy("Gate", "Auditorium")
    print("Route:", " -> ".join(path), "| Distance:", dist, "m")
