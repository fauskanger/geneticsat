from random import randint
from random import random


def _individual(length, min, max):
    return [randint(min, max) for x in range(length)]

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

    score = sum(clauses) / len(clauses)
    return score

def population(count, individual_length, min, max):
    return [_individual(individual_length, min, max) for x in range(count)]

def population_grade(pop):
    grade = 0
    for individual in pop:
        grade += fitness(individual)
    return 1 - (grade / len(pop))

def evolve(pop, selection_ratio=0.5, random_select=0.05, mutation_rate=0.1):
    sorted_pop = [(fitness(x), x) for x in pop]
    sorted_pop = [x[1] for x in sorted(sorted_pop)]
    selection_size = int(len(sorted_pop)*selection_ratio)
    parents = sorted_pop[:selection_size]

    for ind in sorted_pop:
        if random_select > random():
            parents.append(ind)

    remaining_length = len(pop) - len(parents)
    children = []
    while len(children) < remaining_length:
        male = randint(0, len(parents)-1)
        female = randint(0, len(parents)-1)
        if male != female:
            children.extend(crossover(parents[male], parents[female]))
    parents.extend(children)
    parents = parents[:len(pop)]
    return [mutate(ind, mutation_rate) for ind in parents]


def crossover(male, female):
    point_1 = randint(1, len(male)-1)
    point_2 = randint(point_1, len(male))

    first_child = male[:point_1] + female[point_1:point_2] + male[point_2:len(male)]
    second_child = female[:point_1] + male[point_1:point_2] + female[point_2:len(male)]

    return first_child, second_child


def mutate(individual, rate):
    if rate > random():
        gene_to_mutate = randint(0, 7)
        individual[gene_to_mutate] = 1 if not individual[gene_to_mutate] else 0
    return individual


def main():
    gen = prev_gen = population(4, 8, 0, 1)
    best_individual = _individual(8, 0, 1)

    counter = 0
    convergence_count = 0
    converged = False
    solved = False
    while not solved and not converged:

        for ind in gen:
            best_individual = ind if fitness(ind) > fitness(best_individual) else best_individual
        solved = abs(1.0 - fitness(best_individual)) <= 0.1
        print("\n\nGeneration {}:".format(counter))
        print(gen)
        print("Population average fitness: {0:.2f}".format(population_grade(gen)))
        print("Best individual: ")
        print(best_individual)
        print("...and its fitness: {:.2f}".format(fitness(best_individual)))

        convergence_count = convergence_count + 1 if abs(population_grade(prev_gen) - population_grade(gen)) <= 0.1 else 0
        converged = convergence_count > 100
        counter += 1
        prev_gen = gen
        gen = evolve(gen)


main()
# sample_pop = population(100, 8, 0, 1)