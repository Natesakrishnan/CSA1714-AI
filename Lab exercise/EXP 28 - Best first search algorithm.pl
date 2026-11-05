% Best First Search Algorithm

% Graph edges
edge(a, b).
edge(a, c).
edge(b, d).
edge(b, e).
edge(c, f).
edge(d, g).
edge(e, g).
edge(f, g).

% Heuristic values
h(a, 7).
h(b, 6).
h(c, 4).
h(d, 3).
h(e, 2).
h(f, 1).
h(g, 0).

% Best First Search
best_first(Start, Goal, Path) :-
    h(Start, H),
    search([H-[Start]], Goal, [], RevPath),
    reverse(RevPath, Path).

% Goal reached
search([_- [Goal|Rest] | _], Goal, _, [Goal|Rest]).

% Expand the node with lowest heuristic
search([_- [Node|RestPath] | Open], Goal, Visited, Path) :-
    Node \= Goal,
    findall(H-[Next,Node|RestPath],
            (edge(Node, Next),
             \+ member(Next, [Node|RestPath]),
             \+ member(Next, Visited),
             h(Next, H)),
            Children),
    append(Open, Children, Combined),
    keysort(Combined, Sorted),
    search(Sorted, Goal, [Node|Visited], Path).
