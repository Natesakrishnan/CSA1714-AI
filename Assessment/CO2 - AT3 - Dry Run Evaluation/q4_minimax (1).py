"""
Question 4 - Minimax with a heuristic evaluation function
(a),(b) minimax on the given tree   (c) tic-tac-toe evaluation E
Course: Artificial Intelligence (CSA17) - Assessment Tool 3
"""

# ---------- (a), (b) Minimax ----------
# Root A (MAX) -> B1, B2 (MIN) -> C1..C4 (MAX) -> 8 leaves
LEAVES = [3, 5, 6, 9, 1, 2, 0, -1]


def minimax_tree(leaves):
    c = [max(leaves[i], leaves[i + 1]) for i in range(0, 8, 2)]   # C1..C4 (MAX)
    b = [min(c[0], c[1]), min(c[2], c[3])]                          # B1, B2 (MIN)
    a = max(b)                                                      # A (MAX)
    return c, b, a


# ---------- (c) Heuristic evaluation E ----------
# E = (lines still open for X) - (lines still open for O)
BOARD = [["X", "O", " "],
         [" ", "X", " "],
         [" ", " ", "O"]]
LINES = {
    "Row 1": [(0, 0), (0, 1), (0, 2)], "Row 2": [(1, 0), (1, 1), (1, 2)],
    "Row 3": [(2, 0), (2, 1), (2, 2)], "Col 1": [(0, 0), (1, 0), (2, 0)],
    "Col 2": [(0, 1), (1, 1), (2, 1)], "Col 3": [(0, 2), (1, 2), (2, 2)],
    "Diag \\": [(0, 0), (1, 1), (2, 2)], "Diag /": [(0, 2), (1, 1), (2, 0)],
}


def evaluate(board):
    open_x = open_o = 0
    rows = []
    for name, line in LINES.items():
        cells = [board[r][c] for r, c in line]
        x_open = "O" not in cells      # no O in the line -> open for X
        o_open = "X" not in cells      # no X in the line -> open for O
        open_x += x_open
        open_o += o_open
        rows.append((name, cells, x_open, o_open))
    return open_x, open_o, rows


if __name__ == "__main__":
    print("=== (a) Minimax backed-up values ===")
    c, b, a = minimax_tree(LEAVES)
    for i, v in enumerate(c, 1):
        print(f"C{i} (MAX) = {v}")
    for i, v in enumerate(b, 1):
        print(f"B{i} (MIN) = {v}")
    print(f"A  (MAX, root) = {a}")

    print("\n=== (b) Best first move and principal variation ===")
    best = 0 if b[0] >= b[1] else 1                       # MAX picks the larger B
    print("Best first move:", "Left (B1)" if best == 0 else "Right (B2)")
    k = best * 2                                          # its two MAX children C(k+1), C(k+2)
    c_idx = k if c[k] <= c[k + 1] else k + 1              # MIN picks the smaller C
    l = c_idx * 2                                         # its two leaves
    leaf = max(LEAVES[l], LEAVES[l + 1])                  # MAX picks the larger leaf
    print(f"Principal variation: A -> B{best + 1} -> C{c_idx + 1} -> leaf {leaf}")

    print("\n=== (c) Tic-tac-toe evaluation E ===")
    ox, oo, rows = evaluate(BOARD)
    for name, cells, xo, oo_ in rows:
        print(f"{name:<7}{str(cells):<22} open for X: {xo!s:<6} open for O: {oo_}")
    print(f"Lines open for X = {ox}, lines open for O = {oo}")
    print(f"E = {ox} - {oo} = {ox - oo}")
