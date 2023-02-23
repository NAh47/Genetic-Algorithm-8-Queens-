import random
import numpy as np
from matplotlib import pyplot as plt


# generates a random 8 queens configuration
def rand_queens():
  queens = [0] * 8
  for i in range(8):
    queens[i] = random.randint(0, 7)
  return queens


# calculates fitness of given a state, retruns state with fitness value
def fitness(queens):
  fit_val = 0
  for i in range(8):
    for j in range(i + 1, 8):
      if queens[i] == queens[j]:
        fit_val += 1
      if abs(queens[i] - queens[j]) == (abs(i - j)):
        fit_val += 1
  return queens, 28 - fit_val


# selects parent proportional to their fitness value, using roullete
def selection(pop, pop_fit_val):
  total_fitness = sum(pop_fit_val)
  norm_fitness = [f / total_fitness for f in pop_fit_val]
  # Generate a random number between 0 and 1
  r = random.uniform(0, 1)
  # Use Roulette Wheel Selection to choose a parent
  cumulative_fitness = 0
  for i in range(len(pop)):
    cumulative_fitness += norm_fitness[i]
    if cumulative_fitness > r:
      return pop[i]


#given 2 parents, it crossover at a random crossover point
def crossover(parent1, parent2):
  cp = random.randint(1, len(parent1) - 1)
  offspring1 = parent1[:cp] + parent2[cp:]
  offspring2 = parent2[:cp] + parent1[cp:]
  return offspring1, offspring2


# mutates the given 8 queens configuration ata random index for a random value(0-7)
# returns a boolean(to check if solution is found within the given iteration),step count and list of average fitness.
def mutation(queen):
  mp = random.randint(0, 7)
  mv = random.randint(0, 7)
  queen[mp] = mv
  return queen


# runs the GA algorithm for the given iteration
def run(given_iter):
  global population
  global pop_fit
  step = given_iter
  for i in range(pop_size):
    population[i], pop_fit[i] = fitness(rand_queens())
  print("FIRST GENERATION")
  for i in range(pop_size):
    print("STATE : " + str(population[i]) + "  FIT_VAL = " + str(pop_fit[i]))
  count = 0
  average_fit = []
  for steps in range(step):
    for i in range(int(pop_size / 2)):
      q1 = selection(population, pop_fit)
      q2 = selection(population, pop_fit)
      o1, o2 = crossover(q1, q2)
      j = i + int(pop_size / 2)
      offspring[i], offspring_fit[i] = fitness(mutation(o1))
      offspring[j], offspring_fit[j] = fitness(mutation(o2))
    population = offspring
    pop_fit = offspring_fit
    average_fit.append(np.mean(pop_fit))
    count += 1
    if steps%10==0:
      print("GEN : "+str(steps))
    if 28 in pop_fit:
      return True, count, average_fit
  return False, count, average_fit


if __name__ == "__main__":

  iteration = 2000 #Number of generation
  pop_size = 100 #population size per generation
  population = [0] * pop_size
  offspring = [0] * pop_size
  pop_fit = [0] * pop_size
  offspring_fit = [0] * pop_size
  ind = 0
  check, steps_taken, average_fitness = run(iteration)
  if check != False:
    if 28 in pop_fit:
      ind = pop_fit.index(28)
    solution = population[ind]
    sol_fit = pop_fit[ind]
    print("\nSOLUTION FOUND\nNUMBER OF GENERATIONS TAKEN: " + str(steps_taken))
    print("SOLUTION STATE: " + str(solution) + " Fitness :" + str(sol_fit))
  else:
    print("NO SOLUTION FOUND WITHIN THE GIVEN ITERATION/POPULATION SIZE")
  plt.plot(range(0, steps_taken), average_fitness)
  plt.xlabel("Generations taken")
  plt.ylabel("Average Fitness")
  plt.show()
