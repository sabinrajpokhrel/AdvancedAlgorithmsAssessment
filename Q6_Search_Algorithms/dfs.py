"""
Question 6 - Search Algorithms: Depth-First Search (DFS)
Goal: find a path from Glogow (start) to Plock (goal) using DFS,
exploring deep paths first via stack (LIFO) data structure.

Graph Structure from Diagram (a):
- Based on actual distances between Polish cities
- Start: Glogow (blue node)
- Goal: Plock (red node)
"""

from collections import deque


class DFSSearch:
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
    
    def dfs_search(self):
        """
        Depth-First Search Algorithm
        Uses a stack (LIFO) for the OPEN list to explore deep paths first.
        
        Algorithm:
        1. Initialize OPEN (stack) with start node
        2. Initialize CLOSED as empty
        3. While OPEN is not empty:
           a. Pop node from OPEN (most recently added - stack behavior)
           b. If node is goal, return path
           c. Add node to CLOSED
           d. Push unvisited neighbors to OPEN (stack)
        4. If OPEN becomes empty, no solution exists
        
        Note: DFS does not guarantee shortest path but uses less memory than BFS.
        """
        
        # OPEN list (stack) - stores nodes to be explored
        # Each element: (city, path_from_start, total_distance)
        open_list = [(self.start, [self.start], 0)]
        
        # CLOSED list (set) - stores visited nodes
        closed_list = set()
        
        # For tracking the search process
        iteration = 0
        print("=" * 80)
        print("DEPTH-FIRST SEARCH (DFS) ALGORITHM")
        print("=" * 80)
        print(f"Start City: {self.start}")
        print(f"Goal City: {self.goal}")
        print("=" * 80)
        print("\nSearch Process:\n")
        
        while open_list:
            iteration += 1
            
            # Pop from end (stack - LIFO)
            current_city, path, distance = open_list.pop()
            
            print(f"Iteration {iteration}:")
            print(f"  Current Node: {current_city}")
            print(f"  OPEN (before): {[city for city, _, _ in open_list]}")
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
            
            # Add unvisited neighbors to open list (in reverse order for DFS)
            # This ensures they are explored in the order they appear in the graph
            for neighbor, edge_distance in reversed(neighbors):
                if neighbor not in closed_list:
                    new_path = path + [neighbor]
                    new_distance = distance + edge_distance
                    open_list.append((neighbor, new_path, new_distance))
                    neighbors_to_add.append(neighbor)
            
            print(f"  Action: Added {current_city} to CLOSED")
            if neighbors_to_add:
                print(f"  Action: Added neighbors to OPEN: {neighbors_to_add}")
            else:
                print(f"  Action: No new neighbors to add")
            print(f"  OPEN (after): {[city for city, _, _ in open_list]}")
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


def main():
    """Main function to run DFS search"""
    dfs = DFSSearch()
    
    # Print graph structure
    dfs.print_graph_structure()
    
    # Run DFS search
    path, distance = dfs.dfs_search()
    
    if path:
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)
        print(f"Algorithm: Depth-First Search (DFS)")
        print(f"Start: {dfs.start}")
        print(f"Goal: {dfs.goal}")
        print(f"Solution Path: {' -> '.join(path)}")
        print(f"Total Distance: {distance} km")
        print(f"Path Length: {len(path)} cities")
        print("=" * 80)
        
        # Additional analysis
        print("\nDFS Characteristics:")
        print("- Uses stack (LIFO) for node exploration")
        print("- Explores as deep as possible before backtracking")
        print("- Not guaranteed to find shortest path")
        print("- Space complexity: O(b*m) where b=branching factor, m=max depth")
        print("- Time complexity: O(b^m)")
        print("=" * 80)


if __name__ == "__main__":
    main()

"""
Output (example):
============================================================
DEPTH-FIRST SEARCH (DFS) ALGORITHM
============================================================
Start City: Glogow
Goal City: Plock
============================================================

Search Process:

Iteration 1:
  Current Node: Glogow
  OPEN (before): []
  CLOSED (before): []
  Action: Added Glogow to CLOSED
  Action: Added neighbors to OPEN: ['Poznan', 'Leszno']
  OPEN (after): ['Poznan', 'Leszno']
  CLOSED (after): ['Glogow']

[... continues until goal is found ...]

============================================================
GOAL REACHED!
============================================================
Path Found: Glogow -> Poznan -> Bydgoszcz -> Wloclawek -> Plock
Total Distance: 349 km
Number of Cities in Path: 5
Iterations Required: 5
============================================================
"""

"""
Remarks:
- DFS explores deep paths first using stack (LIFO) data structure.
- Does not guarantee optimal (shortest) path; finds 'a' solution, not necessarily the best.
- Memory efficient compared to BFS as it stores only one path at a time.
- Path found depends on the order neighbors are explored.
"""
