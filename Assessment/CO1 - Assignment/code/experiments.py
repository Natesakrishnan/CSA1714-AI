"""
Experimental performance collection – Assignment 1 CSA17
Produces tables (CSV) and PNG figures saved to ../outputs/ and ../figures/
"""

import sys, os, csv, time, random
from collections import deque
sys.path.insert(0, os.path.dirname(__file__))
from hospital_search import generate_hospital_graph, bfs, ucs, iddfs, timed_run

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

OUT = os.path.join(os.path.dirname(__file__), "..", "outputs")
FIG = os.path.join(os.path.dirname(__file__), "..", "figures")
os.makedirs(OUT, exist_ok=True)
os.makedirs(FIG, exist_ok=True)

SIZES = [1_000, 10_000, 100_000, 1_000_000]
SEED  = 42
ALGOS = [("BFS", bfs), ("UCS", ucs), ("IDDFS", iddfs)]

# -------------------------------------------------------
# Helpers
# -------------------------------------------------------
def pick_start_goal(adj, rng):
    """Pick a start/goal that are definitely connected (BFS reachable)."""
    keys = list(adj.keys())
    for _ in range(200):
        s = rng.choice(keys[:100])
        g = rng.choice(keys[-100:])
        if s != g:
            return s, g
    return keys[0], keys[-1]


# -------------------------------------------------------
# Main experiment loop
# -------------------------------------------------------
rows = []
print(f"{'Size':>10}  {'Algo':>7}  {'Gen':>10}  {'Exp':>10}  "
      f"{'MaxFront':>10}  {'Depth':>6}  {'Cost':>8}  {'Time_ms':>9}  {'Optimal':>8}")

for n in SIZES:
    rng = random.Random(SEED)
    adj = generate_hospital_graph(n, seed=SEED)
    start, goal = pick_start_goal(adj, rng)

    # skip IDDFS on very large graphs to avoid stack / time issues
    skip_iddfs = (n >= 1_000_000)

    for aname, afunc in ALGOS:
        if skip_iddfs and aname == "IDDFS":
            rows.append({
                "size": n, "algo": aname,
                "nodes_gen": "N/A", "nodes_exp": "N/A",
                "max_frontier": "N/A", "depth": "N/A",
                "cost": "N/A", "time_ms": "N/A", "optimal": "N/A"
            })
            print(f"{n:>10}  {aname:>7}  {'N/A':>10}  {'N/A':>10}  "
                  f"{'N/A':>10}  {'N/A':>6}  {'N/A':>8}  {'N/A':>9}  {'N/A':>8}")
            continue

        # set recursion limit for IDDFS
        if aname == "IDDFS":
            old_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(max(old_limit, 10_000))

        avg_ms, res = timed_run(afunc, adj, start, goal)

        if aname == "IDDFS":
            sys.setrecursionlimit(old_limit)

        if res["found"]:
            # Is the solution optimal (matches UCS cost)?
            ucs_res = ucs(adj, start, goal)
            is_opt = (ucs_res["path_cost"] == res["path_cost"])
        else:
            is_opt = "N/A"

        row = {
            "size": n, "algo": aname,
            "nodes_gen"   : res["nodes_gen"],
            "nodes_exp"   : res["nodes_exp"],
            "max_frontier": res["max_frontier"],
            "depth"       : res["depth"] if res["found"] else "N/A",
            "cost"        : round(res["path_cost"], 2) if res["found"] else "N/A",
            "time_ms"     : round(avg_ms, 3),
            "optimal"     : is_opt
        }
        rows.append(row)
        print(f"{n:>10}  {aname:>7}  {row['nodes_gen']:>10}  "
              f"{row['nodes_exp']:>10}  {row['max_frontier']:>10}  "
              f"{row['depth']:>6}  {row['cost']:>8}  "
              f"{row['time_ms']:>9}  {str(row['optimal']):>8}")

# -------------------------------------------------------
# Save CSV
# -------------------------------------------------------
csv_path = os.path.join(OUT, "experiment_results.csv")
fieldnames = ["size","algo","nodes_gen","nodes_exp","max_frontier",
              "depth","cost","time_ms","optimal"]
with open(csv_path, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=fieldnames)
    w.writeheader()
    w.writerows(rows)
print(f"\nResults saved → {csv_path}")

# -------------------------------------------------------
# Figures
# -------------------------------------------------------
def numeric_rows(algo):
    return [(int(r["size"]), r) for r in rows
            if r["algo"] == algo and r["nodes_gen"] != "N/A"]

algo_colors = {"BFS": "#1f77b4", "UCS": "#ff7f0e", "IDDFS": "#2ca02c"}

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle("Search Algorithm Performance – Hospital Robot", fontsize=13,
             fontweight="bold")

metrics = [
    ("nodes_gen",    "Nodes Generated",    "Figure 1: Nodes Generated vs State-Space Size"),
    ("max_frontier", "Max Frontier Size",  "Figure 2: Max Frontier Size vs State-Space Size"),
    ("time_ms",      "Execution Time (ms)","Figure 3: Execution Time (ms) vs State-Space Size"),
]

