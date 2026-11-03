
% Facts
male(john).
male(peter).
male(alan).
male(david).

female(mary).
female(lisa).
female(susan).
female(anna).

% Parent relationships
parent(john, peter).
parent(mary, peter).

parent(john, lisa).
parent(mary, lisa).

parent(peter, alan).
parent(susan, alan).

parent(peter, anna).
parent(susan, anna).

parent(lisa, david).

% Rules

% Father relationship
father(X, Y) :-
    male(X),
    parent(X, Y).

% Mother relationship
mother(X, Y) :-
    female(X),
    parent(X, Y).

% Sibling relationship
sibling(X, Y) :-
    parent(P, X),
    parent(P, Y),
    X \= Y.

% Grandparent relationship
grandparent(X, Y) :-
    parent(X, Z),
    parent(Z, Y).

% Brother relationship
brother(X, Y) :-
    male(X),
    sibling(X, Y).

% Sister relationship
sister(X, Y) :-
    female(X),
    sibling(X, Y).
