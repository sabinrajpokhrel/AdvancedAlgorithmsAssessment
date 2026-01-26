import math
import random

def generate_cities(n, lower = 0, upper = 1000):
    return [(random.uniform(lower, upper), random.uniform(lower, upper)) for _ in range(n)]

def distance(city1, city2):
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)

def total_distance(route, cities):
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1)%len(route)]])
    return dist


#swapping two cities for new route
def swap_neighbor(route):
    new_route = route[:]
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def acceptance_probability(old_cost, new_cost, temperature):
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) /temperature)

def exponential_cooling(T, alpha = 0.995):
    return T * alpha

def linear_cooling(T, beta = 0.1):
    return T - beta

def simulated_annealing(cities, T_initial, cooling_type, max_iter):
    n = len(cities)
    current_route = list(range(n))
    random.shuffle(current_route)
    
    current_cost = total_distance(current_route, cities)
    best_route = current_route[:]
    best_cost = current_cost
    
    T = T_initial
    
    for i in range(max_iter):
        new_route = swap_neighbor(current_route)
        new_cost = total_distance(new_route, cities)
        
        if random.random() < acceptance_probability(current_cost, new_cost, T):
            current_route = new_route
            current_cost = new_cost
            
        if current_cost < best_cost:
            best_route = current_route
            best_cost = current_cost
            
        #cooling
        if cooling_type == 'exponential':
            T = exponential_cooling(T)
        elif cooling_type == 'linear':
            T = linear_cooling(T)
        
        #Stopping condition
        if T <= 1e-6:
            break
    return best_route, best_cost


# Example Usage
cities = generate_cities(30)

route_exp, cost_exp = simulated_annealing(
    cities,
    T_initial = 1000,
    cooling_type = "exponential",
    max_iter = 10000
    
)

route_lin, cost_lin = simulated_annealing(
    cities,
    T_initial = 1000,
    cooling_type = "linear",
    max_iter = 10000
    
)

print("Exponential Cooling Distance:", round(cost_exp, 2))
print("Linear Cooling Distance: ", round(cost_lin, 2))
    