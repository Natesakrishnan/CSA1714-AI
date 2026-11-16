"""Task 4 - Depth-limited minimax on Connect-k (gravity board). Player +1 = MAX (our AI), -1 = MIN."""
import random, time, json, sys
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

class Game:
    def __init__(s, rows, cols, k):
        s.R, s.C, s.K = rows, cols, k
        s.b = [[0]*cols for _ in range(rows)]; s.h = [0]*cols
        s.windows = []
        for r in range(rows):
            for c in range(cols):
                for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
                    cells = [(r+i*dr, c+i*dc) for i in range(k)]
                    if all(0 <= a < rows and 0 <= bb < cols for a, bb in cells): s.windows.append(cells)
    def moves(s): return [c for c in range(s.C) if s.h[c] < s.R]
    def play(s, c, p): r = s.h[c]; s.b[r][c] = p; s.h[c] += 1; return r
    def undo(s, c): s.h[c] -= 1; s.b[s.h[c]][c] = 0
    def wins(s, r, c, p):
        for dr, dc in ((0,1),(1,0),(1,1),(1,-1)):
            n = 1
            for sg in (1, -1):
                a, bb = r+sg*dr, c+sg*dc
                while 0 <= a < s.R and 0 <= bb < s.C and s.b[a][bb] == p: n += 1; a += sg*dr; bb += sg*dc
            if n >= s.K: return True
        return False
    def evaluate(s):
        """Heuristic: sum over all k-windows that are 'open' for one player only: 10^(count-1); MAX positive, MIN negative. Centre bonus."""
        tot = 0
        for w in s.windows:
            a = bb = 0
            for r, c in w:
                v = s.b[r][c]
                if v == 1: a += 1
                elif v == -1: bb += 1
            if a and not bb: tot += 10**(a-1)
            elif bb and not a: tot -= 10**(bb-1)
        mid = s.C//2
        for r in range(s.R):
            for c in range(s.C): tot += s.b[r][c]*(s.C//2 - abs(c-mid))
        return tot

WIN = 10**6
def minimax(g, depth, p, cnt, last=None):
    """cnt: visited (every call), expanded (children generated), evals (heuristic calls at cutoff), terminal (win/draw leaves)."""
    cnt["visited"] += 1
    if last is not None and g.wins(last[0], last[1], -p): cnt["terminal"] += 1; return -WIN - depth*0 if p == 1 else WIN   # previous mover won
    mv = g.moves()
    if not mv: cnt["terminal"] += 1; return 0
    if depth == 0: cnt["evals"] += 1; return g.evaluate()
    cnt["expanded"] += 1
    best = -10**9 if p == 1 else 10**9
    for c in mv:
        r = g.play(c, p); v = minimax(g, depth-1, -p, cnt, (r, c)); g.undo(c)
        best = max(best, v) if p == 1 else min(best, v)
    return best

def choose(g, depth, p, cnt):
    """Root move selection (counts the root as one expanded node)."""
    best = None; bv = -10**9 if p == 1 else 10**9
    cnt["visited"] += 1; cnt["expanded"] += 1
    for c in g.moves():
        r = g.play(c, p)
        cnt["visited"] += 1                                   # the child node itself
        if g.wins(r, c, p): cnt["terminal"] += 1; v = WIN if p == 1 else -WIN
        elif depth == 1: cnt["evals"] += 1; v = g.evaluate()
        else:
            cnt["visited"] -= 1                               # minimax() counts its own visit
            v = minimax(g, depth-1, -p, cnt, (r, c))
        g.undo(c)
        if best is None or (p == 1 and v > bv) or (p == -1 and v < bv): best, bv = c, v
    return best

def play_game(R, C, K, depth, ai_first, rnd):
    g = Game(R, C, K); p = 1 if ai_first else -1; ai = 1; last = None
    while True:
        mv = g.moves()
        if not mv: return 0
        if p == ai: c = choose(g, depth, ai, {"visited": 0, "expanded": 0, "evals": 0, "terminal": 0})
        else: c = rnd.choice(mv)
        r = g.play(c, p)
        if g.wins(r, c, p): return 1 if p == ai else -1
        p = -p

if __name__ == "__main__":
    out = {"growth": [], "winrate": []}
    CFG = {(4, 4, 3): 7, (5, 5, 4): 6, (6, 7, 4): 6}            # config -> max depth measured
    for (R, C, K), D in CFG.items():
        for d in range(1, D+1):
            g = Game(R, C, K); cnt = {"visited": 0, "expanded": 0, "evals": 0, "terminal": 0}
            t0 = time.perf_counter(); mv = choose(g, d, 1, cnt); dt = time.perf_counter()-t0
            b = C; theo_nodes = sum(b**i for i in range(d+1)); theo_leaf = b**d
            out["growth"].append(dict(R=R, C=C, K=K, depth=d, visited=cnt["visited"], expanded=cnt["expanded"], evals=cnt["evals"], terminal=cnt["terminal"],
                                      theory_visited=theo_nodes, theory_leaves=theo_leaf, time_s=round(dt, 3), move=mv))
            print(out["growth"][-1], flush=True)
    for (R, C, K), maxd in (((4, 4, 3), 4), ((5, 5, 4), 4), ((6, 7, 4), 4)):
        for d in range(1, maxd+1):
            rnd = random.Random(100+d); w = dr = l = 0; t0 = time.perf_counter()
            for gi in range(20):
                res = play_game(R, C, K, d, gi % 2 == 0, rnd); w += res == 1; dr += res == 0; l += res == -1
            out["winrate"].append(dict(R=R, C=C, K=K, depth=d, wins=w, draws=dr, losses=l, time_s=round(time.perf_counter()-t0, 1)))
            print(out["winrate"][-1], flush=True)
    json.dump(out, open("results/task4.json", "w"), indent=1)
    # growth figure
    plt.figure(figsize=(6.5, 4.2))
    for (R, C, K) in CFG:
        rows = [x for x in out["growth"] if (x["R"], x["C"], x["K"]) == (R, C, K)]
        plt.semilogy([x["depth"] for x in rows], [x["visited"] for x in rows], "o-", label=f"{R}x{C} k={K} measured (b={C})")
        plt.semilogy([x["depth"] for x in rows], [x["theory_visited"] for x in rows], "k--", linewidth=0.8)
    plt.xlabel("Lookahead depth d"); plt.ylabel("Nodes visited (log scale)"); plt.grid(alpha=.3); plt.legend(fontsize=8)
    plt.title("Plain minimax: measured nodes (solid) vs (b^(d+1)-1)/(b-1) (dashed)"); plt.tight_layout(); plt.savefig("results/fig_task4_growth.png", dpi=130)
