"""Task 5 - Constraint propagation (arc consistency, derived from the 'unsupported value' principle) + backtracking for exam timetabling."""
import random, json, time, copy, statistics as st
from collections import deque
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

class CSP:
    """variables: list of exams; dom: var -> set of slots; conflicts: set of frozenset({x,y}) (shared students).
    Constraint representation: for every conflicting pair the two directed arcs (x,y),(y,x) with compat(a,b) := (a != b)."""
    def __init__(self, variables, dom, conflicts):
        self.vars = list(variables); self.dom = {v: set(dom[v]) for v in variables}
        self.nbrs = {v: [] for v in variables}
        for x, y in sorted(tuple(sorted(e)) for e in conflicts):      # sorted => deterministic neighbour order (no hash-seed effects)
            self.nbrs[x].append(y); self.nbrs[y].append(x)
    def compat(self, a, b): return a != b

def new_counters(): return dict(checks=0, nodes=0, tries=0, backtracks=0, wipeouts=0, revisions=0, removals=0)

def revise(csp, D, xi, xj, cnt):
    """Remove every value a of xi that has NO supporting value b in D[xj]. Returns True if D[xi] changed."""
    cnt["revisions"] += 1; changed = False
    for a in list(D[xi]):
        support = False
        for b in D[xj]:
            cnt["checks"] += 1
            if csp.compat(a, b): support = True; break
        if not support: D[xi].discard(a); changed = True; cnt["removals"] += 1
    return changed

def ac3(csp, D, cnt, arcs=None, trace=None):
    """Arc-consistency propagation. Returns False when a domain wipe-out occurs (=> no solution below this state)."""
    q = deque(arcs if arcs is not None else [(x, y) for x in csp.vars for y in csp.nbrs[x]])
    inq = set(q)
    while q:
        xi, xj = q.popleft(); inq.discard((xi, xj))
        if revise(csp, D, xi, xj, cnt):
            if trace is not None: trace.append({v: sorted(D[v]) for v in csp.vars})
            if not D[xi]: cnt["wipeouts"] += 1; return False
            for xk in csp.nbrs[xi]:                    # xi lost values => every neighbour's support in xi must be re-checked
                if xk != xj and (xk, xi) not in inq: q.append((xk, xi)); inq.add((xk, xi))
    return True

def solve(csp, use_prop, node_cap=2_000_000, order="static"):
    """Backtracking. use_prop=False: plain BT (check against assigned neighbours). True: AC-3 at the root + after every assignment (MAC)."""
    cnt = new_counters(); D0 = {v: set(csp.dom[v]) for v in csp.vars}
    if use_prop and not ac3(csp, D0, cnt): return None, cnt, "failed_by_propagation"
    sol = {}
    def rec(D, assigned):
        cnt["nodes"] += 1
        if cnt["nodes"] > node_cap: raise TimeoutError
        if len(assigned) == len(csp.vars): return dict(assigned)
        v = next(x for x in csp.vars if x not in assigned)
        for a in sorted(D[v]):
            cnt["tries"] += 1
            if use_prop:
                D2 = {x: set(s) for x, s in D.items()}; D2[v] = {a}
                if ac3(csp, D2, cnt, arcs=[(xk, v) for xk in csp.nbrs[v]]):
                    assigned[v] = a; r = rec(D2, assigned)
                    if r: return r
                    del assigned[v]
                cnt["backtracks"] += 1
            else:
                ok = True
                for xk in csp.nbrs[v]:
                    if xk in assigned:
                        cnt["checks"] += 1
                        if not csp.compat(a, assigned[xk]): ok = False; break
                if ok:
                    assigned[v] = a; r = rec(D, assigned)
                    if r: return r
                    del assigned[v]
                cnt["backtracks"] += 1
        return None
    try: r = rec(D0, {})
    except TimeoutError: return None, cnt, "node_cap"
    return r, cnt, ("solved" if r else "unsat")

def valid(csp, sol):
    return sol is not None and all(sol[x] != sol[y] for x in csp.vars for y in csp.nbrs[x]) and all(sol[v] in csp.dom[v] for v in csp.vars)

# ------------------------------------------------------------------ instances
def chain(n, slots, anchors):
    V = [f"E{i}" for i in range(1, n+1)]; dom = {v: set(slots) for v in V}
    for k, s in anchors.items(): dom[f"E{k}"] = set(s)
    return CSP(V, dom, {frozenset((V[i], V[i+1])) for i in range(n-1)})

def clique(n, k):
    V = [f"E{i}" for i in range(1, n+1)]
    return CSP(V, {v: set(range(1, k+1)) for v in V}, {frozenset((V[i], V[j])) for i in range(n) for j in range(i+1, n)})

def random_exams(n, avg_deg, k, seed):
    rnd = random.Random(seed); V = [f"E{i}" for i in range(1, n+1)]; p = avg_deg/(n-1)
    return CSP(V, {v: set(range(1, k+1)) for v in V}, {frozenset((V[i], V[j])) for i in range(n) for j in range(i+1, n) if rnd.random() < p})

