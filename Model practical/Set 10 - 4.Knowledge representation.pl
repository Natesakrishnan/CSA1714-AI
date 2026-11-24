% Knowledge Representation using Facts and Rules

% Facts
studies_ai(kumar).

% Rules
learns_intelligent_systems(X) :-
    studies_ai(X).

can_solve_ai_problems(X) :-
    learns_intelligent_systems(X).

% Query
% ?- can_solve_ai_problems(kumar).