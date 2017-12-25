import numpy as np
import individual as id
import function as fn
import sys
import copy
import os
import csv
from config import Config as cf

"""for result file (results.csv)"""
if os.path.exists("results"):
    pass
else:
    os.mkdir("results")

results = open("results" + os.sep + "results.csv", "w")
results_writer = csv.writer(results, lineterminator="\n")

def main():
    for trial in range(cf.get_trial()):
        np.random.seed(trial)

        results_list = [] # fitness list
        de_list = [] # firefly list
        """Generate Initial Population"""
        for p in range(cf.get_population_size()):
            de_list.append(id.Individual())

        """Sort Array"""
        de_list =  sorted(de_list, key=lambda ID : ID.get_fitness())

        """Find Initial Best"""
        BestPosition = de_list[0].get_position() # Best Solution
        BestFitness = fn.calculation(BestPosition,0)

        """↓↓↓Main Loop↓↓↓"""
        for iteration in range(cf.get_iteration()):

            """list copy"""
            candidate_de_list = copy.deepcopy(de_list)

            """Generate New Solutions"""
            for i in range(len(de_list)):

                candidate = copy.deepcopy(de_list[i])

                """select three points (a, b, c)"""
                a = np.random.randint(0, cf.get_population_size())
                while (a == i):
                    a = np.random.randint(0, cf.get_population_size())
                b = np.random.randint(0, cf.get_population_size())
                while (b == i or a == b):
                    b = np.random.randint(0, cf.get_population_size())
                c = np.random.randint(0, cf.get_population_size())
                while (c == i or c == a or c == b):
                    c = np.random.randint(0, cf.get_population_size())

                """Select Random Index (R)"""
                R = np.random.randint(0,cf.get_dimension())

                candidate.generate(a=de_list[a], b=de_list[b], c=de_list[c], R=R)
                candidate.set_fitness(fn.calculation(candidate.get_position(),iteration))

                if candidate.get_fitness() < de_list[i].get_fitness():
                    candidate_de_list[i] = copy.deepcopy(candidate)

            """Sort Array"""
            de_list = sorted(candidate_de_list, key=lambda ID: ID.get_fitness())

            """Rank and Find the Current Best"""
            if de_list[0].get_fitness() < BestFitness:
                BestPosition = de_list[0].get_position()
                BestFitness = fn.calculation(BestPosition,iteration)

            sys.stdout.write("\r Trial:%3d , Iteration:%7d, BestFitness:%.4f" % (trial , iteration, BestFitness))
            results_list.append(str(BestFitness))

        results_writer.writerow(results_list)

if __name__ == '__main__':
    main()
    results.close()