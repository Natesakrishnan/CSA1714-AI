"""Task 1 - UCS vs Greedy Best-First vs A* on grid maps (campus shuttle)."""
import heapq, random, time, json
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap

OBST = -1  # cell value: -1 obstacle, otherwise cost of entering the cell

def h_manhattan(a, b):
    # Admissible: exact cost in the RELAXED problem (obstacles removed, every step costs the minimum, 1)
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def search(grid, start, goal, mode):
    n = len(grid); t0 = time.perf_counter()
    cnt = 0; heap = []
    def pri(g, h):
        return {"ucs": (g,), "greedy": (h,), "astar": (g+h, -g)}[mode]  # A* tie-break: deeper node first
    h0 = h_manhattan(start, goal)
    heapq.heappush(heap, (pri(0, h0), cnt, start)); best_g = {start: 0}; parent = {start: None}
    closed = set(); expanded = 0; generated = 1; maxfront = 1; order = []
    while heap:
        _, _, s = heapq.heappop(heap)
        if s in closed: continue
        closed.add(s); expanded += 1; order.append(s)
        if s == goal: break
        for dr, dc in ((1,0),(-1,0),(0,1),(0,-1)):
            r, c = s[0]+dr, s[1]+dc
            if 0 <= r < n and 0 <= c < n and grid[r][c] != OBST and (r, c) not in closed:
                g2 = best_g[s] + grid[r][c]; t = (r, c)
                if mode == "greedy":
                    if t in best_g: continue           # greedy: first discovery only
                elif t in best_g and best_g[t] <= g2: continue
                best_g[t] = g2; parent[t] = s; cnt += 1; generated += 1
                heapq.heappush(heap, (pri(g2, h_manhattan(t, goal)), cnt, t))
        maxfront = max(maxfront, len(best_g) - len(closed))
    found = goal in closed
    path = []
    if found:
        s = goal
        while s is not None: path.append(s); s = parent[s]
        path.reverse()
    cost = sum(grid[r][c] for r, c in path[1:]) if found else None
    return dict(found=found, expanded=expanded, generated=generated, max_frontier=maxfront, cost=cost,
                time_ms=round((time.perf_counter()-t0)*1000, 2), path=path, order=order)

def map_open(n, seed, obst=0.08, cong=0.10):
    rnd = random.Random(seed); g = [[1]*n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            x = rnd.random()
            if x < obst: g[r][c] = OBST
            elif x < obst+cong: g[r][c] = 4        # congested road, cost 4
    g[0][0] = 1; g[n-1][n-1] = 1
    return g, (0, 0), (n-1, n-1)

def map_trap(n):
    g = [[1]*n for _ in range(n)]
    top, bot, left, right = n//4, 3*n//4, int(0.4*n), int(0.67*n)
    for r in range(top, bot+1): g[r][right] = OBST          # back wall of the cup (faces the goal side)
    for c in range(left, right+1): g[top][c] = OBST; g[bot][c] = OBST  # arms -> cup opens toward the start
    return g, (n//2, 2), (n//2, n-3)

def map_unreach(n):
    g, s, t = map_open(n, 7, obst=0.05, cong=0.0)
    g[n-2][n-1] = OBST; g[n-1][n-2] = OBST                    # goal fully enclosed
    return g, s, t

def run_all(grid, s, t):
    res = {m: search(grid, s, t, m) for m in ("ucs", "greedy", "astar")}
    opt = res["ucs"]["cost"]
    for m in res: res[m]["optimal"] = (res[m]["cost"] == opt) if res[m]["found"] else None
    return res

def draw(grid, s, t, res, fname):
    fig, axs = plt.subplots(1, 3, figsize=(13, 4.4))
    for ax, m, name in zip(axs, ("ucs", "greedy", "astar"), ("Uniform-Cost", "Greedy Best-First", "A*")):
        n = len(grid); img = [[0]*n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                if grid[r][c] == OBST: img[r][c] = 1
        for (r, c) in res[m]["order"]: img[r][c] = 2
        for (r, c) in res[m]["path"]: img[r][c] = 3
        img[s[0]][s[1]] = 4; img[t[0]][t[1]] = 5
        ax.imshow(img, cmap=ListedColormap(["white", "black", "#a6cee3", "#e31a1c", "green", "blue"]), vmin=0, vmax=5)
        ax.set_title(f"{name}\nexpanded={res[m]['expanded']}, cost={res[m]['cost']}", fontsize=10); ax.axis("off")
    plt.tight_layout(); fig.subplots_adjust(top=0.84); plt.savefig(fname, dpi=130); plt.close()

if __name__ == "__main__":
    out = {"open": [], "trap": [], "unreach": []}
    for n in (20, 30, 40):
        # open map: 5 random layouts per size
        seeds = []; sd = 0
        while len(seeds) < 5:                       # keep only layouts where a path exists
            g, s, t = map_open(n, sd)
            if search(g, s, t, "ucs")["found"]: seeds.append(sd)
            sd += 1
        for seed in seeds:
            g, s, t = map_open(n, seed); r = run_all(g, s, t)
            out["open"].append(dict(n=n, seed=seed, **{m: {k: v for k, v in r[m].items() if k not in ("path", "order")} for m in r}))
        g, s, t = map_trap(n); r = run_all(g, s, t)
        out["trap"].append(dict(n=n, **{m: {k: v for k, v in r[m].items() if k not in ("path", "order")} for m in r}))
        if n == 30: draw(g, s, t, r, "results/fig_task1_trap.png")
        g, s, t = map_unreach(n); r = run_all(g, s, t)
        out["unreach"].append(dict(n=n, **{m: {k: v for k, v in r[m].items() if k not in ("path", "order")} for m in r}))
        if n == 30: draw(g, s, t, r, "results/fig_task1_unreach.png")
        if n == 30:
            g, s, t = map_open(30, 0); r = run_all(g, s, t); draw(g, s, t, r, "results/fig_task1_open.png")
    json.dump(out, open("results/task1.json", "w"), indent=1)
    for k in out:
        print("==", k)
        for row in out[k]:
            tag = f"n={row['n']}" + (f" seed={row['seed']}" if 'seed' in row else "")
            print(tag, {m: (row[m]['expanded'], row[m]['generated'], row[m]['max_frontier'], row[m]['cost'], row[m]['optimal']) for m in ("ucs", "greedy", "astar")})