def heat(ax, csp, snap, slots, title):
    M = [[1 if s in snap[v] else 0 for s in slots] for v in csp.vars]
    ax.imshow(M, cmap="Greys", vmin=0, vmax=1.4, aspect="auto"); ax.set_title(title, fontsize=9)
    ax.set_xticks(range(len(slots))); ax.set_xticklabels(slots); ax.set_yticks(range(len(csp.vars))); ax.set_yticklabels(csp.vars, fontsize=7); ax.set_xlabel("slot")

if __name__ == "__main__":
    import sys
    out = {}
    # ---- Instance A: chain of 10 exams, 2 slots, E1 anchored -> propagation alone solves it
    A = chain(10, (1, 2), {1: (1,)}); tr = []; D = {v: set(A.dom[v]) for v in A.vars}; c = new_counters(); ok = ac3(A, D, c, trace=tr)
    out["A_chain_solved_by_AC3"] = dict(consistent=ok, domains={v: sorted(D[v]) for v in A.vars}, counters=c, all_singletons=all(len(D[v]) == 1 for v in A.vars), valid=valid(A, {v: min(D[v]) for v in A.vars}))
    A2 = chain(10, (1, 2), {1: (1,), 10: (1,)}); c2 = new_counters(); D2 = {v: set(A2.dom[v]) for v in A2.vars}; ok2 = ac3(A2, D2, c2)
    out["A2_chain_failure_detected"] = dict(consistent=ok2, counters=c2)
    # ---- Instance B: K6 with 5 slots (pigeonhole) - AC-3 cannot see the contradiction, search is needed
    B = clique(6, 5); cB = new_counters(); DB = {v: set(B.dom[v]) for v in B.vars}; okB = ac3(B, DB, cB)
    rB = {}
    for name, prop in (("plain_BT", False), ("MAC", True)):
        sol, cnt, status = solve(B, prop); rB[name] = dict(status=status, **cnt)
    out["B_K6_5slots"] = dict(ac3_alone_consistent=okB, ac3_removals=cB["removals"], **rB)
    # ---- Figure: domain shrinkage for A and for a mid-size instance
    fig, axs = plt.subplots(1, 4, figsize=(13, 3.8))
    slots = (1, 2); full = {v: [1, 2] for v in A.vars}
    heat(axs[0], A, {**full, "E1": [1]}, slots, "A: initial domains\n(E1 anchored to slot 1)")
    mid = tr[len(tr)//3]; heat(axs[1], A, mid, slots, f"after {len(tr)//3+1} removals")
    mid2 = tr[2*len(tr)//3]; heat(axs[2], A, mid2, slots, f"after {2*len(tr)//3+1} removals")
    heat(axs[3], A, tr[-1], slots, f"AC-3 fixpoint ({len(tr)} removals)\nall domains singleton")
    plt.tight_layout(); plt.savefig("results/fig_task5_domains.png", dpi=130); plt.close()
    # ---- Growth experiment 1: random timetables (avg conflict degree 7, 5 slots), 20 seeds per size, MEDIAN reported
    G = []
    for n in (10, 20, 30, 40, 50):
        rows = {"plain_BT": [], "MAC": []}; res = {"plain_BT": [], "MAC": []}
        for sd in range(20):
            csp = random_exams(n, 7.0, 5, sd)
            for name, prop in (("plain_BT", False), ("MAC", True)):
                sol, cnt, status = solve(csp, prop, node_cap=200_000)
                if status == "solved": assert valid(csp, sol)
                rows[name].append(cnt); res[name].append(status)
        entry = dict(n=n)
        for name in rows:
            entry[name] = {k: round(st.median(r[k] for r in rows[name]), 1) for k in ("nodes", "tries", "backtracks", "checks", "wipeouts")}
            entry[name]["capped"] = res[name].count("node_cap"); entry[name]["unsat"] = res[name].count("unsat"); entry[name]["solved"] = res[name].count("solved")
        G.append(entry); print(entry, flush=True)
    out["growth"] = G
    # ---- Growth experiment 2: pigeonhole family K_n with n-1 slots (always unsatisfiable, deterministic)
    K = []
    for n in range(4, 10):
        csp = clique(n, n-1); e = dict(n=n)
        for name, prop in (("plain_BT", False), ("MAC", True)):
            sol, cnt, status = solve(csp, prop); e[name] = dict(status=status, **cnt)
        K.append(e); print(e, flush=True)
    out["clique_growth"] = K
    json.dump(out, open("results/task5.json", "w"), indent=1)
    # growth plot
    plt.figure(figsize=(6.2, 4)); ns = [g["n"] for g in G]
    ks = [k["n"] for k in K]
    plt.semilogy(ks, [k["plain_BT"]["nodes"] for k in K], "o-", label="plain BT (nodes)"); plt.semilogy(ks, [max(k["MAC"]["nodes"], 1) for k in K], "s-", label="BT + AC-3 (nodes)")
    plt.semilogy(ks, [k["plain_BT"]["checks"] for k in K], "o--", label="plain BT (checks)"); plt.semilogy(ks, [k["MAC"]["checks"] for k in K], "s--", label="BT + AC-3 (checks)")
    plt.xlabel("Number of exams n (K_n conflict graph, n-1 slots)"); plt.ylabel("Work (log scale)"); plt.grid(alpha=.3); plt.legend(); plt.tight_layout(); plt.savefig("results/fig_task5_growth.png", dpi=130)
    print(json.dumps({k: v for k, v in out.items() if k != "growth"}, indent=1))
