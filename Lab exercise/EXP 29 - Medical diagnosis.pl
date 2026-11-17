
% Medical Diagnosis System

% Symptoms of diseases

symptom(flu, fever).
symptom(flu, cough).
symptom(flu, headache).
symptom(flu, body_pain).

symptom(common_cold, sneezing).
symptom(common_cold, cough).
symptom(common_cold, runny_nose).

symptom(malaria, fever).
symptom(malaria, chills).
symptom(malaria, sweating).
symptom(malaria, headache).

symptom(dengue, fever).
symptom(dengue, headache).
symptom(dengue, joint_pain).
symptom(dengue, skin_rash).

% Diagnosis rules

diagnosis(flu) :-
    symptom(flu, fever),
    symptom(flu, cough),
    symptom(flu, headache).

diagnosis(common_cold) :-
    symptom(common_cold, sneezing),
    symptom(common_cold, cough),
    symptom(common_cold, runny_nose).

diagnosis(malaria) :-
    symptom(malaria, fever),
    symptom(malaria, chills),
    symptom(malaria, sweating).

diagnosis(dengue) :-
    symptom(dengue, fever),
    symptom(dengue, headache),
    symptom(dengue, joint_pain),
    symptom(dengue, skin_rash).

% Display diagnosis

check_disease(Disease) :-
    diagnosis(Disease),
    write('Possible Disease: '),
    write(Disease),
    nl.