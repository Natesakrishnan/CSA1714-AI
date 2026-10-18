# Question 3 - CSP: workshop timetable with MRV + degree tie-break + forward checking
SLOTS = ["Morning", "Afternoon", "Evening"]
conflicts = [("W1","W2"),("W1","W3"),("W2","W3"),("W2","W4"),("W3","W5"),("W4","W5")]
domains = {f"W{i}": list(SLOTS) for i in range(1, 6)}
domains["W3"].remove("Morning")   # W3 trainer unavailable in the morning
domains["W4"].remove("Evening")   # W4 hall unavailable in the evening
neigh = {w: set() for w in domains}
for a, b in conflicts:
    neigh[a].add(b); neigh[b].add(a)

def pick(domains, assigned):
    un = [w for w in domains if w not in assigned]
    # fewest remaining slots -> most unscheduled conflicts -> lowest number
    return min(un, key=lambda w: (len(domains[w]),
               -len([n for n in neigh[w] if n not in assigned]), int(w[1:])))

def solve(domains, assigned):
    if len(assigned) == len(domains):
        return assigned
    w = pick(domains, assigned)
    for slot in domains[w]:                       # Morning, Afternoon, Evening
        new = {k: list(v) for k, v in domains.items()}
        new[w] = [slot]
        ok = True
        for n in neigh[w]:
            if n not in assigned:
                if slot in new[n]: new[n].remove(slot)
                if not new[n]: ok = False          # dead end -> backtrack
        if ok:
            a2 = dict(assigned); a2[w] = slot
            rem = {k: v for k, v in new.items() if k not in a2}
            print(f"Assign {w} = {slot:<9} remaining domains: {rem}")
            res = solve(new, a2)
            if res: return res
    return None

print("Initial domains:", domains)
sol = solve(domains, {})
print("\nTimetable:")
for w in sorted(sol): print(f"  {w}: {sol[w]}")
assert all(sol[a] != sol[b] for a, b in conflicts)
assert sol["W3"] != "Morning" and sol["W4"] != "Evening"
print("All constraints satisfied.")
