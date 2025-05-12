import random
import copy
import matplotlib.pyplot as plt
import math

#P decides the size of population
P = 50
#N decides the length of the gene
N = 20
#MIN decides the minimum value a part of the gene can be
MIN = -2.048
#MAX decides the max value a part of the gene can be
MAX = 2.048
#MUTRATE is the probability a mutation will occur within part of a gene during the mutation stage
MUTRATE = 1 / N
#MAXGEN decides the number of generations to be ran
MAXGEN = 50
#MUTSTEP decides the amount of change to occur should a mutation occur (e.g. + or - the MUTSTEP from the gene value)
MUTSTEP = 0.1

#Initialises the arrays
population = []
offspring = []
genAvgFitness = []
genBestFitness = []

#Class to create the individuals of the population and initialise them with an empty gene and 0 fitness
class individual:
    def __init__(self):
        self.gene = [0]*N
        self.fitness = 0

#Test function to use function 1 from the assignment
def test_function(ind):
    fitness = 0
    for i in range(N-1):
        x = ind.gene[i]
        x1 = ind.gene[i+1]
        fitness = fitness + (100*(math.pow((x1-math.pow(x, 2)), 2)))+math.pow((1-x),2)
    return fitness

#Function which simply prints the fitness of the population
def print_pop_fitness(population):
    fitness = 0
    for i in range(0, P):
        fitness += population[i].fitness
    print(fitness)

#Function which fills the population with actual values for their gene and fitness
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

#Function in which offspring are selected based on their fitness, simply selects two random parents and chooses the parent with the higher fitness
#for the offspring
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

#Function in which crossover occurs, selects crosspoint randomly each time in range of N and applies crossover
#from that point between two individuals in the offspring then returns the offspring array with the updated values
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

#Function in which mutation occurs depending on whether or not the randomly generated mutprob is lower than the MUTRATE,
#if the mutation would take the gene value over the MAX or MIN it simply keeps the gene at the MAX or MIN value
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

#Function which updates the fitness of the new population after selection, crossover and mutation has been applied
def evaluate(population):
    for i in range(0, P):
        population[i].fitness = test_function(population[i])
    return population

#Function to store the current populations fitness and update the best fitness where appropriate, will be used to plot the graph
def store_current_fitness(population, genAvgFitness, genBestFitness):
    currentFitness = 0
    if not genBestFitness:
        bestFitness = 1000000000000000000
    else:
        bestFitness = genBestFitness[-1]
        
    for i in range(0, P):
        currentFitness += population[i].fitness
        if(population[i].fitness < bestFitness):
            bestFitness = population[i].fitness
    currentFitness = currentFitness / P
    genAvgFitness.append(currentFitness)
    genBestFitness.append(bestFitness)
    


#Here the population is filled with its beginning values and the fitness is stored
population = fill_population(population)
store_current_fitness(population, genAvgFitness, genBestFitness)
print_pop_fitness(population)

#Loop which runs the GA MAXGEN amount of times
for i in range(MAXGEN):
    offspring = selection(population) #Selects offspring
    offspring = crossover(offspring) #Performs crossover on the offspring
    offspring = mutation(offspring) #Mutates offspring and stores mutated values into population
    population = copy.deepcopy(offspring) #Copies offspring into population
    population = evaluate(population) #Stores fitness of new population
    store_current_fitness(population, genAvgFitness, genBestFitness) #Stores current gen fitness in an array
    print_pop_fitness(population) #Just prints current pop fitness
print("Final Population Fitness:")
print_pop_fitness(population)

#Plots the graph using the stored average and best fitnesses
plt.plot(genAvgFitness, label="Average Generation Fitness")
plt.plot(genBestFitness, label="Generation Best Fitness")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness Over the Generations.")
plt.legend()
plt.show()



