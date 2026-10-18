# Question 4 - Minimax on a Max-Min-Max tree
tree = [  # X move -> O reply -> X final-move scores
    [[4, 7], [8, 2]],   # first move A (left)
    [[3, 5], [6, 9]],   # first move B (right)
]
def minimax(node, is_max, label):
    if isinstance(node, int):
        return node
    vals = [minimax(c, not is_max, f"{label}{i+1}") for i, c in enumerate(node)]
    v = max(vals) if is_max else min(vals)
    print(f"{'MAX' if is_max else 'MIN'} node {label or 'root':<5} children={vals} -> {v}")
    return v

best = minimax(tree, True, "")
print("Value of the game for X:", best)
