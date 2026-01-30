"""
Graph Coloring Algorithm - RAW Implementation
Assigns frequencies/channels to network hubs such that no adjacent hubs
use the same frequency (Chromatic Number problem).

Uses greedy coloring with Welsh-Powell heuristic for better results.
"""


def greedy_graph_coloring(graph):
    """
    Assigns colors to graph nodes using greedy algorithm.
    No adjacent nodes receive the same color.
    
    Algorithm: Welsh-Powell Heuristic
    1. Order vertices by degree (highest first)
    2. Assign smallest available color to each vertex
    3. Ensure no adjacent vertex has same color
    
    Time Complexity: O(V^2 + E) in worst case
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): The network
    
    Returns:
        coloring: Dictionary mapping node -> color (integer)
        chromatic_number: Minimum colors needed
    """
    
    all_cities = graph.get_all_cities()
    
    if not all_cities:
        return {}, 0
    
    # Step 1: Sort vertices by degree (descending)
    degree_list = []
    for city in all_cities:
        neighbors = graph.get_active_neighbors(city)
        degree = len(neighbors)
        degree_list.append((degree, city))
    
    # Sort by degree descending (Welsh-Powell heuristic)
    degree_list.sort(reverse=True)
    
    # Step 2: Initialize coloring
    coloring = {}
    
    # Step 3: Assign colors
    for _, city in degree_list:
        # Find all colors used by adjacent vertices
        used_colors = set()
        neighbors = graph.get_active_neighbors(city)
        
        for neighbor, _ in neighbors:
            if neighbor in coloring:
                used_colors.add(coloring[neighbor])
        
        # Find minimum available color
        color = 0
        while color in used_colors:
            color += 1
        
        coloring[city] = color
    
    # Calculate chromatic number
    chromatic_number = max(coloring.values()) + 1 if coloring else 0
    
    return coloring, chromatic_number


def validate_coloring(graph, coloring):
    """
    Validates that a coloring is valid (no adjacent nodes same color).
    
    Time Complexity: O(V + E)
    Space Complexity: O(1)
    
    Parameters:
        graph (EmergencyGraph): The network
        coloring: Dictionary mapping node -> color
    
    Returns:
        is_valid: Boolean indicating if coloring is valid
        violations: List of edges with same color endpoints
    """
    
    violations = []
    
    for city in graph.get_all_cities():
        if city not in coloring:
            continue
        
        neighbors = graph.get_active_neighbors(city)
        city_color = coloring[city]
        
        for neighbor, _ in neighbors:
            if neighbor in coloring and coloring[neighbor] == city_color:
                # Found a violation
                if (neighbor, city) not in violations:  # Avoid duplicates
                    violations.append((city, neighbor))
    
    return len(violations) == 0, violations


def find_maximum_independent_set(graph):
    """
    Finds largest set of non-adjacent vertices.
    Useful for finding maximum hubs that can use same frequency.
    
    Algorithm: Greedy approach (not guaranteed optimal)
    
    Time Complexity: O(V^2 + E)
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): The network
    
    Returns:
        independent_set: Set of nodes with no edges between them
    """
    
    all_cities = graph.get_all_cities()
    remaining = set(all_cities)
    independent_set = []
    
    # Sort by degree for better results
    degree_list = []
    for city in remaining:
        neighbors = graph.get_active_neighbors(city)
        degree = len(neighbors)
        degree_list.append((degree, city))
    
    degree_list.sort()  # Sort by degree ascending
    
    for _, city in degree_list:
        if city in remaining:
            independent_set.append(city)
            
            # Remove this node and all its neighbors from remaining
            remaining.discard(city)
            neighbors = graph.get_active_neighbors(city)
            for neighbor, _ in neighbors:
                remaining.discard(neighbor)
    
    return independent_set


def color_to_frequency(color):
    """
    Maps color index to communication frequency (for visualization).
    
    Parameters:
        color: Color index (0, 1, 2, ...)
    
    Returns:
        frequency: Frequency band name or value
    """
    
    frequency_bands = {
        0: "Band A (2.4 GHz)",
        1: "Band B (5 GHz)",
        2: "Band C (6 GHz)",
        3: "Band D (28 GHz)",
        4: "Band E (39 GHz)",
    }
    
    return frequency_bands.get(color, f"Band {chr(65 + color)} ({color * 100} MHz)")


def analyze_coloring_efficiency(graph, coloring):
    """
    Analyzes efficiency of a coloring solution.
    
    Parameters:
        graph (EmergencyGraph): The network
        coloring: Dictionary mapping node -> color
    
    Returns:
        analysis: Dictionary with efficiency metrics
    """
    
    analysis = {
        'chromatic_number': max(coloring.values()) + 1 if coloring else 0,
        'colors_used': len(set(coloring.values())),
        'average_degree': 0,
        'max_degree': 0,
        'theoretical_minimum': 0,
        'efficiency': 0  # How close to theoretical minimum
    }
    
    all_cities = graph.get_all_cities()
    degrees = []
    
    for city in all_cities:
        neighbors = graph.get_active_neighbors(city)
        degree = len(neighbors)
        degrees.append(degree)
    
    if degrees:
        analysis['average_degree'] = sum(degrees) / len(degrees)
        analysis['max_degree'] = max(degrees)
        
        # Brooks' theorem: chromatic number <= max_degree + 1 (except for cliques)
        analysis['theoretical_minimum'] = max(degrees) if max(degrees) > 1 else 1
        
        if analysis['theoretical_minimum'] > 0:
            analysis['efficiency'] = (analysis['theoretical_minimum'] / 
                                     analysis['chromatic_number']) * 100
    
    return analysis


def multi_coloring_heuristics(graph):
    """
    Tries multiple coloring heuristics and returns best result.
    
    Time Complexity: O(k * (V^2 + E)) where k = number of heuristics
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): The network
    
    Returns:
        best_coloring: Best coloring found
        best_chromatic: Chromatic number of best coloring
        all_results: Results from all heuristics
    """
    
    all_results = {}
    
    # Heuristic 1: Greedy by degree (Welsh-Powell)
    coloring1, chromatic1 = greedy_graph_coloring(graph)
    all_results['Welsh-Powell'] = (coloring1, chromatic1)
    
    # Heuristic 2: Random order greedy (simplified - just reverse order)
    all_cities = list(reversed(graph.get_all_cities()))
    coloring2 = {}
    
    for city in all_cities:
        used_colors = set()
        neighbors = graph.get_active_neighbors(city)
        
        for neighbor, _ in neighbors:
            if neighbor in coloring2:
                used_colors.add(coloring2[neighbor])
        
        color = 0
        while color in used_colors:
            color += 1
        coloring2[city] = color
    
    chromatic2 = max(coloring2.values()) + 1 if coloring2 else 0
    all_results['Reverse-Order'] = (coloring2, chromatic2)
    
    # Find best
    best_chromatic = float('inf')
    best_coloring = None
    
    for heuristic, (coloring, chromatic) in all_results.items():
        if chromatic < best_chromatic:
            best_chromatic = chromatic
            best_coloring = coloring
    
    return best_coloring, best_chromatic, all_results
