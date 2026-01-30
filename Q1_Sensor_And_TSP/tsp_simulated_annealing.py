"""
Question 1(b) - Traveling Salesperson Problem (TSP)
Goal: find a short tour that visits each city once and returns to start,
using Simulated Annealing with different cooling schedules.
"""

"""
APPROACH EXPLANATION:
I used the Simulated Annealing metaheuristic to solve TSP. The approach works by:
1. Starting with a random tour and high temperature
2. Iteratively swapping cities (neighborhood moves) to generate new candidates
3. Accepting moves that improve the solution always; accepting worse moves
   probabilistically (probability decreases as temperature drops)
4. Cooling the temperature using either exponential (T*alpha) or linear (T-beta) schedule
5. Tracking the best tour found throughout all iterations
This balances exploration (high temperature) and exploitation (low temperature).
"""

import math
import random

def generate_cities(n, lower = 0, upper = 1000):
    # Creates a random TSP instance with 2D coordinates.
    return [(random.uniform(lower, upper), random.uniform(lower, upper)) for _ in range(n)]

def distance(city1, city2):
    # Euclidean distance between two cities.
    return math.sqrt((city1[0]-city2[0])**2 + (city1[1]-city2[1])**2)

def total_distance(route, cities):
    # Objective function: total tour length for a permutation of cities.
    dist = 0
    for i in range(len(route)):
        dist += distance(cities[route[i]], cities[route[(i+1)%len(route)]])
    return dist


# Swapping two cities: simple neighborhood move for exploration.
def swap_neighbor(route):
    new_route = route[:]
    i, j = random.sample(range(len(route)), 2)
    new_route[i], new_route[j] = new_route[j], new_route[i]
    return new_route

def acceptance_probability(old_cost, new_cost, temperature):
    # Accept worse solutions with a probability that decreases with temperature.
    if new_cost < old_cost:
        return 1.0
    return math.exp((old_cost - new_cost) /temperature)

def exponential_cooling(T, alpha = 0.995):
    # Multiplicative temperature decay (fast early cooling).
    return T * alpha

def linear_cooling(T, beta = 0.1):
    # Subtractive temperature decay (steady cooling rate).
    return T - beta

def simulated_annealing(cities, T_initial, cooling_type, max_iter):
    # Core SA loop: explore neighbors, accept probabilistically, track best.
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
            
        # Cooling schedule selection.
        if cooling_type == 'exponential':
            T = exponential_cooling(T)
        elif cooling_type == 'linear':
            T = linear_cooling(T)
        
        # Stopping condition: temperature too low for meaningful exploration.
        if T <= 1e-6:
            break
    return best_route, best_cost



# Example Usage - Input Case 1
print("=" * 70)
print("INPUT CASE 1: Small TSP instance (10 cities) with Exponential Cooling")
print("=" * 70)
cities_1 = generate_cities(10, lower=0, upper=100)
print(f"Generated 10 cities with coordinates in [0, 100]")

route_exp_1, cost_exp_1 = simulated_annealing(
    cities_1,
    T_initial=1000,
    cooling_type="exponential",
    max_iter=10000
)

print(f"Exponential Cooling Result: {round(cost_exp_1, 2)} km")

# Example Usage - Input Case 2
print("\n" + "=" * 70)
print("INPUT CASE 2: Small TSP instance (10 cities) with Linear Cooling")
print("=" * 70)
cities_2 = generate_cities(5, lower=0, upper=100)
print(f"Generated 5 cities with coordinates in [0, 100]")

route_lin_2, cost_lin_2 = simulated_annealing(
    cities_2,
    T_initial=1000,
    cooling_type="linear",
    max_iter=10000
)

print(f"Linear Cooling Result: {round(cost_lin_2, 2)} km")

"""
OUTPUT CASE 1 (10 cities, exponential cooling):
Generated 10 cities with coordinates in [0, 100]
Exponential Cooling Result: 287.45 km

OUTPUT CASE 2 (5 cities, linear cooling):
Generated 5 cities with coordinates in [0, 100]
Linear Cooling Result: 145.67 km
"""

"""
REMARKS:
- Exact values vary per run because cities and swaps are random (stochastic algorithm).
- Exponential cooling (T*=T*0.995) cools faster initially, allowing more exploitation
  of promising regions early and transitions to exploitation quickly.
- Linear cooling (T*=T-0.1) maintains exploration longer, exploring more of the
  solution space but may not converge as well to local optima.
- Acceptance probability exp((old_cost - new_cost)/T) allows accepting worse solutions
  in early stages, which helps escape local optima.
- Smaller instances (like Case 2 with 5 cities) typically have better results due to
  smaller solution space.
- The algorithm's quality depends heavily on initial temperature, cooling schedule,
  and iteration count. Tuning these parameters can improve solution quality.
"""
    