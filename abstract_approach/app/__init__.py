# Python 3.4
# Main entry for application
from random import Random
from time import time

seeded_random = Random()
seeded_random.seed(time())

from app.evolution import Evolution


def run():
    evolution = Evolution()
    previous_best = 0
    best_fitness = evolution.best_fitness()
    previous_avg_fitness = evolution.avg_fitness()
    print('Avg. fitness: {:.2f}%'.format(evolution.avg_fitness()*100))

    diff_avg_fitness = 1.0
    recession_count = 0
    while best_fitness < 1.0 and recession_count < 20:
        if best_fitness-previous_best > 0:
            recession_count = 0
        if diff_avg_fitness < -5:
            recession_count -= 2
        elif diff_avg_fitness < 0.1:
            recession_count += 1
        recession_count = recession_count if recession_count > 0 else 0
        previous_best = best_fitness
        evolution.tick()
        best_fitness = evolution.best_fitness()
        avg_fitness = evolution.avg_fitness()
        diff_avg_fitness = avg_fitness - previous_avg_fitness

        previous_avg_fitness = avg_fitness
        print('Avg. fitness: {:.3f}% ({:.3f}% change)'.format(avg_fitness*100, diff_avg_fitness*100))

if __name__ == '__main__':
    run()
