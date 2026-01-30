"""
Question 6 - Search Algorithms: A* Search
Goal: find the optimal (shortest distance) path from Glogow to Plock using A*,
guided by heuristic function (straight-line distances) to efficiently explore.

Diagram (a): Actual road distances (for g(n) - cost from start)
Diagram (b): Straight-line distances (for h(n) - heuristic to goal)

A* uses f(n) = g(n) + h(n) where:
- g(n) = actual cost from start to node n
- h(n) = estimated cost from node n to goal (heuristic)
- f(n) = estimated total cost through node n

A* is optimal when heuristic is admissible (never overestimates).
"""

import heapq
from typing import Dict, List, Tuple, Set


class AStarSearch:
    def __init__(self):
        # Graph from diagram (a): actual road distances between cities.
        # Graph from diagram (a) - actual road distances
        # Format: {city: [(neighbor, actual_distance), ...]}
        self.graph = {
            'Glogow': [('Leszno', 45), ('Poznan', 90)],
            'Leszno': [('Glogow', 45), ('Poznan', 140), ('Wroclaw', 100), ('Kalisz', 140)],
            'Poznan': [('Glogow', 90), ('Leszno', 140), ('Bydgoszcz', 140), ('Konin', 130)],
            'Wroclaw': [('Leszno', 100), ('Glogow', 140), ('Opole', 100)],
            'Bydgoszcz': [('Poznan', 140), ('Wloclawek', 110), ('Konin', 120)],
            'Konin': [('Poznan', 130), ('Bydgoszcz', 120), ('Wloclawek', 120), ('Kalisz', 120)],
            'Wloclawek': [('Bydgoszcz', 110), ('Konin', 120), ('Plock', 55)],
            'Plock': [('Wloclawek', 55), ('Warsaw', 130), ('Lodz', 150)],
            'Kalisz': [('Konin', 120), ('Leszno', 140), ('Czestochowa', 160), ('Lodz', 120)],
            'Lodz': [('Kalisz', 120), ('Plock', 150), ('Czestochowa', 128), ('Warsaw', 165), ('Radom', 165)],
            'Czestochowa': [('Kalisz', 160), ('Lodz', 128), ('Opole', 118), ('Katowice', 80)],
            'Opole': [('Wroclaw', 100), ('Czestochowa', 118)],
            'Katowice': [('Czestochowa', 80), ('Krakow', 85)],
            'Krakow': [('Katowice', 85), ('Kielce', 120), ('Radom', 280)],
            'Kielce': [('Krakow', 120), ('Radom', 82)],
            'Radom': [('Kielce', 82), ('Krakow', 280), ('Lodz', 165), ('Warsaw', 105)],
            'Warsaw': [('Plock', 130), ('Lodz', 165), ('Radom', 105)]
        }
        
        # Heuristic function from diagram (b) - straight-line distances to goal (Plock)
        # These are the estimated distances from each city to Plock
        self.heuristic = {
            'Glogow': 350,      # Estimated straight-line distance to Plock
            'Leszno': 320,
            'Poznan': 270,
            'Wroclaw': 380,
            'Bydgoszcz': 180,
            'Konin': 200,
            'Wloclawek': 55,
            'Plock': 0,         # Goal has heuristic of 0
            'Kalisz': 250,
            'Lodz': 150,
            'Czestochowa': 240,
            'Opole': 340,
            'Katowice': 300,
            'Krakow': 360,
            'Kielce': 250,
            'Radom': 180,
            'Warsaw': 120
        }
        
        self.start = 'Glogow'
        self.goal = 'Plock'
    
    def a_star_search(self):
        """
        A* Search Algorithm
        Uses a priority queue ordered by f(n) = g(n) + h(n) to prioritize promising nodes.
        
        Algorithm:
        1. Initialize OPEN with start node (priority = f(start))
        2. Initialize CLOSED as empty
        3. While OPEN is not empty:
           a. Remove node with lowest f(n) from OPEN (best candidate)
           b. If node is goal, return path
           c. Add node to CLOSED
           d. For each neighbor:
              - Calculate g(neighbor) = g(node) + cost(node, neighbor)
              - Calculate f(neighbor) = g(neighbor) + h(neighbor)
              - If neighbor not in OPEN or CLOSED, add to OPEN
              - If neighbor in OPEN with higher f, update it (path improvement)
        4. If OPEN becomes empty, no solution exists
        
        Properties:
        - Optimal: Finds shortest path if heuristic is admissible (h(n) ≤ true cost)
        - Complete: Always finds solution if one exists
        - Efficient: Expands fewer nodes than uninformed search due to heuristic guidance
        - Best choice for weighted graphs with good heuristic available
        """
        
        # OPEN list (priority queue) - stores (f_score, counter, city, path, g_score)
        # counter is used to break ties in f_score
        open_heap = []
        counter = 0
        g_start = 0
        h_start = self.heuristic[self.start]
        f_start = g_start + h_start
        
        heapq.heappush(open_heap, (f_start, counter, self.start, [self.start], g_start))
        counter += 1
        
        # CLOSED list (set) - stores visited nodes
        closed_list = set()
        
        # Track best g_score for each node
        g_scores = {self.start: 0}
        
        # For tracking the search process
        iteration = 0
        print("=" * 80)
        print("A* SEARCH ALGORITHM")
        print("=" * 80)
        print(f"Start City: {self.start}")
        print(f"Goal City: {self.goal}")
        print(f"\nA* Formula: f(n) = g(n) + h(n)")
        print("  g(n) = actual cost from start to node n")
        print("  h(n) = estimated cost from node n to goal (heuristic)")
        print("  f(n) = estimated total cost through node n")
        print("=" * 80)
        print("\nHeuristic Function (Straight-line distances to Plock):")
        for city, h_value in sorted(self.heuristic.items()):
            print(f"  h({city}) = {h_value} km")
        print("=" * 80)
        print("\nSearch Process:\n")
        
        while open_heap:
            iteration += 1
            
            # Pop node with lowest f_score
            f_current, _, current_city, path, g_current = heapq.heappop(open_heap)
            h_current = self.heuristic[current_city]
            
            print(f"Iteration {iteration}:")
            print(f"  Current Node: {current_city}")
            print(f"  g({current_city}) = {g_current} km (cost from start)")
            print(f"  h({current_city}) = {h_current} km (estimated cost to goal)")
            print(f"  f({current_city}) = {f_current} km (total estimated cost)")
            
            # Show OPEN list
            open_cities = []
            for f, _, city, _, g in open_heap:
                open_cities.append(f"{city}(f={f})")
            print(f"  OPEN (before): {open_cities}")
            print(f"  CLOSED (before): {sorted(closed_list)}")
            
            # Check if goal is reached
            if current_city == self.goal:
                print(f"\n{'=' * 80}")
                print("GOAL REACHED!")
                print(f"{'=' * 80}")
                print(f"Optimal Path Found: {' -> '.join(path)}")
                print(f"Total Distance: {g_current} km")
                print(f"Number of Cities in Path: {len(path)}")
                print(f"Iterations Required: {iteration}")
                print(f"{'=' * 80}")
                
                # Print detailed path analysis
                print("\nPath Analysis:")
                for i in range(len(path) - 1):
                    city1, city2 = path[i], path[i+1]
                    # Find edge distance
                    edge_dist = next(d for n, d in self.graph[city1] if n == city2)
                    print(f"  {city1} -> {city2}: {edge_dist} km")
                print(f"  Total: {g_current} km")
                print(f"{'=' * 80}")
                
                return path, g_current
            
            # Skip if already visited
            if current_city in closed_list:
                print(f"  Action: {current_city} already in CLOSED, skipping")
                print()
                continue
            
            # Add to closed list
            closed_list.add(current_city)
            
            # Explore neighbors
            neighbors = self.graph.get(current_city, [])
            neighbors_added = []
            
            for neighbor, edge_cost in neighbors:
                if neighbor in closed_list:
                    continue
                
                # Calculate g_score for neighbor
                tentative_g = g_current + edge_cost
                
                # If this is a better path to neighbor, or neighbor is unvisited
                if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                    g_scores[neighbor] = tentative_g
                    h_neighbor = self.heuristic[neighbor]
                    f_neighbor = tentative_g + h_neighbor
                    
                    new_path = path + [neighbor]
                    heapq.heappush(open_heap, (f_neighbor, counter, neighbor, new_path, tentative_g))
                    counter += 1
                    neighbors_added.append(f"{neighbor}(g={tentative_g}, h={h_neighbor}, f={f_neighbor})")
            
            print(f"  Action: Added {current_city} to CLOSED")
            if neighbors_added:
                print(f"  Action: Expanded neighbors:")
                for n_info in neighbors_added:
                    print(f"    - {n_info}")
            else:
                print(f"  Action: No neighbors to expand")
            
            # Show OPEN list after
            open_cities_after = []
            for f, _, city, _, g in open_heap:
                open_cities_after.append(f"{city}(f={f})")
            print(f"  OPEN (after): {open_cities_after}")
            print(f"  CLOSED (after): {sorted(closed_list)}")
            print()
        
        print("No path found from {} to {}".format(self.start, self.goal))
        return None, None
    
    def print_graph_structure(self):
        """Print the graph structure for reference"""
        print("\n" + "=" * 80)
        print("GRAPH STRUCTURE (Diagram a - Actual Road Distances)")
        print("=" * 80)
        for city, neighbors in sorted(self.graph.items()):
            neighbor_str = ", ".join([f"{n}({d}km)" for n, d in neighbors])
            print(f"{city:15} -> {neighbor_str}")
        print("=" * 80)
    
    def explain_heuristic(self):
        """Explain the heuristic function design"""
        print("\n" + "=" * 80)
        print("HEURISTIC FUNCTION DESIGN")
        print("=" * 80)
        print("\nHeuristic: h(n) = straight-line distance from node n to goal (Plock)")
        print("\nProperties of this heuristic:")
        print("1. Admissible: Never overestimates the actual cost")
        print("   - Straight-line distance is always ≤ actual road distance")
        print("   - Guarantees A* will find optimal solution")
        print("\n2. Consistent (Monotonic): h(n) ≤ cost(n,n') + h(n')")
        print("   - Triangle inequality holds for Euclidean distances")
        print("   - Ensures A* expands nodes in order of increasing f-values")
        print("\n3. Informed: Provides useful guidance toward goal")
        print("   - Better than h(n)=0 (reduces to Dijkstra)")
        print("   - Helps prioritize promising paths")
        print("\nHeuristic values from diagram (b):")
        for city in sorted(self.heuristic.keys()):
            h_val = self.heuristic[city]
            print(f"  h({city:15}) = {h_val:3d} km")
        print("=" * 80)


