
# Perceptron Learning Algorithm for AND Gate

inputs = [
    [0, 0],
    [0, 1],
    [1, 0],
    [1, 1]
]

targets = [0, 0, 0, 1]

weights = [0.0, 0.0]
bias = 0.0
learning_rate = 0.1
epochs = 10

def activation(x):
    return 1 if x >= 0 else 0

for epoch in range(epochs):
    for x, target in zip(inputs, targets):
        summation = (
            weights[0] * x[0] +
            weights[1] * x[1] + bias
        )

        prediction = activation(summation)
        error = target - prediction

        weights[0] += learning_rate * error * x[0]
        weights[1] += learning_rate * error * x[1]
        bias += learning_rate * error

    print("Epoch:", epoch + 1)
    print("Weights:", weights)
    print("Bias:", bias)

print("\nAND Gate Testing")
print("X1 X2 Output")

for x in inputs:
    summation = (
        weights[0] * x[0] +
        weights[1] * x[1] + bias
    )

    output = activation(summation)
    print(x[0], x[1], " ", output)
