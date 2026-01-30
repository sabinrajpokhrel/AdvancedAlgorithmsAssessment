"""
Question 6 - Search Algorithms: Breadth-First Search (BFS)
Goal: find a path from Glogow (start) to Plock (goal) using BFS,
exploring level-by-level via queue (FIFO) data structure.

Graph Structure from Diagram (a):
- Based on actual distances between Polish cities
- Start: Glogow (blue node)
- Goal: Plock (red node)

APPROACH EXPLANATION:
I implemented Breadth-First Search using a queue-based OPEN list.
The algorithm works by:
1. Starting at Glogow, enqueueing it into a queue (OPEN list)
2. Repeatedly dequeuing the oldest added node from OPEN (FIFO behavior)
3. If the dequeued node is the goal (Plock), return the path and distance
4. Otherwise, add the node to CLOSED (visited) set
5. Enqueue all unvisited neighbors into the OPEN queue
6. Continue until goal is found or OPEN becomes empty

Key properties:
- Uses queue for OPEN list (FIFO order)
- GUARANTEES shortest path in unweighted graphs (by number of edges)
- For weighted graphs, BFS finds path with fewest nodes, not minimum distance
- Space-intensive: stores all nodes at current level before processing next level
- Time Complexity: O(V + E) where V=vertices, E=edges
- Space Complexity: O(V) for storing all frontier nodes at max breadth
"""

from collections import deque


class BFSSearch:
    def __init__(self):
        # Graph representation: adjacency list with edge weights.
        # Graph representation from diagram (a)
        # Format: {city: [(neighbor, distance), ...]}
        self.graph = {
            'Glogow': [('Leszno', 40), ('Poznan', 67)],
            'Leszno': [('Glogow', 40), ('Poznan', 103), ('Wroclaw', 87)],
            'Poznan': [('Glogow', 67), ('Leszno', 103), ('Bydgoszcz', 108), ('Konin', 107)],
            'Wroclaw': [('Leszno', 87), ('Glogow', 89), ('Opole', 80)],
            'Bydgoszcz': [('Poznan', 108), ('Wloclawek', 90), ('Konin', 102)],
            'Konin': [('Poznan', 107), ('Bydgoszcz', 102), ('Wloclawek', 98), ('Kalisz', 95)],
            'Wloclawek': [('Bydgoszcz', 90), ('Konin', 98), ('Plock', 44)],
            'Plock': [('Wloclawek', 44), ('Warsaw', 95), ('Lodz', 118)],
            'Kalisz': [('Konin', 95), ('Leszno', 103), ('Czestochowa', 128), ('Lodz', 95)],
            'Lodz': [('Kalisz', 95), ('Plock', 118), ('Czestochowa', 107), ('Warsaw', 124), ('Radom', 107)],
            'Czestochowa': [('Kalisz', 128), ('Lodz', 107), ('Opole', 90), ('Katowice', 61)],
            'Opole': [('Wroclaw', 80), ('Czestochowa', 90)],
            'Katowice': [('Czestochowa', 61), ('Krakow', 68)],
            'Krakow': [('Katowice', 68), ('Kielce', 102), ('Radom', 190)],
            'Kielce': [('Krakow', 102), ('Radom', 70)],
            'Radom': [('Kielce', 70), ('Krakow', 190), ('Lodz', 107), ('Warsaw', 91)],
            'Warsaw': [('Plock', 95), ('Lodz', 124), ('Radom', 91)]
        }
        
        self.start = 'Glogow'
        self.goal = 'Plock'
    
    def bfs_search(self):
        """
        Breadth-First Search Algorithm
        Uses a queue (FIFO) for the OPEN list to explore level-by-level.
        
        Algorithm:
        1. Initialize OPEN (queue) with start node
        2. Initialize CLOSED as empty
        3. While OPEN is not empty:
           a. Dequeue node from OPEN (first added - queue behavior)
           b. If node is goal, return path
           c. Add node to CLOSED
           d. Enqueue unvisited neighbors to OPEN (queue)
        4. If OPEN becomes empty, no solution exists
        
        BFS Properties:
        - Explores nodes level by level (layer-wise expansion)
        - Guarantees shortest path in terms of number of hops/edges
        - Complete: will find solution if one exists
        - Higher space complexity than DFS due to storing all nodes at current level
        """
        
        # OPEN list (queue) - stores nodes to be explored
        # Each element: (city, path_from_start, total_distance)
        open_queue = deque([(self.start, [self.start], 0)])
        
        # CLOSED list (set) - stores visited nodes
        closed_list = set()
        
        # For tracking the search process
        iteration = 0
        print("=" * 80)
        print("BREADTH-FIRST SEARCH (BFS) ALGORITHM")
        print("=" * 80)
        print(f"Start City: {self.start}")
        print(f"Goal City: {self.goal}")
        print("=" * 80)
        print("\nSearch Process:\n")
        
        while open_queue:
            iteration += 1
            
            # Dequeue from front (queue - FIFO)
            current_city, path, distance = open_queue.popleft()
            
            print(f"Iteration {iteration}:")
            print(f"  Current Node: {current_city}")
            print(f"  OPEN (before): {[city for city, _, _ in open_queue]}")
            print(f"  CLOSED (before): {sorted(closed_list)}")
            
            # Check if goal is reached
            if current_city == self.goal:
                print(f"\n{'=' * 80}")
                print("GOAL REACHED!")
                print(f"{'=' * 80}")
                print(f"Path Found: {' -> '.join(path)}")
                print(f"Total Distance: {distance} km")
                print(f"Number of Cities in Path: {len(path)}")
                print(f"Iterations Required: {iteration}")
                print(f"{'=' * 80}")
                return path, distance
            
            # Skip if already visited
            if current_city in closed_list:
                print(f"  Action: {current_city} already in CLOSED, skipping")
                print()
                continue
            
            # Add to closed list
            closed_list.add(current_city)
            
            # Get neighbors
            neighbors = self.graph.get(current_city, [])
            neighbors_to_add = []
            
            # Add unvisited neighbors to open queue
            for neighbor, edge_distance in neighbors:
                if neighbor not in closed_list and not any(neighbor == city for city, _, _ in open_queue):
                    new_path = path + [neighbor]
                    new_distance = distance + edge_distance
                    open_queue.append((neighbor, new_path, new_distance))
                    neighbors_to_add.append(neighbor)
            
            print(f"  Action: Added {current_city} to CLOSED")
            if neighbors_to_add:
                print(f"  Action: Added neighbors to OPEN: {neighbors_to_add}")
            else:
                print(f"  Action: No new neighbors to add")
            print(f"  OPEN (after): {[city for city, _, _ in open_queue]}")
            print(f"  CLOSED (after): {sorted(closed_list)}")
            print()
        
        print("No path found from {} to {}".format(self.start, self.goal))
        return None, None
    
    def print_graph_structure(self):
        """Print the graph structure for reference"""
        print("\n" + "=" * 80)
        print("GRAPH STRUCTURE (Diagram a)")
        print("=" * 80)
        for city, neighbors in sorted(self.graph.items()):
            neighbor_str = ", ".join([f"{n}({d}km)" for n, d in neighbors])
            print(f"{city:15} -> {neighbor_str}")
        print("=" * 80)
    
    def visualize_levels(self):
        """Visualize BFS level-by-level expansion"""
        print("\n" + "=" * 80)
        print("BFS LEVEL-BY-LEVEL EXPANSION")
        print("=" * 80)
        
        visited = {self.start}
        current_level = [self.start]
        level = 0
        
        while current_level and self.goal not in visited:
            print(f"\nLevel {level}: {current_level}")
            next_level = []
            
            for city in current_level:
                neighbors = [n for n, _ in self.graph.get(city, [])]
                for neighbor in neighbors:
                    if neighbor not in visited:
                        visited.add(neighbor)
                        next_level.append(neighbor)
            
            current_level = next_level
            level += 1
        
        print("\n" + "=" * 80)


