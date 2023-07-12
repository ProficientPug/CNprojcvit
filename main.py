import csv
import random
import folium
from deap import base, creator, tools, algorithms

# Define the Problem
creator.create("FitnessMax", base.Fitness, weights=(1.0,))
creator.create("Individual", list, fitness=creator.FitnessMax)

# Data Preparation
airports = {'LHR':[51.4700, 0.4543, 81.73],'EWR':[40.6895, 74.1745, 8.72]}
link_delay = 50  # ms
dataset = r'X:\New folder\Cn-project\Data_rate.csv'
datarate = r'X:\New folder\Cn-project\Data_rate.csv'
# Reading data from CSV files
def read_coordinates_from_csv(dataset):
    coordinates = []
    with open(dataset, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            lat = float(row["Latitude"])
            lon = float(row["Longitude"])
            alt = float(row["Altitude"])
            coordinates.append((lat, lon, alt))
    return coordinates

def read_data_from_csv(datarate):
    data = []
    with open(r'X:\New folder\Cn-project\Data_rate.csv', "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            mode = row["mode"]
            mode_color = row["mode color"]
            switching_threshold = float(row["switching threshold"])
            data_rate = float(row["data rate"])
            data.append((mode, mode_color, switching_threshold, data_rate))
    return data

coordinates = read_coordinates_from_csv(r'X:\New folder\Cn-project\dataset.csv')
data = read_data_from_csv(r'X:\New folder\Cn-project\Data_rate.csv')

# Model Formulation: this is still a work under progress
def evaluate(induvidual):
    
    data_rates = []
    for path in induvidual:
        data_rate  = genetic_sorting(path)
        data_rates.append(data_rate)
    
    # Return the sum of data rates as the fitness value
    return data_rates

def genetic_sorting(datarate_file):
    
# Read the data rate transmission file
    with open(r'X:\New folder\Cn-project\dataset.csv', "r") as f:
        reader = csv.reader(f)
        data_rate_transmission = []
        for row in reader:
            data_rate_transmission.append({
            "color": row[0],
            "range": [int(row[1]), int(row[2])]
        })

# Initialize the population
    population = []
    for _ in range(len(data_rate_transmission)):
        population.append([data_rate_transmission[_]])

    while True:

    # Select two parents from the population
        parents = random.sample(population, 2)
    # Create a child
        child = []
        for i in range(len(parents[0])):
            if random.random() > 0.5:
                child.append(parents[0][i])
            else:
                child.append(parents[1][i])

        if random.random() > 0.5:
            child[random.randint(0, len(child) - 1)] = random.randint(0, len(data_rate_transmission) - 1)
            child_fitness = fitness(child)
        if child_fitness > population[-1][1]:
            population[-1] = [child, child_fitness]
        if population[0][1] == population[-1][1]:
            break
    return sorted(population, key=lambda x: x[1])
def fitness(induvidual):
    fitness = 0
    for data_rate_transmission in induvidual:
        fitness += (data_rate_transmission["range"][1] - data_rate_transmission["range"][0])
    return fitness


# Optimization Algorithm Selection
toolbox = base.Toolbox()
toolbox.register("induvidual", tools.initRepeat, creator.Individual, n=len(coordinates))
toolbox.register("population", tools.initRepeat, list, toolbox.induvidual)
toolbox.register("evaluate", evaluate)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.05)
toolbox.register("select", tools.selTournament, tournsize=3)

# Main Optimization Loop
def main():
    population_size = 150
    generations = 100
    population = toolbox.population
    
    for gen in range(generations):
        offspring = algorithms.varAnd(population, toolbox, cxpb=0.5, mutpb=0.1)
        
        fits = toolbox.map(toolbox.evaluate, offspring)
        for fit, ind in zip(fits, offspring):
            ind.fitness.values = fit
        
        population = offspring
    
    best_individual = tools.selBest(population, k=1)[0]
    best_data_rate = evaluate(best_individual)[0]
    
    print("Best Individual:", best_individual)
    print("Best Data Rate:", best_data_rate)

if __name__ == "__main__":
    main()
