"""Task 6 - Exhaustive tour enumeration vs 2-opt local search (courier with n customers + depot 0)."""
import random, math, time, json, itertools, statistics as st, sys
sys.setrecursionlimit(10000)

def make_instance(n, seed):
    rnd = random.Random(seed); pts = [(rnd.uniform(0, 100), rnd.uniform(0, 100)) for _ in range(n+1)]
    return pts, [[math.dist(a, b) for b in pts] for a in pts]

def tour_cost(D, tour):                    # tour = [0, c1, ..., cn]  (return to depot implied)
    return sum(D[tour[i]][tour[(i+1) % len(tour)]] for i in range(len(tour)))

def exhaustive(D):
    """Tour = permutation of customers 1..n with depot fixed at 0 (fixing the start removes the n+... rotations).
    Generation: depth-first, choose the next unvisited customer. Evaluation: running distance, closed with the return leg at the leaf.
    Retention: keep the cheapest complete tour seen. No pruning -> every one of n! tours is evaluated."""
    n = len(D)-1; best = [float("inf"), None]; cnt = {"tours": 0, "nodes": 0}
    path = [0]; used = [False]*(n+1)
    def rec(cur, cost):
        if len(path) == n+1:
            cnt["tours"] += 1; total = cost + D[cur][0]
            if total < best[0]: best[0] = total; best[1] = list(path)
            return
        for c in range(1, n+1):
            if not used[c]:
                used[c] = True; path.append(c); cnt["nodes"] += 1
                rec(c, cost + D[cur][c])
                path.pop(); used[c] = False
    rec(0, 0.0)
    return best[0], best[1], cnt

def two_opt_once(D, rnd):
    n = len(D)-1; tour = [0] + rnd.sample(range(1, n+1), n)
    improved = True; moves = 0
    while improved:
        improved = False
        for i in range(1, n):
            for j in range(i+1, n+1):
                a, b = tour[i-1], tour[i]; c, d = tour[j], tour[(j+1) % (n+1)]
                if D[a][c] + D[b][d] < D[a][b] + D[c][d] - 1e-12:      # reversing segment i..j shortens the tour
                    tour[i:j+1] = reversed(tour[i:j+1]); improved = True; moves += 1
    return tour_cost(D, tour), tour

def local_search(D, restarts, seed):
    rnd = random.Random(seed); best = (float("inf"), None)
    for _ in range(restarts):
        r = two_opt_once(D, rnd)
        if r[0] < best[0]: best = r
    return best

