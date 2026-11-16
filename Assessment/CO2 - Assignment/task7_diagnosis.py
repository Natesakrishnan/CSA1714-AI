"""Task 7A evidence: where does the exhaustive search of Task 6 spend its effort?  (re-runs the Task-6 enumeration with extra bookkeeping)"""
import json, math, sys, statistics as st
sys.setrecursionlimit(10000)
from task6 import make_instance

def profile(D):
    n = len(D)-1; levels = [0]*(n+1); opt = [float("inf")]
    # pass 1: optimum (plain enumeration)
    path = [0]; used = [False]*(n+1)
    def rec1(cur, cost):
        if len(path) == n+1: opt[0] = min(opt[0], cost + D[cur][0]); return
        for c in range(1, n+1):
            if not used[c]: used[c] = True; path.append(c); rec1(c, cost + D[cur][c]); path.pop(); used[c] = False
    rec1(0, 0.0)
    # pass 2: count nodes per level, nodes whose prefix already >= optimum, and enumeration index of the first time the optimum is reached
    wasted = [0]; seen = [0]; first = [None]; tours = [0]
    def rec2(cur, cost):
        if len(path) == n+1:
            tours[0] += 1
            if first[0] is None and cost + D[cur][0] <= opt[0] + 1e-12: first[0] = tours[0]
            return
        for c in range(1, n+1):
            if not used[c]:
                used[c] = True; path.append(c); levels[len(path)-1] += 1; seen[0] += 1
                if cost + D[cur][c] >= opt[0] - 1e-12: wasted[0] += 1
                rec2(c, cost + D[cur][c]); path.pop(); used[c] = False
    rec2(0, 0.0)
    return dict(levels=levels[1:], nodes=seen[0], wasted=wasted[0], first_opt_index=first[0], tours=tours[0])

if __name__ == "__main__":
    out = []
    for n, k in ((7, 10), (8, 10), (9, 5), (10, 1)):
        rows = [profile(make_instance(n, 3000+sd)[1]) for sd in range(k)]
        e = dict(n=n, instances=k, nodes=rows[0]["nodes"], last_two_levels_share=round(100*(rows[0]["levels"][-1]+rows[0]["levels"][-2])/rows[0]["nodes"], 1),
                 wasted_share_mean=round(100*st.mean(r["wasted"]/r["nodes"] for r in rows), 1), wasted_share_min=round(100*min(r["wasted"]/r["nodes"] for r in rows), 1),
                 first_opt_fraction_mean=round(100*st.mean(r["first_opt_index"]/r["tours"] for r in rows), 1), first_opt_fraction_max=round(100*max(r["first_opt_index"]/r["tours"] for r in rows), 1),
                 tours_after_opt_found_pct=round(100*(1-st.mean(r["first_opt_index"]/r["tours"] for r in rows)), 1))
        out.append(e); print(e, flush=True)
    json.dump(out, open("results/task7_diagnosis.json", "w"), indent=1)
