from collections import deque

def is_valid(state):
    m_left, c_left, boat = state
    m_right = 3 - m_left
    c_right = 3 - c_left

    if m_left > 0 and c_left > m_left:
        return False

    if m_right > 0 and c_right > m_right:
        return False

    return True


def get_next_states(state):
    m_left, c_left, boat = state
    moves = [
        (1, 0),   # 1 missionary
        (2, 0),   # 2 missionaries
        (0, 1),   # 1 cannibal
        (0, 2),   # 2 cannibals
        (1, 1)    # 1 missionary and 1 cannibal
    ]

    next_states = []

    for m, c in moves:
        if boat == 0:  # Boat on left side
            new_state = (m_left - m, c_left - c, 1)

        else:          # Boat on right side
            new_state = (m_left + m, c_left + c, 0)

        if 0 <= new_state[0] <= 3 and 0 <= new_state[1] <= 3:
            if is_valid(new_state):
                next_states.append(new_state)

    return next_states


def solve():
    start = (3, 3, 0)
    goal = (0, 0, 1)

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if state == goal:
            return path

        for next_state in get_next_states(state):
            if next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state]))

    return None

solution = solve()

if solution:
    print("Solution found!\n")

    for state in solution:
        m, c, boat = state
        side = "Left" if boat == 0 else "Right"

        print(f"Missionaries Left: {m}, Cannibals Left: {c}, Boat: {side}")
else:
    print("No solution found.")
