import random
import copy
import matplotlib.pyplot as plt
import math


P = 50
N = 10
MIN = -5.12
MAX = 5.12
MUTRATE = 1 / N
MAXGEN = 50
MUTSTEP = 0.1

population = []
offspring = []
genAvgFitness = []
genBestFitness = []

class individual:
    def __init__(self):
        self.gene = [0]*N
        self.fitness = 0

# def test_function(ind):
#     utility = 0
#     for i in range(N):
#         utility = utility + ind.gene[i]
#     return utility

#Test function to use rastigrin function
def test_function(ind):
    fitness = 0
    for i in range(N):
        x = ind.gene[i]
        fitness = fitness + ((x * x) - 10*(math.cos((2*math.pi)*(x))))
    fitness = fitness + (10*N)
    return fitness

def print_pop_fitness(population):
    fitness = 0
    for i in range(0, P):
        fitness += population[i].fitness
    print(fitness)


def fill_population(population):
    for x in range(0, P):
        tempgene = []
        for y in range (0, N):
            tempgene.append(random.uniform(MIN, MAX))
        newind = individual()
        newind.gene = tempgene.copy()
        newind.fitness = test_function(newind)
        population.append(newind)
    return population

def selection(population):
    offspring = []
    for i in range(0, P):
        parent1 = random.randint(0, P-1)
        off1 = copy.deepcopy(population[parent1])
        parent2 = random.randint(0, P-1)
        off2 = copy.deepcopy(population[parent2])
        if off1.fitness < off2.fitness:
            offspring.append(off1)
        else:
            offspring.append(off2)
    return offspring

def crossover(offspring):
    toff1 = individual()
    toff2 = individual()
    temp = individual()
    for i in range(0, P, 2):
        toff1 = copy.deepcopy(offspring[i])
        toff2 = copy.deepcopy(offspring[i+1])
        temp = copy.deepcopy(offspring[i])
        crosspoint = random.randint(1, N)
        for j in range(crosspoint, N):
            toff1.gene[j] = toff2.gene[j]
            toff2.gene[j] = temp.gene[j]
        offspring[i] = copy.deepcopy(toff1)
        offspring[i+1] = copy.deepcopy(toff2)
    return offspring

def mutation(offspring):
    newOff = []
    for i in range(0, P):
        newind = individual()
        newind.gene = []
        for j in range(0, N):
            gene = offspring[i].gene[j]
            mutprob = random.random()
            if(mutprob < MUTRATE):
                alter = random.uniform(-MUTSTEP, MUTSTEP)
                gene = gene + alter
                if gene > MAX:
                    gene = MAX
                if gene < MIN:
                    gene = MIN
            newind.gene.append(gene)
        newOff.append(newind)
    return newOff

def evaluate(population):
    for i in range(0, P):
        population[i].fitness = test_function(population[i])
    return population

def store_current_fitness(population, genAvgFitness, genBestFitness):
    currentFitness = 0
    if not genBestFitness:
        bestFitness = 10000
    else:
        bestFitness = genBestFitness[-1]
        
    for i in range(0, P):
        currentFitness += population[i].fitness
        if(population[i].fitness < bestFitness):
            bestFitness = population[i].fitness
    currentFitness = currentFitness / P
    genAvgFitness.append(currentFitness)
    genBestFitness.append(bestFitness)
    



population = fill_population(population)
store_current_fitness(population, genAvgFitness, genBestFitness)
print_pop_fitness(population)

for i in range(MAXGEN):
    offspring = selection(population) #selects offspring
    offspring = crossover(offspring) #performs crossover on the offspring
    offspring = mutation(offspring) #mutates offspring and stores mutated values into population
    population = copy.deepcopy(offspring) #copies offspring into population
    population = evaluate(population) #stores fitness of new population
    store_current_fitness(population, genAvgFitness, genBestFitness) #Stores current gen fitness in an array
    print_pop_fitness(population) #Just prints current pop fitness
print("Final Population Fitness:")
print_pop_fitness(population)

#plots graph
plt.plot(genAvgFitness, label="Average Generation Fitness")
plt.plot(genBestFitness, label="Generation Best Fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness Over the Generations.")
plt.legend()
plt.show()



