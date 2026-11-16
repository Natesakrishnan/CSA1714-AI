"""Task 3 - Alpha-beta behaviour on engineered game trees (uniform branching b, depth d). Leaves are ints."""
import random, json, statistics as st, sys
sys.setrecursionlimit(10000)

def build(b, d, leaf):                      # leaf() gives each leaf value
    return leaf() if d == 0 else [build(b, d-1, leaf) for _ in range(b)]

def minimax(node, is_max, c):
    c["nodes"] += 1
    if not isinstance(node, list): return node
    vals = [minimax(ch, not is_max, c) for ch in node]
    return max(vals) if is_max else min(vals)

def alphabeta(node, is_max, alpha, beta, c):
    c["nodes"] += 1
    if not isinstance(node, list): c["leaves"] += 1; return node
    if is_max:
        v = -10**9
        for ch in node:
            v = max(v, alphabeta(ch, False, alpha, beta, c)); alpha = max(alpha, v)
            if alpha >= beta: c["cutoffs"] += 1; break
        return v
    v = 10**9
    for ch in node:
        v = min(v, alphabeta(ch, True, alpha, beta, c)); beta = min(beta, v)
        if alpha >= beta: c["cutoffs"] += 1; break
    return v

def reorder(node, is_max, best):
    """Return (value, tree) where every node's children are re-sorted: best-first (best=True) or worst-first (best=False)."""
    if not isinstance(node, list): return node, node
    kids = [reorder(ch, not is_max, best) for ch in node]
    kids.sort(key=lambda x: x[0], reverse=(is_max == best))      # MAX+best -> descending; MIN+best -> ascending
    return (max if is_max else min)(k[0] for k in kids), [k[1] for k in kids]

def nested_adversarial(b, d, is_max=True, lo=0):
    """Sibling subtrees get disjoint, nested value blocks: ascending for MAX nodes, descending for MIN nodes, so the best child
    is always searched LAST and every leaf lies strictly inside the (alpha,beta) window -> no cutoff can fire."""
    if d == 0: return lo
    size = b**(d-1)
    order = range(b) if is_max else range(b-1, -1, -1)
    return [nested_adversarial(b, d-1, not is_max, lo + k*size) for k in order]

def run(tree):
    c1 = {"nodes": 0}; v1 = minimax(tree, True, c1)
    c2 = {"nodes": 0, "leaves": 0, "cutoffs": 0}; v2 = alphabeta(tree, True, -10**9, 10**9, c2)
    assert v1 == v2, "alpha-beta must return the minimax value"
    return dict(value=v1, minimax_nodes=c1["nodes"], ab_nodes=c2["nodes"], ab_leaves=c2["leaves"], cutoffs=c2["cutoffs"])

def predicted_best_nodes(b, d): return sum(b**((k+1)//2) + b**(k//2) - 1 for k in range(d+1))
def predicted_best_leaves(b, d): return b**((d+1)//2) + b**(d//2) - 1
def total_nodes(b, d): return (b**(d+1)-1)//(b-1)

def permuted_tree(b, d, seed):
    leaves = list(range(b**d)); random.Random(seed).shuffle(leaves); it = iter(leaves)
    return build(b, d, lambda: next(it))

if __name__ == "__main__":
    out = []
    for (b, d) in ((3, 6), (4, 4), (4, 6), (4, 8), (5, 6)):
        T = permuted_tree(b, d, 1)
        best = reorder(T, True, True)[1]; worst = reorder(T, True, False)[1]
        eq = build(b, d, lambda: 0)
        rows = {"best_order": run(best), "sorted_worst_order": run(worst), "nested_adversarial": run(nested_adversarial(b, d)), "equal_leaves": run(eq)}
        rnd = [run(permuted_tree(b, d, s)) for s in range(30)]                       # 30 random trees
        rows["random_order"] = {k: round(st.mean(r[k] for r in rnd), 1) for k in rnd[0]}
        rows["random_order"]["ab_nodes_min"] = min(r["ab_nodes"] for r in rnd); rows["random_order"]["ab_nodes_max"] = max(r["ab_nodes"] for r in rnd)
        out.append(dict(b=b, d=d, total=total_nodes(b, d), pred_best_nodes=predicted_best_nodes(b, d), pred_best_leaves=predicted_best_leaves(b, d), leaves_total=b**d, **rows))
        print(b, d, json.dumps(out[-1]))
    json.dump(out, open("results/task3.json", "w"), indent=1)
