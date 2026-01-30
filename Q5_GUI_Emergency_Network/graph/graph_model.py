class EmergencyGraph:
    """
    Represents the Emergency Communication & Response Network
    using a weighted, undirected graph implemented as an adjacency list.

    - Nodes represent cities / hubs
    - Edges represent roads with associated cost or time
    """

    def __init__(self):
        # Adjacency list:
        # {
        #   'A': [('B', 4), ('C', 2)],
        #   'B': [('A', 4)]
        # }
        self.graph = {}

        # Stores edges that are marked as vulnerable
        # Format: {('A', 'B'), ('B', 'A')}
        self.vulnerable_edges = set()

        # Stores nodes that are currently disabled (failure simulation)
        self.disabled_nodes = set()

    # Node (City / Hub) Operations

    def add_city(self, city):
        """
        Adds a new city (node) to the network.
        """
        if city not in self.graph:
            self.graph[city] = []

    def remove_city(self, city):
        """
        Removes a city and all associated roads from the network.
        """
        if city in self.graph:
            # Remove all roads connected to this city
            for neighbor, _ in self.graph[city]:
                self.graph[neighbor] = [
                    (n, w) for (n, w) in self.graph[neighbor] if n != city
                ]
            del self.graph[city]
            self.disabled_nodes.discard(city)

    def disable_city(self, city):
        """
        Disables a city to simulate node failure.
        """
        if city in self.graph:
            self.disabled_nodes.add(city)

    def enable_city(self, city):
        """
        Re-enables a previously disabled city.
        """
        self.disabled_nodes.discard(city)


    # Edge (Road) Operations
    
    def add_road(self, city1, city2, weight):
        """
        Adds a bidirectional road between two cities with a given weight.
        """
        if city1 not in self.graph:
            self.add_city(city1)
        if city2 not in self.graph:
            self.add_city(city2)

        self.graph[city1].append((city2, weight))
        self.graph[city2].append((city1, weight))

    def remove_road(self, city1, city2):
        """
        Removes the road between two cities.
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
        """
        if city1 in self.graph and city2 in self.graph:
            self.vulnerable_edges.add((city1, city2))
            self.vulnerable_edges.add((city2, city1))

    def is_road_vulnerable(self, city1, city2):
        """
        Checks if a road is marked as vulnerable.
        """
        return (city1, city2) in self.vulnerable_edges or (city2, city1) in self.vulnerable_edges

    # Graph Utilities (Used by Algorithms)

    def get_all_cities(self):
        """
        Returns a list of all cities in the network.
        """
        return list(self.graph.keys())

    def get_all_edges(self):
        """
        Returns a list of all unique edges in the network.
        Format: (city1, city2, weight)
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
        - Disabled cities
        - Vulnerable roads
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
        """
        active_graph = {}

        for city in self.graph:
            if city not in self.disabled_nodes:
                active_graph[city] = self.get_active_neighbors(city)

        return active_graph
