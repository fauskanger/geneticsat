# -*- coding: UTF-8 -*-
# Python 3.4


class Environment(object):
    def __init__(self):
        pass

    def get_conjunctions(self, chromosome):
        x1, x2, x3, x4, x5, x6, x7, x8 = chromosome.genes()
        return [
            x1 or x5,
            x3 or not x1,
            x6 or x8,
            x3 or not x7,
            x2 or not x4,
            x3 or x8 or not x5
        ]

    def chromosome_fitness(self, chromosome):
        conjunctions = self.get_conjunctions(chromosome)
        fitness = sum(1 for premise in conjunctions if premise)
        return fitness/len(conjunctions)


class DifficultEnvironment(Environment):
    def __init__(self):
        super().__init__()

    def get_conjunctions(self, chromosome):
        x1, x2, x3, x4, x5, x6, x7, x8 = chromosome.genes()
        return [
            x1 or x5,
            x3 or not x1,
            x6 or x8,
            x3 or not x7,
            x2 or not x4,
            x3 or x8 or not x5,
            not x1 or x5,
            not x3 and not x7,
            x2 and not x1
        ]
