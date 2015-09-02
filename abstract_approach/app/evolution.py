# -*- coding: UTF-8 -*-
# Python 3.4
import os
from operator import itemgetter
from app import seeded_random
from app.environment import Environment, DifficultEnvironment
from app.chromosome import Chromosome
from app.selector import Selector, NormalizedRatioSelector
from app.mutator import PerGeneMutator, GeneCountRatioMutator, OneGeneChanceMutator


class Evolution(object):
    def __init__(self):
        self._initial_population_size = 4
        self._include_parents = True
        self._birthrate = int(self._initial_population_size/2)  # Number of children per parent chromosome
        self._birthrate -= 1 if self._include_parents else 0
        self._generation = -1                                   # First generation = 0, set in _new_generation(...)

        self._chromosomes = []
        self._fitness_archive = []      # list(dict()) usage: fitness = self_fitness_archive[generation][chromosome]
        self._fitness_dict = dict()
        self._chromosome_counter = dict()

        self._environment = DifficultEnvironment()
        self._selector = NormalizedRatioSelector()
        self._mutator = OneGeneChanceMutator()

        self._create_initial_population()

    def current_generation(self):
        return self._generation

    def _check_fitness(self, chromosome):
        try:
            return self._fitness_dict[chromosome]
        except KeyError:
            self._fitness_dict[chromosome] = self._environment.chromosome_fitness(chromosome)
            return self._fitness_dict[chromosome]

    def sorted_chromosomes(self):
        ordered_dict = tuple((chromosome, self._fitness_dict[chromosome])
                             for chromosome, fitness in
                             sorted(self._fitness_dict.items(), key=itemgetter(1), reverse=True))
        # keyvalue_pairs = list(ordered_dict.items())
        return ordered_dict

    def print_fitness(self):
        print('{}Generation {}'.format(os.linesep, self._generation))
        sorted_chromosomes = self.sorted_chromosomes()
        try:
            for chromosome, fitness in sorted_chromosomes:
                print('Fitness: {} - Chromosome: {}'.format(fitness, chromosome))
        except ValueError as e:
            print('error: {}'.format(e))

    def tick(self):
        self.evolve_next_generation()
        self.print_fitness()

    def evolve_next_generation(self):
        selected = self._selector.select(self.sorted_chromosomes(), k=self._initial_population_size / 2)
        new_genes = self._crossover(selected)
        mutated_genes = [self._mutator.mutate(genes) for genes in new_genes]
        self._new_generation_from_genes(mutated_genes)

    def best_chromosome(self):
        sorteds = self.sorted_chromosomes()
        if not sorteds:
            return None
        return sorteds[0][0]

    def best_fitness(self):
        sorteds = self.sorted_chromosomes()
        try:
            return sorteds[0][1]
        except (IndexError, KeyError):
            return None

    def avg_fitness(self):
        try:
            sz = len(self._chromosomes)
            return sum(fitness for (_, fitness) in self._fitness_dict.items())/sz
        except TypeError as e:
            print('Error: {}'.format(e))

    def _new_generation_from_genes(self, list_of_genes):
        self._new_generation((Chromosome(genes=genes) for genes in list_of_genes))

    def _new_generation(self, chromosomes):
        self._chromosomes = []
        if self._generation >= 0:
            # Save existing generation in archive
            self._fitness_archive.append(self._fitness_dict)
            self._fitness_dict = dict()
        self._generation += 1
        for chromosome in chromosomes:
            self._add_chromosome(chromosome)

    def _create_initial_population(self):
        # Will create random chromosome by default
        chromosomes = [Chromosome() for _ in range(self._initial_population_size)]
        self._new_generation(chromosomes)
        self.print_fitness()

    def _add_chromosome(self, chromosome):
        self._count_chromosome(chromosome)
        self._chromosomes.append(chromosome)
        self._check_fitness(chromosome)

    def _count_chromosome(self, chromosome):
        try:
            self._chromosome_counter[tuple(chromosome.genes())] += 1
        except KeyError:
            self._chromosome_counter[tuple(chromosome.genes())] = 1

    def _crossover(self, parent_chromosomes):
        parent_as = [parent for i, parent in enumerate(parent_chromosomes) if i % 2]
        parent_bs = [parent for parent in parent_chromosomes if parent not in parent_as]

        new_genes = []
        for i, parent_a in enumerate(parent_as):
            parent_b = parent_bs[i]
            for _ in range(self._birthrate):
                new_genes.extend(self._random_crossover(parent_a, parent_b))
        return new_genes

    def _random_crossover(self, chromosome_a, chromosome_b, n_cross_points=2):
        cross_points = seeded_random.sample(range(chromosome_a.length()), n_cross_points)
        cross_points.sort()
        return self._crossover_from_points(chromosome_a, chromosome_b, cross_points)

    def _crossover_from_points(self, chromosome_a, chromosome_b, cross_points):
        genes_a = []
        genes_b = []
        a = chromosome_a.genes()
        b = chromosome_b.genes()
        n_cross = len(cross_points)
        n_genes = len(a)
        previous_i = 0
        for i, cross_point in enumerate(cross_points):
            genes_a.extend(a[previous_i:cross_point])
            genes_b.extend(b[previous_i:cross_point])
            tmp = a
            a = b
            b = tmp
            previous_i = cross_point
        if previous_i < n_genes:
            genes_a += a[previous_i:]
            genes_b += b[previous_i:]
        return genes_a, genes_b
