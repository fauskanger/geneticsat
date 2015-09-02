# -*- coding: UTF-8 -*-
# Python 3.4
from app import seeded_random


class Mutator(object):
    def __init__(self):
        self.mutation_rate = 0.1
        self.mutate_roll_per_gene = True
        pass

    def mutate(self, genes):
        if self.mutate_roll_per_gene:
            return [gene if seeded_random.random() < self.mutation_rate else not gene for gene in genes]
        n = len(genes)
        to_mutate = seeded_random.sample(range(n), max(n * self.mutation_rate, 1))
        for i in to_mutate:
            genes[i] = not genes[i]
        return genes
