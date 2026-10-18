# Question 5 - Alpha-Beta pruning (Max root, Min replies)
moves = {"M1": [6, 9, 7], "M2": [4, 8, 10], "M3": [7, 5, 12]}
alpha, beta = float("-inf"), float("inf")
best_move, scored = None, 0
for m, replies in moves.items():
    b = beta
    val = float("inf")
    for i, s in enumerate(replies):
        scored += 1
        val = min(val, s); b = min(b, val)
        print(f"{m}: score {s}  -> best so far for MIN (beta) = {b}, alpha = {alpha}")
        if b <= alpha:
            skipped = replies[i+1:]
            print(f"   PRUNE {m}: beta {b} <= alpha {alpha}; skipped {skipped}")
            break
    if val > alpha:
        alpha, best_move = val, m
    print(f"   {m} value = {val if val>=alpha else '<= ' + str(val)} | alpha = {alpha}")
print(f"\nPositions scored: {scored} of 9 | Best move: {best_move} | Value: {alpha}")
full = max(min(r) for r in moves.values())
print("Full minimax value:", full, "-> same result:", full == alpha)
