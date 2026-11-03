% Facts: Birds that can fly
can_fly(parrot).
can_fly(eagle).
can_fly(pigeon).
can_fly(sparrow).
can_fly(crow).

% Facts: Birds that cannot fly
cannot_fly(penguin).
cannot_fly(ostrich).
cannot_fly(kiwi).

% Rule to check whether a bird can fly
bird_fly(Bird) :-
    can_fly(Bird),
    write(Bird),
    write(' can fly.').

% Rule to check whether a bird cannot fly
bird_fly(Bird) :-
    cannot_fly(Bird),
    write(Bird),
    write(' cannot fly.').
