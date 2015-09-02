# -*- coding: UTF-8 -*-
# Python 3.4
import random


def create_random_chromosome():
    return [random.choice([True, False]) for _ in range(8)]


def fitness(chromosome):
    x1, x2, x3, x4, x5, x6, x7, x8 = chromosome
    clauses = [
        x1 or x5,
        x3 or not x1,
        x6 or x8,
        x3 or not x7,
        x2 or not x4,
        x3 or x8 or not x5,
        not x1,
        not x8
    ]
    return sum(clauses)/len(clauses)


def run():
    def output_results(_count, _best_score, _best_chromosome):
        print('Best fitness after {} generations: {:3f}% Chromosome: {}'.format(_count, _best_score, _best_chromosome))
    chromosomes = [create_random_chromosome() for _ in range(4)]
    best_score, best_chromosome = best_fitness(chromosomes)
    count = 0
    output_results(count, best_score, best_chromosome)
    while best_score < 1 and count < 1000:
        count += 1
        chromosomes = evolve(chromosomes)
        best_score, best_chromosome = best_fitness(chromosomes)
        output_results(count, best_score, best_chromosome)


def best_fitness(chromosomes):
    return max([(fitness(c), c) for c in chromosomes])


def evolve(chromosomes):
    children_of_best = sorted(chromosomes, key=lambda c: fitness(c), reverse=True)[:2]
    crossed = []
    crossed.extend(crossover(*children_of_best))
    crossed.extend(list(children_of_best))
    return [mutate(chromosome)for chromosome in crossed]


def crossover(chromosome_a, chromosome_b):
    cross_point = sorted(random.sample(range(8), 2))
    start = cross_point[0]
    end = cross_point[1]
    new_a = chromosome_a[:start]
    new_a += chromosome_b[start:end]
    new_b = chromosome_b[:start]
    new_b += chromosome_a[start:end]
    if end < 7:
        new_a += chromosome_a[end:]
        new_b += chromosome_b[end:]
    return new_a, new_b


def is_mutating():
    return random.random() > 0.1


def mutate(chromosome):
    return [is_mutating() != gene for gene in chromosome]  # is_mutation XOR gene


if __name__ == '__main__':
    run()
