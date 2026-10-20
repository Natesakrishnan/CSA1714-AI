"""
Question 5 - Alpha-Beta Pruning on a depth-4 binary tree
Root MAX, then MIN, MAX, MIN, with 16 leaves at the bottom.
Course: Artificial Intelligence (CSA17) - Assessment Tool 3
"""

LEAVES = [8, 6, 5, 7, 2, 9, 4, 3, 6, 1, 5, 2, 9, 7, 3, 4]
INF = float("inf")


def plain_minimax(depth, index, is_max, counter):
    """Ordinary minimax (no pruning); counter[0] counts leaves evaluated."""
    if depth == 4:
        counter[0] += 1
        return LEAVES[index]
    vals = [plain_minimax(depth + 1, 2 * index + i, not is_max, counter) for i in (0, 1)]
    return max(vals) if is_max else min(vals)


def alpha_beta(depth, index, is_max, alpha, beta, stats, name):
    """Alpha-beta pruning, visiting children left to right."""
    if depth == 4:
        stats["leaves"] += 1
        stats["trace"].append(f"{name}: leaf = {LEAVES[index]}")
        return LEAVES[index]
    stats["trace"].append(f"{name} ({'MAX' if is_max else 'MIN'}) entry  alpha={alpha}  beta={beta}")
    value = -INF if is_max else INF
    for i in (0, 1):
        v = alpha_beta(depth + 1, 2 * index + i, not is_max, alpha, beta, stats, f"{name}{i}")
        if is_max:
            value = max(value, v)
            alpha = max(alpha, value)
        else:
            value = min(value, v)
            beta = min(beta, value)
        if alpha >= beta:                       # cut-off
            if i == 0:
                stats["pruned"].append(f"{name}{1} pruned  (alpha={alpha} >= beta={beta})")
            break
    stats["trace"].append(f"{name} returns {value}")
    return value


if __name__ == "__main__":
    stats = {"leaves": 0, "trace": [], "pruned": []}
    root = alpha_beta(0, 0, True, -INF, INF, stats, "n")

    print("=== (a) Alpha-beta trace (n = root; digits = child path, 0 left, 1 right) ===")
    print("\n".join(stats["trace"]))
    print("\nPruned branches:")
    for p in stats["pruned"]:
        print("  ", p)
    print("Value of the root:", root)

    counter = [0]
    root_plain = plain_minimax(0, 0, True, counter)
    print("\n=== (b) Comparison with plain minimax ===")
    print(f"Alpha-beta : root = {root},       leaves evaluated = {stats['leaves']} of 16")
    print(f"Minimax    : root = {root_plain}, leaves evaluated = {counter[0]} of 16")
    print("Same root value:", root == root_plain)
