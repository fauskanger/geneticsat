# -*- coding: UTF-8 -*-
# Python 3.4
from app import seeded_random


class Chromosome(object):

    def __init__(self, genes=None, length=8):
        self._length = length
        self._genes = self._create_random_genes() if not genes else genes
        verified = self.verify()
        assert verified

    def __repr__(self):
        return 'Chromosome {}'.format(self.genes())

    def verify(self):
        test = self._length == len(self._genes)
        if not test:
            print('wow, uneven!')
        return test

    def length(self):
        return len(self._genes)

    def genes(self):
        return self._genes

    def _create_random_genes(self):
        new_genes = []
        for _ in range(self._length):
            new_genes.append(seeded_random.choice([True, False]))
        return new_genes
