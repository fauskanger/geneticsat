# -*- coding: UTF-8 -*-
# Python 3.4
from app import seeded_random


class Selector(object):
    def __init__(self):
        pass

    def select(self, sorted_chromosome_fitness, k):  # Tuple(Chromosome, Fitness)
        k = int(k)
        kth_best = sorted_chromosome_fitness[:k]
        return [chromosome for chromosome, _ in kth_best]


class NormalizedRatioSelector(Selector):
    def __init__(self, unique_selection=True):
        super().__init__()
        self._unique = unique_selection

    def select(self, sorted_chromosome_fitness, k):
        if k >= len(sorted_chromosome_fitness) and self._unique:
            AttributeError("Not enough alternatives in population")
        total_fitness = sum(fitness for _, fitness in sorted_chromosome_fitness)
        selected = []
        while len(selected) < k:
            random_threshold = seeded_random.random() * total_fitness
            acc = 0
            for chromosome, fitness in sorted_chromosome_fitness:
                acc += fitness
                if acc > random_threshold and not (chromosome in selected and self._unique):
                    selected.append(chromosome)
                    break
        return selected
