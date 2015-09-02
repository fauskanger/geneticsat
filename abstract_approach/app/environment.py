# -*- coding: UTF-8 -*-
# Python 3.4


class UnfitChromosomeError(Exception):
    def __init__(self, msg=None):
        super().__init__('UnfitChromosomeError{}'.format('' if not msg else ': '.format(msg)))


class Environment(object):
    def __init__(self, accepted_chromosome_sizes=None, raise_on_unfit_chromosome=False):
        default_szs = [8]
        szs = accepted_chromosome_sizes
        self._raises_on_unfit_chromosome = raise_on_unfit_chromosome
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

    def chromosome_fitness(self, chromosome, default_value=0):
        clauses = self._safe_get_clauses(chromosome)
        if not clauses:
            if self._raises_on_unfit_chromosome:
                raise UnfitChromosomeError('Cannot measure fitness of unfit chromosome. Accepted lengths: {}. {}'
                                           .format(self._chromosome_accepted_sizes, chromosome))
            return default_value
        fitness = sum(1 for clause in clauses if clause)
        return fitness/len(clauses)

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
