"""
Q3 - CSP (map colouring) : backtracking + forward checking + MRV + degree heuristic
"""
VARS = ["WA", "NT", "SA", "Q", "NSW", "V"]
DOMAIN = ["R", "G", "B"]
EDGES = [("WA", "NT"), ("WA", "SA"), ("NT", "SA"), ("NT", "Q"), ("SA", "Q"),
         ("SA", "NSW"), ("SA", "V"), ("Q", "NSW"), ("NSW", "V")]
NB = {v: set() for v in VARS}
for a, b in EDGES:
    NB[a].add(b)
    NB[b].add(a)


def fmt(domains, assigned):
    return "  ".join(f"{v}:{{{','.join(domains[v])}}}" for v in VARS if v not in assigned)


def select_variable(domains, assigned):
    unassigned = [v for v in VARS if v not in assigned]
    # MRV -> degree (most unassigned neighbours) -> fixed order
    return min(unassigned,
               key=lambda v: (len(domains[v]),
                              -len([n for n in NB[v] if n not in assigned]),
                              VARS.index(v)))


def backtrack(assigned, domains, log, depth=0):
    if len(assigned) == len(VARS):
        return assigned
    var = select_variable(domains, assigned)
    for colour in DOMAIN:
        if colour not in domains[var]:
            continue
        new_assigned = dict(assigned, **{var: colour})
        new_domains = {v: list(d) for v, d in domains.items()}
        new_domains[var] = [colour]
        pruned, failed = [], False
        for n in sorted(NB[var], key=VARS.index):   # forward checking
            if n not in new_assigned and colour in new_domains[n]:
                new_domains[n].remove(colour)
                pruned.append(n)
                if not new_domains[n]:
                    failed = True
        log.append((depth + 1, var, colour, fmt(new_domains, new_assigned),
                    pruned, "DEAD END - backtrack" if failed else ""))
        if not failed:
            result = backtrack(new_assigned, new_domains, log, depth + 1)
            if result:
                return result
    return None


if __name__ == "__main__":
    domains = {v: list(DOMAIN) for v in VARS}
    log = []
    solution = backtrack({}, domains, log)
    print("Initial domains:", fmt(domains, {}))
    for i, (d, var, col, doms, pruned, note) in enumerate(log, 1):
        print(f"Step {i}: assign {var}={col}  | removed {col} from {pruned or '-'}")
        print("        domains ->", doms or "(all assigned)", note)
    print("\nFinal colouring:", solution)
    ok = all(solution[a] != solution[b] for a, b in EDGES)
    print("All constraints satisfied:", ok)
