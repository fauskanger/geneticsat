# Python 3.4
# Main entry for application
from random import Random
from time import time

seeded_random = Random()
seeded_random.seed(time())

from app.evolution import Evolution


def run():
    evolution = Evolution()
    best_fitness = evolution.best_fitness()
    previous_avg_fitness = evolution.avg_fitness()
    print('Avg. fitness: {:.2f}%'.format(evolution.avg_fitness()*100))
    diff_avg_fitness = 1.0
    recession_count = 0
    while best_fitness < 1.0 and recession_count < 10:
        if diff_avg_fitness < 0.01:
            recession_count += 1
        evolution.tick()
        best_fitness = evolution.best_fitness()
        avg_fitness = evolution.avg_fitness()
        diff_avg_fitness = avg_fitness - previous_avg_fitness
        previous_avg_fitness = avg_fitness
        print('Avg. fitness: {:.3f}% ({:.3f}% change)'.format(avg_fitness*100, diff_avg_fitness*100))

if __name__ == '__main__':
    run()