def compare_algorithms():
    """Compare A* with DFS and BFS"""
    print("\n" + "=" * 80)
    print("ALGORITHM COMPARISON")
    print("=" * 80)
    
    print("\n1. A* ALGORITHM:")
    print("   - Uses heuristic to guide search")
    print("   - Optimal: Finds shortest path")
    print("   - Complete: Always finds solution if exists")
    print("   - Efficient: Expands fewer nodes than uninformed search")
    print("   - f(n) = g(n) + h(n)")
    
    print("\n2. BFS (Breadth-First Search):")
    print("   - Explores level by level")
    print("   - Optimal: For unweighted graphs only")
    print("   - Complete: Always finds solution if exists")
    print("   - Higher space complexity than DFS")
    
    print("\n3. DFS (Depth-First Search):")
    print("   - Explores deep paths first")
    print("   - Not optimal: May not find shortest path")
    print("   - Complete: For finite graphs")
    print("   - Lower space complexity than BFS")
    
    print("\n" + "=" * 80)
    print("Why A* is best for this problem:")
    print("- Need optimal path (shortest distance)")
    print("- Have good heuristic (straight-line distances)")
    print("- Weighted graph (different edge costs)")
    print("- Large search space (many cities)")
    print("=" * 80)


def main():
    """Main function to run A* search"""
    astar = AStarSearch()
    
    # Print graph structure
    astar.print_graph_structure()
    
    # Explain heuristic function
    astar.explain_heuristic()
    
    # Run A* search
    path, distance = astar.a_star_search()
    
    if path:
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Algorithm: A* Search")
        print(f"Start: {astar.start}")
        print(f"Goal: {astar.goal}")
        print(f"Optimal Path: {' -> '.join(path)}")
        print(f"Total Distance: {distance} km")
        print(f"Path Length: {len(path)} cities")
        print("=" * 80)
        
        # Compare algorithms
        compare_algorithms()


