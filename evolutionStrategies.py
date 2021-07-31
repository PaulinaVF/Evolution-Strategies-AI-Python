# Paulina Vara Figueroa
# Evolution Strategies are algorithms which imitate the principles of natural
# evolution as a method to solve parameter optimization problems.
# 1 - A floating point number representation is used
# 2 - The mutation is the most important operation
# 3 - The selection is a elitist process
import random as rnd
import math as mt
import numpy as np
import matplotlib.pyplot as plt

popSize = 0 # Tamaño de la población
newIndiv_n = 0 # Nuevos individuos a generar
mutRate = 0 # Fracción de individuos para mutación
fitness = [] # Fitness de la población
newFitness = [] # Fitness de la nueva población
population = [] # Población
newPopulation = [] #Guarda la población que se genera a través de mutación y cruza
aInterval = -1
bInterval = 2
sigma = 1 #Desviación estándar

# Primero se solicitan los datos que necesita el algoritmo para trabajar:
popSize = int(input('Tamaño de la población: '))
newIndiv_n = int(input('Cantidad de nuevos individuos: '))
mutRate = float(input('Fracción de individuos generados por mutación: '))
crossRate = 1 - mutRate
print('La fracción de individuos generados por cruza será: ' + str(crossRate))

# Se crean las funciones que van a ayudar a seguir el algoritmo
def createInitialPop (): # Crea de manera aleatoria la población inicial
    global popSize, population, aInterval, bInterval
    for ind in range(popSize):
        thisIndividual = []
        thisIndividual.append(float(rnd.uniform(aInterval, bInterval))) # Elige individuos aleatorios dentro del rango
        thisIndividual.append(int(1))
        population.append(thisIndividual) # El individuo consta del valor decimal y un valor de distrib. normal
    print(population)

def getFitness (testedPopulation): # Evalua el fitnes de la población que reciba y devuelve una lista con dicho fitness.
    thisFitness = []
    for individual in testedPopulation:
        currentFitness = individual[0]*mt.sin(10*mt.pi*individual[0])+1.0 # Función fitness actual
        thisFitness.append(currentFitness)
    #print(thisFitness)
    return thisFitness

def createNewIndividuals ():
    global population, mutRate, popSize, newIndiv_n, newPopulation, sigma
    selectedForMut = int(mt.ceil(newIndiv_n*mutRate)) # Redondea hacia arriba los individuos a tratar por mutación
    selectedForCross = (newIndiv_n - selectedForMut)*2 # El resto de individuos se obtienen por cruza para
                                                        # evitar cambios en tamaño de la población
    newPopulation = []
    # Mutación:
    for index in range(selectedForMut):
        selectedIndividual = rnd.randrange(0,popSize)
       # normalDistValue = mt.sqrt(-2*mt.log(rnd.uniform(0,1),mt.e))*mt.cos(2*mt.pi*rnd.uniform(0,1))
        normalDistValue = float(np.random.lognormal(0,sigma,1))
        # Cambiar desviación estandar
        print('NORMAL::: ')
        print(normalDistValue)
        newValue = population[selectedIndividual][0] + normalDistValue
        newIndividual = []
        newIndividual.append(newValue)
        newIndividual.append(int(1))
        newPopulation.append(newIndividual)

    #Crossover:
    for index in range(selectedForCross):
        selectedIndividual1 = rnd.randrange(0,popSize)
        selectedIndividual2 = rnd.randrange(0, popSize)
        newValue = (population[selectedIndividual1][0]+population[selectedIndividual2][0])/2
        newIndividual = []
        newIndividual.append(newValue)
        newIndividual.append(int(1))
        newPopulation.append(newIndividual)

def selection ():
    global fitness, newFitness, popSize, population
    selectedIndividuals = []
    combinedFitness = []
    combinedFitness.extend(fitness)
    combinedFitness.extend(newFitness)
    print(combinedFitness)
    for index in range(popSize):
        maxPosition = combinedFitness.index(max(combinedFitness))
        if (maxPosition >= len(fitness)):
            selectedIndividuals.append(newPopulation[maxPosition-len(fitness)])
        else:
            selectedIndividuals.append(population[maxPosition])
        combinedFitness[maxPosition] = -1000
    population = []
    population = selectedIndividuals.copy()

# Siguiendo el algoritmo de Estrategias Evolutivas:
createInitialPop()

iterations = 100
i = 0
promFitness = []
indIteracion = []

while(iterations > 0):
    i += 1
    tempPromFit = sum(fitness) / popSize
    promFitness.append(tempPromFit)
    indIteracion.append(i)
    fitness = getFitness(population).copy()
    createNewIndividuals()
    newFitness = getFitness(newPopulation).copy()
    selection()
    print('New pop: ')
    print(population)
    iterations -= 1

max_ind = fitness.index(max(fitness))
print('Valor máximo: ' + str(fitness[max_ind]) + ' | En posición: ' + str(max_ind))
plt.plot(indIteracion, promFitness, "#FFD700") #Se utiliza la herramienta plot para graficar mandando nuestros valores x & y
plt.grid()

plt.title('Estrategias Evolutivas')
plt.xlabel('Iteración')
plt.ylabel('Promedio Fitness')

plt.show()