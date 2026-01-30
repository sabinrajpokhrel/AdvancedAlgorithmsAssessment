"""
Question 5 - Emergency Network Simulator: Graph Data Structure

Problem Overview:
This module implements the core graph data structure for the Emergency Communication
& Response Network. The graph represents cities (nodes) connected by roads (edges)
where each edge has a weight representing distance, cost, or travel time.

Approach:
I used an adjacency list representation for the graph because it provides efficient
storage for sparse networks and allows fast neighbor lookups. The graph supports:
- Dynamic node and edge addition/removal
- Node failure simulation (disabled nodes)
- Vulnerable edge marking (for routing avoidance)
- Active subgraph queries (excluding failures)

The implementation maintains three key data structures:
1. graph: adjacency list {city: [(neighbor, weight), ...]}
2. vulnerable_edges: set of edges marked as at-risk
3. disabled_nodes: set of cities currently offline (for failure simulation)
"""


class EmergencyGraph:
    """
    Represents the Emergency Communication & Response Network
    using a weighted, undirected graph implemented as an adjacency list.

    - Nodes represent cities / hubs
    - Edges represent roads with associated cost or time
    """

    def __init__(self):
        # Adjacency list storing graph structure.
        # Format: {city: [(neighbor, weight), ...]}
        # This allows O(1) neighbor lookup and O(degree) iteration.
        self.graph = {}

        # Stores edges marked as vulnerable for routing decisions.
        # Format: {(city1, city2), (city2, city1)} - bidirectional
        self.vulnerable_edges = set()

        # Stores nodes currently disabled for failure simulation.
        # Disabled nodes are excluded from path computations.
        self.disabled_nodes = set()

    # Node (City / Hub) Operations

    def add_city(self, city):
        """
        Adds a new city (node) to the network.
        This operation is idempotent - adding existing city has no effect.
        """
        if city not in self.graph:
            self.graph[city] = []

    def remove_city(self, city):
        """
        Removes a city and all associated roads from the network.
        Also cleans up the city from neighbor adjacency lists.
        """
        if city in self.graph:
            # Remove all roads connected to this city from neighbors' lists.
            for neighbor, _ in self.graph[city]:
                self.graph[neighbor] = [
                    (n, w) for (n, w) in self.graph[neighbor] if n != city
                ]
            del self.graph[city]
            self.disabled_nodes.discard(city)

    def disable_city(self, city):
        """
        Disables a city to simulate node failure.
        Disabled cities are excluded from pathfinding but remain in graph.
        """
        if city in self.graph:
            self.disabled_nodes.add(city)

    def enable_city(self, city):
        """
        Re-enables a previously disabled city.
        This restores the city for routing operations.
        """
        self.disabled_nodes.discard(city)


    # Edge (Road) Operations
    
    def add_road(self, city1, city2, weight):
        """
        Adds a bidirectional road between two cities with a given weight.
        Creates cities if they don't exist (convenience feature).
        """
        if city1 not in self.graph:
            self.add_city(city1)
        if city2 not in self.graph:
            self.add_city(city2)

        self.graph[city1].append((city2, weight))
        self.graph[city2].append((city1, weight))

    def remove_road(self, city1, city2):
        """
        Removes the bidirectional road between two cities.
        Also removes vulnerable marking if present.
        """
        if city1 in self.graph and city2 in self.graph:
            self.graph[city1] = [
                (n, w) for (n, w) in self.graph[city1] if n != city2
            ]
            self.graph[city2] = [
                (n, w) for (n, w) in self.graph[city2] if n != city1
            ]

            self.vulnerable_edges.discard((city1, city2))
            self.vulnerable_edges.discard((city2, city1))

    def mark_vulnerable_road(self, city1, city2):
        """
        Marks a road as vulnerable (to be avoided in routing).
        Used for disaster-prone routes or maintenance planning.
        """
        if city1 in self.graph and city2 in self.graph:
            self.vulnerable_edges.add((city1, city2))
            self.vulnerable_edges.add((city2, city1))

    def is_road_vulnerable(self, city1, city2):
        """
        Checks if a road is marked as vulnerable.
        Returns True if either direction is marked.
        """
        return (city1, city2) in self.vulnerable_edges or (city2, city1) in self.vulnerable_edges

    # Graph Utilities (Used by Algorithms)

    def get_all_cities(self):
        """
        Returns a list of all cities in the network.
        Used by algorithms to iterate over all nodes.
        """
        return list(self.graph.keys())

    def get_all_edges(self):
        """
        Returns a list of all unique edges in the network.
        Format: (city1, city2, weight)
        
        Ensures each edge appears only once (not bidirectionally).
        Used by MST and other edge-based algorithms.
        """
        edges = []
        seen = set()

        for city in self.graph:
            for neighbor, weight in self.graph[city]:
                if (neighbor, city) not in seen:
                    edges.append((city, neighbor, weight))
                    seen.add((city, neighbor))

        return edges

    def get_active_neighbors(self, city):
        """
        Returns neighbors of a city excluding:
        - Disabled cities (simulating failures)
        - Vulnerable roads (for safe routing)
        
        Used by pathfinding algorithms to respect network state.
        """
        neighbors = []

        if city in self.disabled_nodes:
            return neighbors

        for neighbor, weight in self.graph.get(city, []):
            if neighbor not in self.disabled_nodes and (city, neighbor) not in self.vulnerable_edges:
                neighbors.append((neighbor, weight))

        return neighbors

    def get_active_graph(self):
        """
        Returns a filtered adjacency list excluding disabled cities
        and vulnerable roads.
        
        Provides a clean view of operational network for algorithms.
        """
        active_graph = {}

        for city in self.graph:
            if city not in self.disabled_nodes:
                active_graph[city] = self.get_active_neighbors(city)

        return active_graph


"""
Remarks:
- Adjacency list provides O(1) edge addition and O(degree) neighbor iteration.
- Bidirectional edges maintained symmetrically for undirected graph.
- Failure simulation (disabled nodes) allows testing network resilience without modifying structure.
- Vulnerable edge marking enables disaster-aware routing decisions.
- Active graph queries provide clean separation between full graph and operational state.
"""
