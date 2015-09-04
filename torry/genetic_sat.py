from random import randint
from random import random


def run(print_results=True):
    generation = prev_generation = population(4)
    best_individual = create_random_individual()
    best_score = fitness(best_individual)
    counter = 0
    convergence_count = 0
    converged = False
    while best_score < 1 and not converged:

        for ind in generation:
            if fitness(ind) > best_score:
                best_individual = ind
                best_score = fitness(ind)

        convergence_count = convergence_count + 1 if abs(pop_fit(prev_generation) - pop_fit(generation)) <= 0.1 else 0
        converged = convergence_count > 10
        counter += 1
        prev_generation = generation
        if print_results:
            print("\nGeneration {} score: {:.3f}".format(counter, pop_fit(generation)))
        generation = evolve(generation)

    if print_results:
        print("\nSolved with a total of {} generations.\nBest individual:".format(counter))
        print(best_individual)
        print("Fitness: {:.2f}".format(best_score))

    return best_individual


def run_many(count=10000):
    best_individuals = []
    for _ in range(0, count):
        best_individuals.append(run(False))
    success_count = sum(abs(1.0 - fitness(i)) <= 0.01 for i in best_individuals)
    print("Found solution in {}/{} runs".format(success_count, count))


def create_random_individual():
    return [randint(0, 1) for _ in range(8)]


def population(count):
    return [create_random_individual() for _ in range(count)]


def pop_fit(pop):
    return sum([fitness(ind) for ind in pop]) / len(pop)


def fitness(ind):
    (x1, x2, x3, x4, x5, x6, x7, x8) = ind
    clauses = [
        x1 or x5,
        x3 or not x1,
        x6 or x8,
        not x7 or x3,
        x2 or not x4,
        x3 or x8 or not x5
    ]
    return sum(clauses) / len(clauses)


def evolve(pop, selection_ratio=0.5, random_select=0.05):
    sorted_pop = sorted(pop, key=lambda ind: fitness(ind), reverse=True)
    selection_size = int(len(sorted_pop) * selection_ratio)
    parents = sorted_pop[:selection_size]

    for ind in sorted_pop:
        if random_select > random():
            parents.append(ind)

    remaining_length = len(pop) - len(parents)
    children = []
    while len(children) < remaining_length:
        male = randint(0, len(parents) - 1)
        female = randint(0, len(parents) - 1)
        if male != female:
            children.extend(crossover(parents[male], parents[female]))
    parents.extend(children)
    parents = parents[:len(pop)]
    return [mutate(ind) for ind in parents]


def crossover(male, female):
    point_1 = randint(1, len(male) - 1)
    point_2 = randint(point_1, len(male))
    first_child = male[:point_1] + female[point_1:point_2] + male[point_2:len(male)]
    second_child = female[:point_1] + male[point_1:point_2] + female[point_2:len(male)]
    return first_child, second_child


def mutate(individual):
    return [0.3 > random() != gene for gene in individual]

run_many()