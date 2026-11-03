% Initial facts
parent(john, mary).
parent(mary, susan).
parent(susan, david).

% Rules
% If X is a parent of Y, X is an ancestor of Y.
ancestor(X, Y) :-
    parent(X, Y).

% If X is a parent of Z and Z is an ancestor of Y,
% then X is an ancestor of Y.
ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).

% Forward chaining to derive ancestor relationships
forward_chaining :-
    ancestor(X, Y),
    write(X),
    write(' is an ancestor of '),
    write(Y),
    nl,
    fail.

forward_chaining.
