"""Task 2 - Online DFS agent (and LRTA*) in unmapped mazes. Agent senses only the 4 neighbouring cells."""
import random, json, statistics as st
from collections import deque

DIRS = ((-1,0),(0,1),(1,0),(0,-1))

def gen_maze(m, braid, seed):
    """m x m cell perfect maze (recursive backtracker) -> grid (2m+1)^2; 1=free,0=wall. braid = fraction of dead ends removed."""
    rnd = random.Random(seed); N = 2*m+1
    g = [[0]*N for _ in range(N)]; g[1][1] = 1; stack = [(1,1)]
    while stack:
        r, c = stack[-1]
        nb = [(r+2*dr, c+2*dc, r+dr, c+dc) for dr, dc in DIRS if 0 < r+2*dr < N and 0 < c+2*dc < N and g[r+2*dr][c+2*dc] == 0]
        if nb:
            r2, c2, wr, wc = rnd.choice(nb); g[wr][wc] = 1; g[r2][c2] = 1; stack.append((r2, c2))
        else: stack.pop()
    if braid > 0:
        for r in range(1, N, 2):
            for c in range(1, N, 2):
                if sum(g[r+dr][c+dc] for dr, dc in DIRS) == 1 and rnd.random() < braid:
                    opts = [(r+dr, c+dc) for dr, dc in DIRS if 0 < r+2*dr < N and 0 < c+2*dc < N and g[r+dr][c+dc] == 0]
                    if opts: wr, wc = rnd.choice(opts); g[wr][wc] = 1
    return g

def dead_end_density(g):
    N = len(g); free = 0; de = 0
    for r in range(N):
        for c in range(N):
            if g[r][c]:
                free += 1
                if sum(g[r+dr][c+dc] for dr, dc in DIRS if 0 <= r+dr < N and 0 <= c+dc < N) == 1: de += 1
    return de/free

def bfs(g, s):
    N = len(g); d = {s: 0}; q = deque([s])
    while q:
        r, c = q.popleft()
        for dr, dc in DIRS:
            t = (r+dr, c+dc)
            if 0 <= t[0] < N and 0 <= t[1] < N and g[t[0]][t[1]] and t not in d: d[t] = d[(r, c)]+1; q.append(t)
    return d

def online_dfs(g, s, target):
    """Agent knows only its position and which neighbours are free. Returns moves, backtrack(revisit) moves, distinct cells, found."""
    N = len(g); visited = {s}; stack = []; pos = s; moves = 0; back = 0
    while pos != target:
        nxt = None
        for dr, dc in DIRS:
            t = (pos[0]+dr, pos[1]+dc)
            if 0 <= t[0] < N and 0 <= t[1] < N and g[t[0]][t[1]] and t not in visited: nxt = t; break
        if nxt: stack.append(pos); pos = nxt; visited.add(pos); moves += 1
        elif stack: pos = stack.pop(); moves += 1; back += 1
        else: return dict(moves=moves, back=back, distinct=len(visited), found=False)
    return dict(moves=moves, back=back, distinct=len(visited), found=True)

def lrta_star(g, s, target, trials, H=None):
    """LRTA*: H persists across trials. Goal coordinates are known (assumption), map is not. Returns moves per trial."""
    N = len(g); H = {} if H is None else H; per = []
    h0 = lambda p: abs(p[0]-target[0])+abs(p[1]-target[1])
    for _ in range(trials):
        pos = s; moves = 0
        while pos != target and moves < 200000:
            nbrs = [(pos[0]+dr, pos[1]+dc) for dr, dc in DIRS if 0 <= pos[0]+dr < N and 0 <= pos[1]+dc < N and g[pos[0]+dr][pos[1]+dc]]
            cost = [(1+H.get(t, h0(t)), i, t) for i, t in enumerate(nbrs)]
            best = min(cost)
            H[pos] = best[0]; pos = best[2]; moves += 1
        per.append(moves)
    return per

def mean(x): return round(st.mean(x), 2)

