# -*- coding: UTF-8 -*-
# Python 3.4


class Environment(object):

    def __init__(self):
        self._chromosomes = []
        self._fitness_dict = dict()
        pass

    def add_chromosome(self, chromosome):
        self._chromosomes.append(chromosome)
        self._fitness_dict[chromosome] = self._chromosome_fitness(chromosome)

    def _chromosome_fitness(self, chromosome):
        x1, x2, x3, x4, x5, x6, x7, x8 = chromosome.genes()
        conjunctions = [
            x1 or x5,
            x3 or not x1,
            x6 or x8,
            x3 or not x7,
            x2 or not x4,
            x3 or x8 or not x5
        ]
        fitness = sum(1 for premise in conjunctions if premise)
        return fitness
