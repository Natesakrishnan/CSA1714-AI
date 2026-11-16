import json, math
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
R = lambda f: json.load(open(f"results/{f}.json"))
# T2: competitive ratio vs size for three braiding levels
d = R("task2")["size_density"]; plt.figure(figsize=(6, 4))
for br, lab in ((0.0, "perfect maze (dead-end density ~6%)"), (0.5, "braided 50%"), (1.0, "fully braided (no dead ends)")):
    rows = [x for x in d if x["braid"] == br]; plt.plot([x["grid"] for x in rows], [x["ratio"] for x in rows], "o-", label=lab)
plt.xlabel("Maze side (cells)"); plt.ylabel("Mean competitive ratio (moves / optimal)"); plt.grid(alpha=.3); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig("results/fig_task2_ratio.png", dpi=130); plt.close()
# T3: bars
d = R("task3"); x = [f"b={r['b']},d={r['d']}" for r in d]; import numpy as np; xs = np.arange(len(d)); w = 0.2
plt.figure(figsize=(7.5, 4))
for i, (k, lab) in enumerate((("best_order", "best order"), ("random_order", "random (mean of 30)"), ("sorted_worst_order", "value-sorted worst"), ("nested_adversarial", "nested adversarial"))):
    plt.bar(xs+(i-1.5)*w, [r[k]["ab_nodes"] for r in d], w, label=lab)
plt.yscale("log"); plt.xticks(xs, x); plt.ylabel("Alpha-beta nodes visited (log)"); plt.legend(fontsize=8); plt.grid(alpha=.3, axis="y"); plt.tight_layout(); plt.savefig("results/fig_task3_nodes.png", dpi=130); plt.close()
# T6: growth
g = R("task6")["growth"]; plt.figure(figsize=(6, 4))
plt.semilogy([r["n"] for r in g], [r["tours"] for r in g], "o-", label="tours evaluated (measured)"); plt.semilogy([r["n"] for r in g], [math.factorial(r["n"]) for r in g], "k--", label="n!")
plt.semilogy([r["n"] for r in g], [max(r["time_s"], 1e-4) for r in g], "s-", label="time (s)")
plt.xlabel("Number of customers n"); plt.ylabel("Count / seconds (log)"); plt.grid(alpha=.3); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig("results/fig_task6_growth.png", dpi=130); plt.close()
# T7: scaling
s = R("task7")["scaling"]; plt.figure(figsize=(6, 4))
plt.semilogy([r["n"] for r in s], [r["orig_nodes"] for r in s], "k--o", label="original: nodes = sum n!/(n-k)!"); plt.semilogy([r["n"] for r in s], [r["nodes_mean"] for r in s], "o-", label="redesign: mean nodes (5 instances)")
plt.semilogy([r["n"] for r in s], [r["nodes_max"] for r in s], "s:", label="redesign: worst instance")
plt.xlabel("Number of customers n"); plt.ylabel("Partial tours created (log)"); plt.grid(alpha=.3); plt.legend(fontsize=8); plt.tight_layout(); plt.savefig("results/fig_task7_scaling.png", dpi=130)
