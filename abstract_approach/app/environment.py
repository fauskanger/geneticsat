# -*- coding: UTF-8 -*-
# Python 3.4


class Environment(object):
    def __init__(self, accepted_chromosome_sizes=None):
        default_szs = [8]
        szs = accepted_chromosome_sizes
        self._chromosome_accepted_sizes = szs if szs else default_szs

    def _verify_chromosome(self, chromosome):
        return chromosome.length() in self._chromosome_accepted_sizes

    def get_clauses(self, chromosome):
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
        conjunctions = self._safe_get_clauses(chromosome)
        fitness = sum(1 for premise in conjunctions if premise)
        return fitness/len(conjunctions)

    def _safe_get_clauses(self, chromosome):
        return [] if not self._verify_chromosome(chromosome) else self.get_clauses(chromosome)


class DifficultEnvironment(Environment):
    def __init__(self):
        super().__init__()

    def get_clauses(self, chromosome):
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
