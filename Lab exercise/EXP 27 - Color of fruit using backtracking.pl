% Facts: Fruit and its color

fruit_color(apple, red).
fruit_color(banana, yellow).
fruit_color(orange, orange).
fruit_color(grapes, green).
fruit_color(mango, yellow).
fruit_color(strawberry, red).
fruit_color(guava, green).
fruit_color(cherry, red).

% Rule to display fruit and color
display_fruit_color :-
    fruit_color(Fruit, Color),
    write(Fruit),
    write(' is '),
    write(Color),
    nl,
    fail.

display_fruit_color.
