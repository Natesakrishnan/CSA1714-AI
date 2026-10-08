from itertools import permutations


def solve_cryptarithm():
    letters = "SENDMORY"

    for digits in permutations(range(10), len(letters)):

        S, E, N, D, M, O, R, Y = digits

        if S == 0 or M == 0:
            continue

        SEND = 1000 * S + 100 * E + 10 * N + D
        MORE = 1000 * M + 100 * O + 10 * R + E
        MONEY = (
            10000 * M +
            1000 * O +
            100 * N +
            10 * E +
            Y
        )

        if SEND + MORE == MONEY:

            print("Solution found!")
            print("S =", S)
            print("E =", E)
            print("N =", N)
            print("D =", D)
            print("M =", M)
            print("O =", O)
            print("R =", R)
            print("Y =", Y)

            print("\nEquation:")
            print("  ", SEND)
            print("+ ", MORE)
            print("-------")
            print(" ", MONEY)

            return

solve_cryptarithm()