if __name__ == "__main__":
    out = {}
    SEEDS = range(20)
    # ---- Exp A: target distance (21x21 grid perfect maze, m=10)
    A = {}
    for q in (0.25, 0.5, 0.75, 1.0):
        rows = []
        for sd in SEEDS:
            g = gen_maze(10, 0.0, sd); d = bfs(g, (1,1)); mx = max(d.values())
            tgt = min(d, key=lambda k: abs(d[k]-q*mx)); r = online_dfs(g, (1,1), tgt); opt = d[tgt]
            rows.append((opt, r["moves"], r["back"], r["moves"]/opt))
        A[q] = dict(opt=mean([x[0] for x in rows]), moves=mean([x[1] for x in rows]), back=mean([x[2] for x in rows]),
                    ratio_mean=mean([x[3] for x in rows]), ratio_min=round(min(x[3] for x in rows), 2), ratio_max=round(max(x[3] for x in rows), 2))
    out["distance"] = A
    # ---- Exp B: unreachable target
    B = []
    for m in (6, 11, 16, 21):
        rows = []
        for sd in SEEDS:
            g = gen_maze(m, 0.0, sd); N = len(g); tgt = (N-2, N-2)
            for dr, dc in DIRS: g[tgt[0]+dr][tgt[1]+dc] = 0     # wall the target in
            reach = len(bfs(g, (1,1))); r = online_dfs(g, (1,1), tgt)
            rows.append((reach, r["moves"], r["found"]))
        B.append(dict(grid=2*m+1, reachable=mean([x[0] for x in rows]), moves=mean([x[1] for x in rows]),
                      two_R_minus_2=mean([2*(x[0]-1) for x in rows]), any_found=any(x[2] for x in rows)))
    out["unreachable"] = B
    # ---- Exp C: size x dead-end density (target = farthest cell)
    C = []
    for m in (6, 11, 16, 21):
        for braid in (0.0, 0.5, 1.0):
            rows = []
            for sd in SEEDS:
                g = gen_maze(m, braid, sd); d = bfs(g, (1,1)); tgt = max(d, key=d.get); r = online_dfs(g, (1,1), tgt)
                rows.append((dead_end_density(g), d[tgt], r["moves"], r["back"], r["moves"]/d[tgt], len(d)))
            C.append(dict(grid=2*m+1, braid=braid, dead_end_density=round(mean([x[0] for x in rows]), 3), free=mean([x[5] for x in rows]),
                          opt=mean([x[1] for x in rows]), moves=mean([x[2] for x in rows]), back=mean([x[3] for x in rows]),
                          ratio=mean([x[4] for x in rows]), ratio_max=round(max(x[4] for x in rows), 2)))
    out["size_density"] = C
    # ---- Exp D: LRTA* across 10 trials (21x21 and 31x31, perfect maze, farthest target)
    D = []
    for m in (6, 11, 16):
        tr = []
        for sd in SEEDS:
            g = gen_maze(m, 0.0, sd); d = bfs(g, (1,1)); tgt = max(d, key=d.get)
            tr.append([x/d[tgt] for x in lrta_star(g, (1,1), tgt, 10)] + [online_dfs(g, (1,1), tgt)["moves"]/d[tgt]])
        D.append(dict(grid=2*m+1, ratio_per_trial=[round(st.mean(t[i] for t in tr), 2) for i in range(10)], dfs_ratio=round(st.mean(t[10] for t in tr), 2)))
    out["lrta"] = D
    # ---- Fleet / repeated missions (21x21 perfect maze, farthest target): total moves for K missions
    g_rows = []
    for sd in SEEDS:
        g = gen_maze(10, 0.0, sd); d = bfs(g, (1,1)); tgt = max(d, key=d.get)
        dfs_m = online_dfs(g, (1,1), tgt)["moves"]; lr = lrta_star(g, (1,1), tgt, 100); g_rows.append((d[tgt], dfs_m, lr))
    fleet = []
    for K in (1, 5, 20, 100):
        opt = st.mean(r[0] for r in g_rows)
        fleet.append(dict(K=K, online_dfs_every_mission=mean([K*r[1] for r in g_rows]),
                          explore_once_then_plan=mean([r[1]+(K-1)*r[0] for r in g_rows]),
                          lrta_learning=mean([sum(r[2][:K]) for r in g_rows]), always_optimal_if_mapped=round(K*opt, 2)))
    out["fleet"] = fleet
    # ---- Exp E: long-horizon LRTA* convergence (23x23 perfect mazes)
    E = {t: [] for t in (1, 10, 25, 50, 100, 200)}
    for sd in SEEDS:
        g = gen_maze(10, 0.0, sd); d = bfs(g, (1,1)); tgt = max(d, key=d.get); lr = lrta_star(g, (1,1), tgt, 200)
        for t in E: E[t].append(lr[t-1]/d[tgt])
    out["lrta_convergence"] = {t: round(st.mean(v), 2) for t, v in E.items()}
    json.dump(out, open("results/task2.json", "w"), indent=1)
    for k, v in out.items(): print("==", k); print(json.dumps(v, indent=0)[:1800])