if __name__ == "__main__":
    out = {}
    # ---------- correctness 1: regular octagon (depot + 7 customers, indices shuffled) -> optimum = perimeter, known analytically
    R = 10.0; pts = [(R*math.cos(2*math.pi*k/8), R*math.sin(2*math.pi*k/8)) for k in range(8)]
    random.Random(3).shuffle(pts); D = [[math.dist(a, b) for b in pts] for a in pts]
    c, t, cnt = exhaustive(D); analytic = 8*2*R*math.sin(math.pi/8)
    out["octagon"] = dict(found=round(c, 6), analytic=round(analytic, 6), match=abs(c-analytic) < 1e-9, tours=cnt["tours"])
    # ---------- correctness 2: random 7-customer instances vs independent itertools.permutations brute force
    ok = []
    for sd in range(5):
        pts, D = make_instance(7, 100+sd); c1, _, _ = exhaustive(D)
        c2 = min(tour_cost(D, (0,)+p) for p in itertools.permutations(range(1, 8)))
        ok.append(abs(c1-c2) < 1e-9)
    out["independent_check_all_match"] = all(ok)
    # ---------- hand-verifiable 4-customer instance (integer distances)
    D4 = [[0,2,9,10,7],[2,0,6,4,3],[9,6,0,8,5],[10,4,8,0,6],[7,3,5,6,0]]
    c, t, cnt = exhaustive(D4); out["hand_instance"] = dict(optimum=c, tour=t, tours=cnt["tours"])
    # ---------- growth: tours and nodes vs n, plus time
    growth = []
    for n in (4, 5, 6, 7, 8, 9, 10):
        pts, D = make_instance(n, 1); t0 = time.perf_counter(); c, t, cnt = exhaustive(D); dt = time.perf_counter()-t0
        growth.append(dict(n=n, tours=cnt["tours"], factorial=math.factorial(n), nodes=cnt["nodes"], time_s=round(dt, 3), best=round(c, 3))); print(growth[-1], flush=True)
    out["growth"] = growth
    # ---------- local search quality (>=20 runs per size)
    LS = []
    for n, ninst in ((7, 20), (8, 20), (9, 20)):
        g1 = []; g10 = []; t1 = []; t10 = []; hit1 = hit10 = 0
        for sd in range(ninst):
            pts, D = make_instance(n, 1000+sd); opt, _, _ = exhaustive(D)
            t0 = time.perf_counter(); c1, _ = local_search(D, 1, sd); t1.append(time.perf_counter()-t0)
            t0 = time.perf_counter(); c10, _ = local_search(D, 10, sd); t10.append(time.perf_counter()-t0)
            g1.append(100*(c1-opt)/opt); g10.append(100*(c10-opt)/opt); hit1 += (c1-opt) < 1e-9; hit10 += (c10-opt) < 1e-9
        LS.append(dict(n=n, runs=ninst, single_mean_gap=round(st.mean(g1), 2), single_max_gap=round(max(g1), 2), single_opt_found=hit1, single_time_ms=round(1000*st.mean(t1), 2),
                       restart10_mean_gap=round(st.mean(g10), 2), restart10_max_gap=round(max(g10), 2), restart10_opt_found=hit10, restart10_time_ms=round(1000*st.mean(t10), 2)))
        print(LS[-1], flush=True)
    # n = 10: one instance, optimum by exhaustive search, 20 independent LS runs
    pts, D = make_instance(10, 2024); opt, _, _ = exhaustive(D); g1 = []; g10 = []; t1 = []; t10 = []
    for sd in range(20):
        t0 = time.perf_counter(); c1, _ = local_search(D, 1, sd); t1.append(time.perf_counter()-t0)
        t0 = time.perf_counter(); c10, _ = local_search(D, 10, sd); t10.append(time.perf_counter()-t0)
        g1.append(100*(c1-opt)/opt); g10.append(100*(c10-opt)/opt)
    LS.append(dict(n=10, runs=20, single_mean_gap=round(st.mean(g1), 2), single_max_gap=round(max(g1), 2), single_opt_found=sum(g < 1e-9 for g in g1), single_time_ms=round(1000*st.mean(t1), 2),
                   restart10_mean_gap=round(st.mean(g10), 2), restart10_max_gap=round(max(g10), 2), restart10_opt_found=sum(g < 1e-9 for g in g10), restart10_time_ms=round(1000*st.mean(t10), 2)))
    print(LS[-1], flush=True)
    out["local_search"] = LS
    # ---------- local search beyond exhaustive range
    big = []
    for n in (15, 20, 50, 100):
        pts, D = make_instance(n, 5); t0 = time.perf_counter(); c1, _ = local_search(D, 1, 0); t1 = time.perf_counter()-t0
        t0 = time.perf_counter(); c10, _ = local_search(D, 10, 0); t10 = time.perf_counter()-t0
        big.append(dict(n=n, single_cost=round(c1, 1), single_time_s=round(t1, 3), restart10_cost=round(c10, 1), restart10_time_s=round(t10, 3)))
        print(big[-1], flush=True)
    out["local_search_large"] = big
    json.dump(out, open("results/task6.json", "w"), indent=1)
    print({k: v for k, v in out.items() if k in ("octagon", "independent_check_all_match", "hand_instance")})
