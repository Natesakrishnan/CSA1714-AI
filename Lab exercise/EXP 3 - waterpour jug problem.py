def water_jug(cap1, cap2, target):

    visited = set()

    def dfs(jug1, jug2, path):

        if jug1 == target or jug2 == target:
            path.append((jug1, jug2))
            return True

        if (jug1, jug2) in visited:
            return False

        visited.add((jug1, jug2))
        path.append((jug1, jug2))


        states = [
            (cap1, jug2),  
            (jug1, cap2),  
            (0, jug2),     
            (jug1, 0),     # Empty Jug 2

            (
                jug1 - min(jug1, cap2 - jug2),
                jug2 + min(jug1, cap2 - jug2)
            ),

            (
                jug1 + min(jug2, cap1 - jug1),
                jug2 - min(jug2, cap1 - jug1)
            )
        ]

        for new_jug1, new_jug2 in states:

            if dfs(new_jug1, new_jug2, path):
                return True
        path.pop()
        return False

    path = []

    if dfs(0, 0, path):
        return path

    return None


cap1 = 4
cap2 = 3

target = 2

solution = water_jug(cap1, cap2, target)

if solution:
    print("Solution found!")

    for step, state in enumerate(solution):
        print("Step", step, ":", state)
else:
    print("No solution exists.")