for ax, (key, ylabel, title) in zip(axes, metrics):
    for aname, _ in ALGOS:
        pts = numeric_rows(aname)
        if pts:
            xs = [p[0] for p in pts]
            ys = [float(p[1][key]) for p in pts]
            ax.plot(xs, ys, marker="o", label=aname, color=algo_colors[aname])
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel("State-Space Size (log scale)")
    ax.set_ylabel(ylabel + " (log scale)")
    ax.set_title(title, fontsize=9)
    ax.legend()
    ax.grid(True, which="both", linestyle="--", alpha=0.4)

plt.tight_layout()
fig_path = os.path.join(FIG, "performance_comparison.png")
plt.savefig(fig_path, dpi=150)
plt.close()
print(f"Figure saved  → {fig_path}")


# -------------------------------------------------------
# Task 12 – Belief-State experiment
# -------------------------------------------------------
print("\n--- Task 12 Belief-State Experiment ---")

def belief_state_search(adj, goal, k_possible, with_sensor=False, seed=42):
    """
    BFS over belief states for a *small* subgraph (nodes 0..49).
    belief_state : frozenset of possible node locations
    with_sensor  : if True, after each move the local sensor keeps only
                   those nodes that share a neighbour with the goal
                   (simulates partial localisation improvement).
    Returns (belief_states_generated, plan_length)
    """
    # Use the full graph passed in
    sub_nodes = list(adj.keys())
    sub_adj   = adj

    rng = random.Random(seed)
    # pick k start nodes that are NOT the goal
    candidates = [n for n in sub_nodes if n != goal]
    k_actual   = min(k_possible, len(candidates))
    initial    = frozenset(rng.sample(candidates, k_actual))

    visited    = {initial}
    queue      = deque([(initial, 0)])
    belief_gen = 1

    while queue:
        bs, depth = queue.popleft()

        # Goal test: all possible locations are the goal
        if bs == frozenset({goal}) or all(n == goal for n in bs):
            return belief_gen, depth

        if depth >= 30:
            continue

        # Collect all possible actions from any node in belief state
        possible_actions = set()
        for node in bs:
            for nb, _ in sub_adj.get(node, []):
                possible_actions.add(nb)

        for action in list(possible_actions)[:8]:   # bounded branching
            new_bs_set = set()
            for node in bs:
                # try to move toward action; if action is a neighbour, move there
                nbrs = [nb for nb, _ in sub_adj.get(node, [])]
                if action in nbrs:
                    new_bs_set.add(action)
                else:
                    new_bs_set.add(node)    # can't reach action from here

            new_bs = frozenset(new_bs_set)

            if with_sensor:
                # sensor: filter to nodes that are neighbours of goal
                goal_nbrs = {nb for nb, _ in sub_adj.get(goal, [])} | {goal}
                filtered  = frozenset(n for n in new_bs if n in goal_nbrs)
                if filtered:
                    new_bs = filtered

            belief_gen += 1
            if new_bs not in visited:
                visited.add(new_bs)
                queue.append((new_bs, depth + 1))

    return belief_gen, -1


adj_small = generate_hospital_graph(30, seed=SEED)
keys_small = list(adj_small.keys())
goal_node  = keys_small[0]   # use first node as goal (guaranteed reachable)

t12_rows = []
t12_csv  = os.path.join(OUT, "task12_belief_state.csv")
print(f"{'k':>4}  {'Sensor':>8}  {'BeliefStatesGen':>17}  {'PlanLength':>11}")

for k in [2, 4, 8]:
    for sensor in [False, True]:
        bg, pl = belief_state_search(adj_small, goal_node, k,
                                     with_sensor=sensor, seed=SEED)
        label = "Yes" if sensor else "No"
        print(f"{k:>4}  {label:>8}  {bg:>17}  {pl:>11}")
        t12_rows.append({"k": k, "sensor": label,
                          "belief_states_gen": bg, "plan_length": pl})

with open(t12_csv, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["k","sensor","belief_states_gen","plan_length"])
    w.writeheader()
    w.writerows(t12_rows)
print(f"Task-12 results saved → {t12_csv}")

# Task-12 bar chart
ks      = [2, 4, 8]
bg_no   = [r["belief_states_gen"] for r in t12_rows if r["sensor"]=="No"]
bg_yes  = [r["belief_states_gen"] for r in t12_rows if r["sensor"]=="Yes"]

x = np.arange(len(ks))
width = 0.35
fig2, ax2 = plt.subplots(figsize=(7, 4))
ax2.bar(x - width/2, bg_no,  width, label="No sensor",   color="#1f77b4")
ax2.bar(x + width/2, bg_yes, width, label="With sensor", color="#ff7f0e")
ax2.set_xlabel("Number of Possible Locations (k)")
ax2.set_ylabel("Belief States Generated")
ax2.set_title("Figure 4: Task 12 – Belief States Generated vs k (with/without sensor)")
ax2.set_xticks(x)
ax2.set_xticklabels([str(k) for k in ks])
ax2.legend()
ax2.grid(axis="y", linestyle="--", alpha=0.4)
plt.tight_layout()
fig2_path = os.path.join(FIG, "task12_belief_states.png")
plt.savefig(fig2_path, dpi=150)
plt.close()
print(f"Task-12 figure saved → {fig2_path}")
print("\nAll experiments complete.")
