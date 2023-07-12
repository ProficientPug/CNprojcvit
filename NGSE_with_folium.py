import csv
import math
import random
import numpy as np
import folium
from deap import algorithms, base, creator, tools

# Load dataset from CSV file
def load_dataset(data):
    dataset = []
    with open(data, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header
        for row in reader:
            dataset.append(row)
    return dataset

data = r'X:\New folder\Cn-project\dataset.csv'
dataset = load_dataset(data)

latitudes = [float(row[3]) for row in dataset]
longitudes = [float(row[4]) for row in dataset]
altitudes = [float(row[2]) for row in dataset]

# Convert latitude, longitude, and altitude to 3D cartesian coordinates
def convert_to_cartesian(latitudes, longitudes, altitudes):
    cartesian_coords = []
    for lat, lon, alt in zip(latitudes, longitudes, altitudes):
        lat_rad = math.radians(float(lat))
        lon_rad = math.radians(float(lon))
        x = (math.cos(lat_rad) * math.cos(lon_rad)) * float(alt)
        y = (math.cos(lat_rad) * math.sin(lon_rad)) * float(alt)
        z = math.sin(lat_rad) * float(alt)
        cartesian_coords.append((x, y, z))
    return cartesian_coords

coordinates = convert_to_cartesian(latitudes, longitudes, altitudes)

# Calculate Euclidean distance between two points
def distance(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

# Calculate data transmission rate based on distance
def transmission_rate(distance):
    if 0 <= distance <= 5.56:
        return 119.13
    elif 5.56 < distance <= 35:
        return 93.854
    elif 35 < distance <= 90:
        return 77.071
    elif 90 < distance <= 190:
        return 63.937
    elif 190 < distance <= 300:
        return 52.857
    elif 300 < distance <= 400:
        return 43.505
    elif 400 < distance <= 500:
        return 31.895
    else:
        return 0.0

# Calculate end-to-end latency of a routing path
def calculate_latency(path):
    return sum(transmission_rate(distance(path[i], path[i+1])) for i in range(len(path) - 1))

# Calculate end-to-end data transmission rate of a routing path
def calculate_data_rate(path):
    rates = [transmission_rate(distance(path[i], path[i+1])) for i in range(len(path) - 1)]
    valid_rates = [rate for rate in rates if rate is not None]
    if valid_rates:
        return min(valid_rates)
    else:
        # Handle the case when there are no valid rates
        return 0.0  # You can choose an appropriate default value here

# Multi-objective fitness evaluation
def evaluate_multi(path):
    return calculate_data_rate(path), calculate_latency(path)

# Create the routing path individual and population
creator.create("FitnessMin", base.Fitness, weights=(-1.0, -1.0))
creator.create("Individual", list, fitness=creator.FitnessMin)
toolbox = base.Toolbox()
toolbox.register("individual", tools.initRepeat, creator.Individual, lambda: random.choice(coordinates), 3)
toolbox.register("population", tools.initRepeat, list, toolbox.individual)

def mutate(individual, indpb):
    mutated_individual = []
    for element in individual:
        if isinstance(element, tuple):
            mutated_element = tuple(tools.mutGaussian(list(element), mu=0, sigma=1, indpb=indpb))
        else:
            mutated_element = element
        mutated_individual.append(mutated_element)
    return tuple(mutated_individual)
toolbox.register("mutate", mutate, indpb=0.1)
toolbox.register("mate", tools.cxTwoPoint)
toolbox.register("select", tools.selNSGA2)

# Load dataset
dataset = load_dataset(r'X:\New folder\Cn-project\dataset.csv')

# Define problem dimension and bounds
dim = len(dataset)
bounds = [(-180, 180), (-90, 90), (0, 100000)]

# Initialize population
population = toolbox.population(n=100)
# Evaluate fitness
toolbox.register("evaluate", evaluate_multi)
fitnesses = toolbox.map(toolbox.evaluate, population)
for ind, fit in zip(population, fitnesses):
    ind.fitness.values = fit

# Run NSGA-II algorithm
NGEN = 50
CXPB = 0.9
MUTPB = 0.1
for gen in range(NGEN):
    offspring = [toolbox.clone(ind) for ind in population]  # Create offspring with fitness attribute
    # Apply variation operators
    for ind1, ind2 in zip(offspring[::2], offspring[1::2]):
        if random.random() < CXPB:
            toolbox.mate(ind1, ind2)
            del ind1.fitness.values
            del ind2.fitness.values
    for ind in offspring:
        if random.random() < MUTPB:
            toolbox.mutate(ind)
            del ind.fitness.values
    # Evaluate fitness
    fitnesses = toolbox.map(toolbox.evaluate, offspring)
    for ind, fit in zip(offspring, fitnesses):
        ind.fitness.values = fit
    # Select individuals for the next generation
    population = toolbox.select(population + offspring, k=len(population))

# Retrieve the best individual
best_individuals = tools.selBest(population, k=5)
best_individual_indices = [population.index(individual) for individual in best_individuals]
print(best_individual_indices)

# Create a Folium map instance
m = folium.Map()

# Plot airports (Ground Stations)
lhr = [51.4700, 0.4543, 81.73]
ewr = [40.6895, -74.1745, 8.72]
folium.Marker(lhr[:2], popup='LHR (Heathrow Airport)', icon=folium.Icon(color='red')).add_to(m)
folium.Marker(ewr[:2], popup='EWR (Newark Liberty International Airport)', icon=folium.Icon(color='blue')).add_to(m)

# Plot best routing paths
for idx, best_individual_indices_tuple in enumerate(best_individuals):
    best_individual_indices = list(best_individual_indices_tuple)
    routing_path = []
    for i in best_individual_indices:
        if isinstance(i, int) and 0 <= i < len(dataset):
            path = [float(dataset[i][3]), float(dataset[i][4]), float(dataset[i][2])]
            routing_path.append(path)
    if routing_path:
        folium.PolyLine(locations=routing_path, color=f"#{random.randint(0, 0xFFFFFF):06x}", weight=2).add_to(m)

# Display the map
m.fit_bounds(m.get_bounds())
m