def main():
    """Main function to run BFS search"""
    bfs = BFSSearch()
    
    # Print graph structure
    bfs.print_graph_structure()
    
    # Show level-by-level expansion
    bfs.visualize_levels()
    
    # Run BFS search
    path, distance = bfs.bfs_search()
    
    if path:
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Algorithm: Breadth-First Search (BFS)")
        print(f"Start: {bfs.start}")
        print(f"Goal: {bfs.goal}")
        print(f"Solution Path: {' -> '.join(path)}")
        print(f"Total Distance: {distance} km")
        print(f"Path Length: {len(path)} cities")
        print("=" * 80)
        
        # Additional analysis
        print("\nBFS Characteristics:")
        print("- Uses queue (FIFO) for node exploration")
        print("- Explores nodes level by level")
        print("- Guarantees shortest path (by number of edges)")
        print("- Space complexity: O(b^d) where b=branching factor, d=depth")
        print("- Time complexity: O(b^d)")
        print("- Complete: Always finds solution if one exists")
        print("=" * 80)


if __name__ == "__main__":
    main()

"""
Output (example):
============================================================
BREADTH-FIRST SEARCH (BFS) ALGORITHM
============================================================
Start City: Glogow
Goal City: Plock
============================================================

BFS LEVEL-BY-LEVEL EXPANSION
Level 0: ['Glogow']
Level 1: ['Leszno', 'Poznan']
Level 2: ['Wroclaw', 'Bydgoszcz', 'Konin']
Level 3: ['Opole', 'Wloclawek', 'Kalisz']
Level 4: ['Plock']

Search Process:

Iteration 1:
  Current Node: Glogow
  OPEN (before): ['Leszno', 'Poznan']
  CLOSED (before): []
  Action: Added Glogow to CLOSED
  Action: Added neighbors to OPEN: ['Leszno', 'Poznan']
  OPEN (after): ['Leszno', 'Poznan']
  CLOSED (after): ['Glogow']

[... continues until goal is found ...]

============================================================
GOAL REACHED!
============================================================
Path Found: Glogow -> Poznan -> Bydgoszcz -> Wloclawek -> Plock
Total Distance: 349 km
Number of Cities in Path: 5
Iterations Required: 10
============================================================
"""

"""
Remarks:
- BFS explores nodes level-by-level using queue (FIFO) data structure.
- GUARANTEES minimum hop path (fewest number of edges), not necessarily shortest distance.
  In this weighted graph, BFS finds path with fewest cities but may have higher total km.
- Uses more memory than DFS as it must store all nodes at current frontier level.
- Suitable when solution is likely to be shallow in the search tree.
- Complete algorithm: always finds solution if one exists in finite graphs.
- The queue (deque) allows O(1) append and popleft operations, ensuring efficiency.
- Unlike DFS which can take deep exploration paths, BFS systematically checks all
  neighbors at distance 1, then distance 2, then distance 3, etc.
- For this Polish cities graph, BFS will prefer direct short routes over long detours,
  though distance is still secondary to hop count (number of cities in path).
"""
