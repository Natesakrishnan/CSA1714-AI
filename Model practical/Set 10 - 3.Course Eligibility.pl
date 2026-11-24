% Course Eligibility Expert System

% Student marks
marks(kumar, 85, 90, 75).
marks(raja, 45, 80, 65).
marks(ajay, 70, 75, 80).

% Eligibility rules
eligible(Student) :-
    marks(Student, Math, Programming, English),
    Math >= 60,
    Programming >= 60,
    English >= 50.

% Check eligibility
check_eligibility(Student) :-
    eligible(Student),
    write(Student),
    write(' is eligible for the course.').

check_eligibility(Student) :-
    \+ eligible(Student),
    write(Student),
    write(' is not eligible for the course.').
