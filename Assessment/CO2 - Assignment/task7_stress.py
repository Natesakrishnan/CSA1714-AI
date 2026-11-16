"""Task 7F evidence: does the redesign still help when the lower bound is weak? (customers in near-coincident pairs)"""
import random, math, json, time, statistics as st
from task6 import make_instance
from task7 import branch_bound

def paired_instance(n, seed):
    rnd = random.Random(seed); pts = [(rnd.uniform(0, 100), rnd.uniform(0, 100))]
    while len(pts) < n+1:
        x, y = rnd.uniform(0, 100), rnd.uniform(0, 100); pts.append((x, y))
        if len(pts) < n+1: pts.append((x+rnd.uniform(-0.2, 0.2), y+rnd.uniform(-0.2, 0.2)))   # twin customer 0.1-0.3 away
    return pts, [[math.dist(a, b) for b in pts] for a in pts]

out = []
for n in (10, 12, 14):
    for kind, mk in (("uniform random", make_instance), ("paired customers", paired_instance)):
        rows = []
        for sd in range(5):
            pts, D = mk(n, 5000+sd); t0 = time.perf_counter(); c, t, k = branch_bound(D); rows.append((k["nodes"], time.perf_counter()-t0))
        out.append(dict(n=n, kind=kind, nodes_mean=round(st.mean(r[0] for r in rows)), nodes_max=max(r[0] for r in rows), time_s_mean=round(st.mean(r[1] for r in rows), 3), orig_nodes=sum(math.factorial(n)//math.factorial(n-k) for k in range(1, n+1))))
        print(out[-1], flush=True)
json.dump(out, open("results/task7_stress.json", "w"), indent=1)
