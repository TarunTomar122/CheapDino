from neural import *
import random

num_generations = 1000
individual_per_pop = 20
num_parents = 5
num_babies = individual_per_pop - num_parents

population = []
for ind in range(individual_per_pop):
    new_guy = NeuralNetwork()
    population.append(new_guy)

def select_parents(population, fitness, num_parents):
    parents = []
    for parent in range(num_parents):
        max_idx = fitness.index(max(fitness))
        parents.append(population[max_idx])
        fitness[max_idx] = -1
    return parents

def give_babies(parents, num_babies):
    babies = []
    for i in range(num_babies):
        baby = NeuralNetwork()
        baby.wts[0] = (parents[i%num_parents].wts[0] + parents[(i+1)%num_parents].wts[0])/2
        babies.append(baby)
    return babies

def mutation(babies):
    for baby in range(num_babies):
        babies[baby].wts[0] = random.uniform(-10,10)
    return babies

