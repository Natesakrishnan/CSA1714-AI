"""Exam-scheduling CSP: Plain Backtracking vs Backtracking + Forward Checking"""

import copy

# ---------------------------------------------------------
# Problem Definition
# ---------------------------------------------------------

VARIABLES = ["A", "B", "C", "D", "E"]

# Value order: Slot1 -> Slot2 -> Slot3
DOMAIN = ["Slot1", "Slot2", "Slot3"]

# Conflicting course pairs
EDGES = [
    ("A", "B"),
    ("A", "C"),
    ("B", "C"),
    ("B", "D"),
    ("C", "D"),
    ("C", "E"),
    ("D", "E")
]

# ---------------------------------------------------------
# Create Neighbour List
# ---------------------------------------------------------

NEIGHBOURS = {v: set() for v in VARIABLES}

for u, v in EDGES:
    NEIGHBOURS[u].add(v)
    NEIGHBOURS[v].add(u)


# ---------------------------------------------------------
# Check whether an assignment is consistent
# ---------------------------------------------------------

def consistent(var, val, assignment):
    """
    Checks whether assigning val to var violates
    any constraint with an already assigned neighbour.
    """

    return all(
        assignment.get(n) != val
        for n in NEIGHBOURS[var]
    )


# =========================================================
# 1. PLAIN BACKTRACKING SEARCH
# =========================================================

def backtracking(assignment, stats, log):

    # Goal test
    if len(assignment) == len(VARIABLES):
        return assignment

    # Static variable order:
    # A -> B -> C -> D -> E
    var = VARIABLES[len(assignment)]

    # Static value order:
    # Slot1 -> Slot2 -> Slot3
    for val in DOMAIN:

        stats["attempts"] += 1

        # Check constraint
        if consistent(var, val, assignment):

            log.append(
                (stats["attempts"], var, val, "ACCEPTED")
            )

            # Assign value
            assignment[var] = val

            # Recursive search
            result = backtracking(
                assignment,
                stats,
                log
            )

            # Solution found
            if result:
                return result

            # Undo assignment
            del assignment[var]

            stats["backtracks"] += 1

            log.append(
                (
                    stats["attempts"],
                    var,
                    val,
                    "BACKTRACK"
                )
            )

        else:

            stats["failed"] += 1

            log.append(
                (
                    stats["attempts"],
                    var,
                    val,
                    "REJECTED (conflict)"
                )
            )

    return None


# =========================================================
# 2. BACKTRACKING WITH FORWARD CHECKING
# =========================================================

def forward_checking(assignment, domains, stats, log):

    # Goal test
    if len(assignment) == len(VARIABLES):
        return assignment

    # Static variable order
    var = VARIABLES[len(assignment)]

    # Only surviving domain values are considered
    for val in list(domains[var]):

        stats["attempts"] += 1

        # Copy domains so that changes can be undone
        new_domains = copy.deepcopy(domains)

        # Assign current variable
        new_domains[var] = [val]

        pruned = []
        wipeout = False

        # -------------------------------------------------
        # Forward Checking
        # Remove current value from the domains
        # of all unassigned neighbouring variables.
        # -------------------------------------------------

        for n in NEIGHBOURS[var]:

            if n not in assignment and val in new_domains[n]:

                new_domains[n].remove(val)

                pruned.append((n, val))

                # Domain becomes empty
                if not new_domains[n]:
                    wipeout = True

        # -------------------------------------------------
        # If any domain becomes empty, reject assignment
        # -------------------------------------------------

        if wipeout:

            stats["failed"] += 1

            log.append(
                (
                    stats["attempts"],
                    var,
                    val,
                    "WIPE-OUT",
                    pruned,
                    new_domains
                )
            )

            continue

        # -------------------------------------------------
        # Accept assignment
        # -------------------------------------------------

        assignment[var] = val

        log.append(
            (
                stats["attempts"],
                var,
                val,
                "ACCEPTED",
                pruned,
                new_domains
            )
        )

        # Recursive search
        result = forward_checking(
            assignment,
            new_domains,
            stats,
            log
        )

        # Solution found
        if result:
            return result

        # Undo assignment
        del assignment[var]

        stats["backtracks"] += 1

    return None


# =========================================================
# MAIN PROGRAM
# =========================================================

if __name__ == "__main__":

    # -----------------------------------------------------
    # Plain Backtracking
    # -----------------------------------------------------

    stats1 = {
        "attempts": 0,
        "failed": 0,
        "backtracks": 0
    }

    log1 = []

    solution1 = backtracking(
        {},
        stats1,
        log1
    )

    print("=" * 60)
    print("PLAIN BACKTRACKING")
    print("=" * 60)

    for record in log1:
        print(record)

    print("\nSolution:")
    print(solution1)

    print("\nStatistics:")
    print("Assignment Attempts :", stats1["attempts"])
    print("Failed Attempts     :", stats1["failed"])
    print("Backtracks           :", stats1["backtracks"])


    # -----------------------------------------------------
    # Backtracking + Forward Checking
    # -----------------------------------------------------

    stats2 = {
        "attempts": 0,
        "failed": 0,
        "backtracks": 0
    }

    log2 = []

    # Initial domains
    initial_domains = {
        v: list(DOMAIN)
        for v in VARIABLES
    }

    solution2 = forward_checking(
        {},
        initial_domains,
        stats2,
        log2
    )

    print("\n" + "=" * 60)
    print("BACKTRACKING + FORWARD CHECKING")
    print("=" * 60)

    for record in log2:

        print("\nAttempt:", record[0])
        print("Variable:", record[1])
        print("Value:", record[2])
        print("Status:", record[3])

        if len(record) > 4:

            print("Pruned:", record[4])

            print("Domains:")

            for variable, domain in record[5].items():
                print(
                    "  ",
                    variable,
                    "->",
                    domain
                )

    print("\nSolution:")
    print(solution2)

    print("\nStatistics:")
    print("Assignment Attempts :", stats2["attempts"])
    print("Failed Attempts     :", stats2["failed"])
    print("Backtracks           :", stats2["backtracks"])
