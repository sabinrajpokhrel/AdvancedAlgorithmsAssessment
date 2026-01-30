"""
Question 1(a) - Optimizing Sensor Placement for Data Collection
Goal: find a hub position (hub_x, hub_y) that minimizes the total
sum of Euclidean distances to all given sensor coordinates.
"""

"""
APPROACH EXPLANATION:
I used Weiszfeld's iterative algorithm to find the geometric median.
This is done by starting from the centroid, then iteratively updating
the position by computing weighted averages of normalized vectors from
the current point to each sensor. The algorithm converges when movement
becomes negligible (epsilon threshold).
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
    


# Example Usage - Input Case 1
print("=" * 70)
print("INPUT CASE 1: Small 4-sensor grid")
print("=" * 70)
sensor_locations_1 = [(0, 1), (1, 0), (1, 2), (2, 1)]
print(f"Sensors: {sensor_locations_1}")

hub_x_1, hub_y_1 = geometric_median(sensor_locations_1)
min_distance_1 = total_distance(hub_x_1, hub_y_1, sensor_locations_1)

print("Optimal Hub Location:", (round(hub_x_1, 5), round(hub_y_1, 5)))
print("Minimum total distance:", round(min_distance_1, 5))

# Example Usage - Input Case 2
print("\n" + "=" * 70)
print("INPUT CASE 2: Two distant sensors")
print("=" * 70)
sensor_locations_2 = [(1, 1), (3, 3)]
print(f"Sensors: {sensor_locations_2}")

hub_x_2, hub_y_2 = geometric_median(sensor_locations_2)
min_distance_2 = total_distance(hub_x_2, hub_y_2, sensor_locations_2)

print("Optimal Hub Location:", (round(hub_x_2, 5), round(hub_y_2, 5)))
print("Minimum total distance:", round(min_distance_2, 5))

"""
OUTPUT CASE 1 (4-sensor grid):
Optimal Hub Location: (1.0, 1.0)
Minimum total distance: 4.0

OUTPUT CASE 2 (Two distant sensors):
Optimal Hub Location: (2.0, 2.0)
Minimum total distance: 2.82843
"""

"""
REMARKS:
- The optimal hub is the geometric median, not necessarily the centroid.
- For Case 1, the center of the square grid (1,1) minimizes total distance.
- For Case 2 with just two sensors, the optimal point lies on the line segment
  connecting them, specifically at the midpoint (2,2).
- Weiszfeld's algorithm converges quickly for this problem (typically < 100 iterations).
- Small floating-point variations are expected due to iterative convergence with epsilon.
- The algorithm handles edge cases like coincident sensors gracefully by skipping
  distance calculations when d=0.
"""
    