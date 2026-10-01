from collections import deque

def solve_8_puzzle(start, goal):
    queue = deque([(start, [])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path + [state]

        zero = state.index(0)
        row, col = divmod(zero, 3)

        moves = [
            (-1, 0), 
            (1, 0),  
            (0, -1),  
            (0, 1)    
        ]

        for dr, dc in moves:
            nr, nc = row + dr, col + dc

            if 0 <= nr < 3 and 0 <= nc < 3:
                new_zero = nr * 3 + nc
                new_state = list(state)

                new_state[zero], new_state[new_zero] = \
                    new_state[new_zero], new_state[zero]

                new_state = tuple(new_state)

                if new_state not in visited:
                    visited.add(new_state)
                    queue.append((new_state, path + [state]))

    return None


def display(state):
    for i in range(0, 9, 3):
        print(state[i:i+3])
    print()

start = (1, 2, 3,
         4, 0, 6,
         7, 5, 8)

goal = (1, 2, 3,
        4, 5, 6,
        7, 8, 0)

solution = solve_8_puzzle(start, goal)

if solution:
    print("Solution found!")
    print("Number of moves:", len(solution) - 1)

    for step, state in enumerate(solution):
        print("Step", step)
        display(state)
else:
    print("No solution exists.")
