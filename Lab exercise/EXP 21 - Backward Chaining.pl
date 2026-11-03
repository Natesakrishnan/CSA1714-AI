% Facts
parent(john, mary).
parent(mary, susan).
parent(susan, david).

% Rules
% X is an ancestor of Y if X is a parent of Y.
ancestor(X, Y) :-
    parent(X, Y).

% X is an ancestor of Y if X is a parent of Z
% and Z is an ancestor of Y.
ancestor(X, Y) :-
    parent(X, Z),
    ancestor(Z, Y).