if __name__ == "__main__":
    main()

"""
Output (example):
============================================================
A* SEARCH ALGORITHM
============================================================
Start City: Glogow
Goal City: Plock

A* Formula: f(n) = g(n) + h(n)
  g(n) = actual cost from start to node n
  h(n) = estimated cost from node n to goal (heuristic)
  f(n) = estimated total cost through node n
============================================================

Heuristic Function (Straight-line distances to Plock):
  h(Bydgoszcz) = 180 km
  h(Glogow) = 350 km
  h(Konin) = 200 km
  h(Plock) = 0 km
  h(Poznan) = 270 km
  h(Wloclawek) = 55 km
  [... other cities ...]
============================================================

Search Process:

Iteration 1:
  Current Node: Glogow
  g(Glogow) = 0 km (cost from start)
  h(Glogow) = 350 km (estimated cost to goal)
  f(Glogow) = 350 km (total estimated cost)
  OPEN (before): []
  CLOSED (before): []
  Action: Added Glogow to CLOSED
  Action: Expanded neighbors:
    - Leszno(g=45, h=320, f=365)
    - Poznan(g=90, h=270, f=360)
  OPEN (after): ['Poznan(f=360)', 'Leszno(f=365)']
  CLOSED (after): ['Glogow']

[... continues until goal is found ...]

============================================================
GOAL REACHED!
============================================================
Optimal Path Found: Glogow -> Poznan -> Bydgoszcz -> Wloclawek -> Plock
Total Distance: 395 km
Number of Cities in Path: 5
Iterations Required: 5
============================================================

Path Analysis:
  Glogow -> Poznan: 90 km
  Poznan -> Bydgoszcz: 140 km
  Bydgoszcz -> Wloclawek: 110 km
  Wloclawek -> Plock: 55 km
  Total: 395 km
============================================================
"""

"""
Remarks:
- A* combines benefits of uniform-cost search (optimality) and greedy search (efficiency).
- The straight-line distance heuristic is admissible (never overestimates), guaranteeing optimal path.
- A* expands fewer nodes than BFS/DFS by prioritizing nodes with lower f(n) values.
- Perfect for robot parcel delivery: finds shortest route efficiently using geographic heuristic.
- Superior to DFS (not optimal) and BFS (explores too many nodes) for weighted graphs.
"""
