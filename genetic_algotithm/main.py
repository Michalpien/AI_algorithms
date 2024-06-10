from random import randint, sample
import numpy as np


def get_paths_50():
    paths = []
    for j in range(50):
        if j < 40:
            paths.append((j, j+10))
        if (j - 9) % 10 != 0:
            paths.append((j, j+1))

    return paths


def f(x, price, paths, pen_mult):

    all_price = sum(price * x)
    penalty = 0
    for path in paths:
        if not x[path[0]] and not x[path[1]]:
            penalty += 1
    result = all_price + penalty * pen_mult
    return result


def selection(population, price, paths, pen_mult):
    new_population = []
    for _ in population:
        individuals = sample(population, 2)
        f1 = f(individuals[0], price, paths, pen_mult)
        f2 = f(individuals[1], price, paths, pen_mult)
        if f1 < f2:
            new_population.append(individuals[0])
        else:
            new_population.append(individuals[1])

    return new_population


def get_start_population(size, indyviduals_number):
    length = len(indyviduals_number)
    return [[randint(0, 1) for _ in range(size)] for _ in range(length)]


def mutate(population):
    mutated_population = []
    for indyvidual in population:
        draw = randint(0, 100)
        if draw < 80:
            mutated_indyvidual = []
            for feature in indyvidual:
                draw = randint(0, 100)
                elem_to_add = feature ^ 1 if draw < 20 else feature
                mutated_indyvidual.append(elem_to_add)
            mutated_population.append(mutated_indyvidual)
        else:
            mutated_population.append(indyvidual)

    return mutated_population


def get_best(population, price, paths, pen_mult):
    values = [(f(ele, price, paths, pen_mult), ele) for ele in population]
    values.sort(key=lambda x: x[0])
    return values[0]


def genetical_algorithm(iter, price, pen_mult, population,
                        paths, maximal_cost=None):
    best = get_best(population, price, paths, pen_mult)
    if maximal_cost:
        while best[0] > maximal_cost:
            new_pop = selection(population, price, paths, pen_mult)
            mut_pop = mutate(new_pop)
            if get_best(population, price, paths, pen_mult)[0] < best[0]:
                best = get_best(population, price, paths, pen_mult)
            population = mut_pop
    else:
        for _ in range(iter):
            new_pop = selection(population, price, paths, pen_mult)
            mut_pop = mutate(new_pop)
            if get_best(population, price, paths, pen_mult)[0] < best[0]:
                best = get_best(population, price, paths, pen_mult)
            population = mut_pop

    return best


def print_city(indyvidual):
    printed_list = []
    for char in indyvidual:
        if char == 0:
            printed_list.append('0')
        else:
            printed_list.append(f'\033[93m{1}\033[0m')

    for i in range(5):
        for j in range(10):
            print(f'{printed_list[10*i+j]} ', end='')
        print()


def standard_deviation(data):
    average = sum(data) / len(data)
    deviations_sum = 0
    for element in data:
        deviations_sum += (element - average) ** 2
    deviation = np.sqrt(deviations_sum / (len(data) - 1))
    return deviation


if __name__ == "__main__":
    population = get_start_population(5, 50)  # test for 5 places
    paths = [(0, 1), (1, 2), (2, 3), (0, 4)]

    best = genetical_algorithm(2000, 20, 20, population, paths)
