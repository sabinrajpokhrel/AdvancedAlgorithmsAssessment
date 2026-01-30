"""
Question 1(a) - Optimizing Sensor Placement for Data Collection
Goal: find a hub position (hub_x, hub_y) that minimizes the total
sum of Euclidean distances to all given sensor coordinates.
"""

import math

def euclidean_distance(x1, y1, x2, y2):
    # Core utility to measure signal attenuation between two points.
    return math.sqrt((x2-x1)**2 + (y2-y1)**2)

def geometric_median(sensor_locations, epsilon = 1e-6, max_iter = 1000):
    # Weiszfeld's algorithm: converges to the geometric median for L2 distance.
    # Initial guess: centroid (fast, stable starting point).
    x = sum(p[0] for p in sensor_locations) / len(sensor_locations)
    y = sum(p[1] for p in sensor_locations) / len(sensor_locations)
    
    for _ in range(max_iter):
        num_x = 0
        num_y = 0
        denom = 0
        
        for xi, yi in sensor_locations:
            d = euclidean_distance(x, y, xi, yi)
            if d == 0:
                continue
            num_x += xi/d
            num_y += yi / d
            denom += 1/d
            
        new_x = num_x / denom
        new_y = num_y / denom
        
        # Stopping condition: tiny movement means convergence.
        if euclidean_distance(x, y, new_x, new_y) < epsilon:
            break
        x, y = new_x, new_y
        
    return x, y

def total_distance(hub_x, hub_y, sensor_locations):
    # Objective function: total distance from hub to all sensors.
    return sum(
        euclidean_distance(hub_x, hub_y, xi, yi)
        for xi, yi in sensor_locations
    )
    

# Example Usage
sensor_locations = [(0, 1), (1, 0), (1, 2), (2, 1)]

hub_x, hub_y = geometric_median(sensor_locations)
min_distance = total_distance(hub_x, hub_y, sensor_locations)

print("Optimal Hub Location:", (round(hub_x, 5), round(hub_y, 5)))
print("Minimum total distance:", round(min_distance, 5))

"""
Output (example):
Optimal Hub Location: (1.0, 1.0)
Minimum total distance: 4.0
"""

"""
Remarks:
- The optimal hub is the geometric median, not necessarily the centroid.
- Small floating-point variations are expected due to iterative convergence.
"""
    