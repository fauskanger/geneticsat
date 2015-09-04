# -*- coding: UTF-8 -*-
# Python 3.4
from app import seeded_random


# abstract class
class BaseMutator(object):
    def __init__(self, mutation_rate=0.0):
        self.mutation_rate = mutation_rate

    def mutate(self, genes):
        return genes

    def _is_mutating(self):
        return seeded_random.random() < self.mutation_rate


class PerGeneMutator(BaseMutator):
    def __init__(self, mutation_rate=0.013):  # => (1-0.013)^8 = 0.901 chance of not mutating.
        super().__init__(mutation_rate)

    def mutate(self, genes):
        return [gene if self._is_mutating() else not gene for gene in genes]


class OneGeneChanceMutator(BaseMutator):
    def __init__(self, mutation_rate=0.1):
        super().__init__(mutation_rate)

    def mutate(self, genes):
        if not self._is_mutating():
            return genes
        mutant = seeded_random.choice(range(len(genes)))
        genes[mutant] = not genes[mutant]
        return genes


class GeneCountRatioMutator(BaseMutator):
    def __init__(self, mutation_rate=0.1):
        super().__init__(mutation_rate)

    def mutate(self, genes):
        n = len(genes)
        to_mutate = seeded_random.sample(range(n), max(n * self.mutation_rate, 1))
        for i in to_mutate:
            genes[i] = not genes[i]
        return genes

