% Diet suggestions based on disease

% Disease and diet facts
diet(diabetes, 'Balanced meals with controlled carbohydrates').
diet(hypertension, 'Low-sodium diet with fruits and vegetables').
diet(obesity, 'Calorie-controlled diet with vegetables and whole grains').
diet(anemia, 'Iron-rich foods such as spinach and beans').
diet(heart_disease, 'Low-saturated-fat diet with fruits and vegetables').
diet(acidity, 'Small meals and non-spicy foods').

% Rule to suggest diet based on disease
suggest_diet(Disease, Diet) :-
    diet(Disease, Diet).

% Rule to display diet suggestion
display_diet(Disease) :-
    suggest_diet(Disease, Diet),
    write('Disease: '),
    write(Disease),
    nl,
    write('Recommended Diet: '),
    write(Diet),
    nl.
