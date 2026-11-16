"""Task 7 - Redesign of the Task-6 exhaustive tour search.
Diagnosis: every one of the n! tours is generated although almost all partial tours are already longer than a known tour.
Redesign (branch & bound built from the diagnosis, not from a textbook recipe):
  R1 prefix-cost pruning : abandon a partial tour as soon as its length >= best known tour (the rest of the tour can only add cost)
  R2 reuse of earlier work: initial best-known tour comes from the Task-6 2-opt local search (cheap, usually optimal) -> pruning is effective from node 1
  R3 candidate ordering   : try nearest unvisited customer first so that good tours are found early (move-ordering idea of Task 3)
  R4 optimistic completion bound: every remaining leg leaves a distinct node; each such leg costs >= that node's cheapest outgoing edge,
                            so  cost_so_far + minout[cur] + sum(minout[c] for unvisited c)  is a lower bound on any completion."""
import time, json, sys, math, statistics as st
sys.setrecursionlimit(10000)
from task6 import make_instance, exhaustive, local_search, tour_cost

def branch_bound(D, use_order=True, use_ub=True, use_lb=True, ub_restarts=5):
    n = len(D)-1; N = n+1
    minout = [min(D[i][j] for j in range(N) if j != i) for i in range(N)]
    cnt = {"nodes": 0, "tours": 0, "pruned": 0}
    if use_ub: ub, tour = local_search(D, ub_restarts, 0)
    else: ub, tour = float("inf"), None
    best = [ub, tour]
    cand = [sorted((j for j in range(1, N) if j != i), key=lambda j: D[i][j]) if use_order else [j for j in range(1, N) if j != i] for i in range(N)]
    used = [False]*N; path = [0]; rem_min = [sum(minout[1:])]
    def rec(cur, cost, rem_sum):
        if len(path) == N:
            cnt["tours"] += 1; total = cost + D[cur][0]
            if total < best[0] - 1e-12: best[0] = total; best[1] = list(path)
            return
        for c in cand[cur]:
            if used[c]: continue
            cnt["nodes"] += 1; c2 = cost + D[cur][c]
            # R4: any completion from c needs |unvisited|+1 legs leaving c and each unvisited customer: cost >= minout[c] + sum(minout[unvisited after c]) = rem_sum
            if c2 >= best[0] - 1e-12 or (use_lb and c2 + rem_sum >= best[0] - 1e-12):
                cnt["pruned"] += 1; continue
            used[c] = True; path.append(c)
            rec(c, c2, rem_sum - minout[c])
            path.pop(); used[c] = False
    rec(0, 0.0, sum(minout[1:]))
    return best[0], best[1], cnt

if __name__ == "__main__":
    out = {}
    # ---- Validation + ablation on the SAME instances as the original (n = 8, 9, 10; 5 instances each)
    abl = []
    for n in (8, 9, 10):
        rows = []
        for sd in range(5):
            pts, D = make_instance(n, 3000+sd)
            t0 = time.perf_counter(); c0, t0_, k0 = exhaustive(D); tm0 = time.perf_counter()-t0
            r = {"orig": (c0, k0["nodes"], k0["tours"], tm0)}
            for name, kw in (("R1_prefix_only", dict(use_order=False, use_ub=False, use_lb=False)),
                             ("R1+R2+R3", dict(use_order=True, use_ub=True, use_lb=False)),
                             ("R1+R2+R3+R4", dict(use_order=True, use_ub=True, use_lb=True))):
                t0 = time.perf_counter(); c, t, k = branch_bound(D, **kw); tm = time.perf_counter()-t0
                assert abs(c-c0) < 1e-9, (name, c, c0)                       # identical optimum
                r[name] = (c, k["nodes"], k["tours"], tm)
            rows.append(r)
        entry = dict(n=n)
        for name in rows[0]:
            entry[name] = dict(nodes=round(st.mean(r[name][1] for r in rows)), tours=round(st.mean(r[name][2] for r in rows)), time_ms=round(1000*st.mean(r[name][3] for r in rows), 1))
        abl.append(entry); print(entry, flush=True)
    out["ablation"] = abl
    # ---- Scaling of the final design beyond the original's reach (5 random instances per n)
    sc = []
    for n in (10, 11, 12, 13, 14, 15, 16):
        rows = []
        for sd in range(5):
            pts, D = make_instance(n, 4000+sd); t0 = time.perf_counter(); c, t, k = branch_bound(D); rows.append((k["nodes"], k["tours"], time.perf_counter()-t0))
        sc.append(dict(n=n, nodes_mean=round(st.mean(r[0] for r in rows)), nodes_max=max(r[0] for r in rows), time_s_mean=round(st.mean(r[2] for r in rows), 3),
                       time_s_max=round(max(r[2] for r in rows), 3), orig_nodes=sum(math.factorial(n)//math.factorial(n-k) for k in range(1, n+1))))
        print(sc[-1], flush=True)
    out["scaling"] = sc
    json.dump(out, open("results/task7.json", "w"), indent=1)
