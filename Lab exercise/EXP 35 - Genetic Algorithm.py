
import random

# Objective function
def fitness(x):
    return x ** 2

# Generate initial population
population = [random.randint(0, 31) for _ in range(6)]

# Genetic Algorithm parameters
generations = 20
mutation_rate = 0.1

for generation in range(generations):

    # Evaluate fitness
    population.sort(key=fitness, reverse=True)

    # Selection
    parents = population[:3]

    # Crossover
    offspring = []
    for i in range(3):
        parent1 = random.choice(parents)
        parent2 = random.choice(parents)

        child = (parent1 + parent2) // 2
        offspring.append(child)

    # Mutation
    for i in range(len(offspring)):
        if random.random() < mutation_rate:
            offspring[i] = random.randint(0, 31)

    # Create new population
    population = parents + offspring

    # Display generation result
    best = max(population, key=fitness)

    print("Generation:", generation + 1,
          "Best Solution:", best,
          "Fitness:", fitness(best))

# Final result
best = max(population, key=fitness)

print("\nOptimal Solution:", best)
print("Maximum Fitness:", fitness(best))
