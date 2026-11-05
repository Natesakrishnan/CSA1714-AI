% Monkey Banana Problem

% State: state(MonkeyPosition, BoxPosition, MonkeyStatus)
% MonkeyStatus = onfloor or onbox

% Initial state:
% Monkey at door, box at window, bananas at middle

% Goal state
goal(state(_, _, has_banana)).

% Monkey walks from one place to another
move(state(P, B, onfloor),
     walk(P, Q),
     state(Q, B, onfloor)) :-
    place(Q),
    P \= Q.

% Monkey pushes the box
move(state(P, P, onfloor),
     push(P, Q),
     state(Q, Q, onfloor)) :-
    place(Q),
    P \= Q.

% Monkey climbs onto the box
move(state(P, P, onfloor),
     climb,
     state(P, P, onbox)).

% Monkey grabs bananas
move(state(middle, middle, onbox),
     grab,
     state(middle, middle, has_banana)).

% Possible places
place(door).
place(window).
place(middle).

% Find a sequence of moves
solve(State, [], State) :-
    goal(State).

solve(State, [Action | Rest], FinalState) :-
    move(State, Action, NextState),
    solve(NextState, Rest, FinalState).
