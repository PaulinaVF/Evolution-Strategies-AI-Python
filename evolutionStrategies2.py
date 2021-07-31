# Paulina Vara Figueroa
# Evolution Strategies are algorithms which imitate the principles of natural
# evolution as a method to solve parameter optimization problems.
# 1 - A floating point number representation is used
# 2 - The mutation is the most important operation
# 3 - The selection is a elitist process
#
# This version's changes are:
# 1 - Limits are established so that the normal value doesn't take the individuals out of range
# 2 - The end of the algorithm isn't controlled by a number of iterations, but by the lack of improvement on the maximum fitness value
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
newPopulation = [] # Guarda la población que se genera a través de mutación y cruza
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
        population.append(float(rnd.uniform(aInterval, bInterval)))

def getFitness (testedPopulation): # Evalua el fitnes de la población que reciba y devuelve una lista con dicho fitness.
    thisFitness = []
    for individual in testedPopulation:
        currentFitness = individual*mt.sin(10*mt.pi*individual)+1.0 # Función fitness actual
        thisFitness.append(currentFitness)
    return thisFitness

def createNewIndividuals ():
    global population, mutRate, popSize, newIndiv_n, newPopulation, sigma, aInterval, bInterval
    selectedForMut = int(mt.ceil(newIndiv_n*mutRate)) # Redondea hacia arriba los individuos a tratar por mutación
    selectedForCross = (newIndiv_n - selectedForMut)*2 # El resto de individuos se obtienen por cruza para
                                                        # evitar cambios en tamaño de la población
    newPopulation = []
    # Mutación:
    for index in range(selectedForMut):
        selectedIndividual = rnd.randrange(0,popSize)
        normalDistValue = float(np.random.lognormal(0,sigma,1))
        # Mutar con la desviación estandar:
        newValue = population[selectedIndividual] + normalDistValue
        # Limitar el resultado para que no salga de rango:
        if (newValue < aInterval):
            newValue = aInterval
        elif (newValue > bInterval):
            newValue = bInterval
        newPopulation.append(newValue)

    #Crossover:
    for index in range(selectedForCross):
        selectedIndividual1 = rnd.randrange(0, popSize)
        selectedIndividual2 = rnd.randrange(0, popSize)
        newValue = (population[selectedIndividual1]+population[selectedIndividual2])/2
        newPopulation.append(newValue)

def selection ():
    global fitness, newFitness, popSize, population
    selectedIndividuals = []
    combinedFitness = []
    combinedFitness.extend(fitness)
    combinedFitness.extend(newFitness)
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
improveCounter = 0 # Cuenta el número de veces que el fitness máximo no mejora
originalSigma = sigma # Guarda la sigma original para no perderla por las modificaciones
counterFilled = False
lastcounterFilled = False
continueLooking = True
while(continueLooking):
    fitness = getFitness(population).copy()

    i += 1
    tempPromFit = sum(fitness) / popSize
    promFitness.append(tempPromFit)
    indIteracion.append(i)

    if (i == 1):
        max_previo = max(fitness)

    createNewIndividuals()
    newFitness = getFitness(newPopulation).copy()
    selection()
    iterations -= 1

    # Se obtiene el fitness máximo para poder compararlo con el anterior
    max_ind = fitness.index(max(fitness))
    max_actual = fitness[max_ind]

    if (max_actual <= max_previo):
        improveCounter += 1
    else:
        max_previo = max_actual
        sigma = originalSigma
        improveCounter = 0
        counterFilled = False
        lastcounterFilled = False

    if (improveCounter == 200 and not counterFilled and not lastcounterFilled):
        sigma = originalSigma * 2
        counterFilled = True
        improveCounter = 0
    elif (improveCounter == 200 and counterFilled and not lastcounterFilled):
        sigma = originalSigma / 2
        lastcounterFilled = True
        improveCounter = 0
    elif (improveCounter == 200 and lastcounterFilled):
        continueLooking = False


max_ind = fitness.index(max(fitness))
print('Valor máximo: ' + str(fitness[max_ind]) + ' | En posición: ' + str(max_ind))
print('Valor x : ' + str(population[max_ind]))
plt.plot(indIteracion, promFitness, "#8A2BE2") #Se utiliza la herramienta plot para graficar mandando nuestros valores x & y
plt.grid()

plt.title('Estrategias Evolutivas')
plt.xlabel('Iteración')
plt.ylabel('Promedio Fitness')

plt.show()