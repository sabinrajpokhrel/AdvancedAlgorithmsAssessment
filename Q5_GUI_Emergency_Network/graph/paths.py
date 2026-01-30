"""
Shortest Path Algorithms - RAW Implementation
No external algorithm libraries are used.

Implements:
1. Dijkstra's Algorithm - O(V^2) for dense graphs
2. Breadth-First Search (BFS) - O(V + E)
3. K-Disjoint Paths using Max Flow approach
"""

from collections import deque
import heapq


def dijkstra_shortest_path(graph, start, end):
    """
    Computes shortest path between two nodes using Dijkstra's algorithm.
    
    Time Complexity: O(V^2) using array, O((V + E) log V) using min-heap
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): Custom graph object
        start: Starting city
        end: Destination city
    
    Returns:
        path: List of cities in shortest path
        distance: Total distance of shortest path
    """
    
    # Initialize distances
    distances = {}
    previous = {}
    unvisited = set()
    
    for city in graph.get_all_cities():
        distances[city] = float('inf')
        previous[city] = None
        unvisited.add(city)
    
    distances[start] = 0
    
    while unvisited:
        # Find unvisited node with minimum distance
        current = None
        min_dist = float('inf')
        
        for city in unvisited:
            if distances[city] < min_dist:
                min_dist = distances[city]
                current = city
        
        if current is None or distances[current] == float('inf'):
            break
        
        if current == end:
            break
        
        unvisited.remove(current)
        
        # Check neighbors
        for neighbor, weight in graph.get_active_neighbors(current):
            if neighbor in unvisited:
                new_distance = distances[current] + weight
                
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    previous[neighbor] = current
    
    # Reconstruct path
    path = []
    current = end
    
    if distances[end] == float('inf'):
        return None, float('inf')  # No path exists
    
    while current is not None:
        path.insert(0, current)
        current = previous[current]
    
    return path, distances[end]


def bfs_shortest_path(graph, start, end):
    """
    Computes shortest path using BFS (unweighted or unit-weighted edges).
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): Custom graph object
        start: Starting city
        end: Destination city
    
    Returns:
        path: List of cities in shortest path
        hops: Number of edges in path
    """
    
    queue = deque([start])
    visited = {start}
    parent = {start: None}
    
    while queue:
        current = queue.popleft()
        
        if current == end:
            # Reconstruct path
            path = []
            node = end
            while node is not None:
                path.insert(0, node)
                node = parent[node]
            return path, len(path) - 1
        
        for neighbor, _ in graph.get_active_neighbors(current):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    
    return None, float('inf')  # No path found


def find_k_disjoint_paths(graph, start, end, k):
    """
    Finds K edge-disjoint paths between two nodes using max-flow approach.
    
    Algorithm: Use Ford-Fulkerson with DFS to find augmenting paths.
    Each augmenting path represents one disjoint path.
    
    Time Complexity: O(K * (V + E)) for finding K paths
    Space Complexity: O(V + E)
    
    Parameters:
        graph (EmergencyGraph): Custom graph object
        start: Starting city
        end: Destination city
        k: Number of disjoint paths to find
    
    Returns:
        paths: List of K disjoint paths (or fewer if not available)
    """
    
    paths = []
    residual_graph = {}
    
    # Initialize residual graph (capacity = 1 for each edge)
    for city in graph.get_all_cities():
        residual_graph[city] = {}
        for neighbor, weight in graph.graph.get(city, []):
            if neighbor not in residual_graph[city]:
                residual_graph[city][neighbor] = 1
    
    # Find K augmenting paths
    for _ in range(k):
        path = _dfs_augmenting_path(residual_graph, start, end, graph)
        
        if path is None:
            break
        
        paths.append(path)
        
        # Reduce capacity along the path
        for i in range(len(path) - 1):
            u, v = path[i], path[i + 1]
            residual_graph[u][v] -= 1
            if residual_graph[u][v] == 0:
                del residual_graph[u][v]
            
            # Add reverse edge for flow return
            if v not in residual_graph:
                residual_graph[v] = {}
            residual_graph[v][u] = residual_graph[v].get(u, 0) + 1
    
    return paths


def _dfs_augmenting_path(residual_graph, start, end, original_graph, visited=None):
    """
    Helper function: DFS to find augmenting path in residual graph.
    
    Parameters:
        residual_graph: Graph with remaining capacities
        start: Starting node
        end: Target node
        original_graph: Original graph for checking active neighbors
        visited: Set of visited nodes in current DFS
    
    Returns:
        path: List of nodes in augmenting path, or None
    """
    
    if visited is None:
        visited = set()
    
    if start == end:
        return [end]
    
    visited.add(start)
    
    # Check neighbors in residual graph
    for neighbor in residual_graph.get(start, {}):
        if neighbor not in visited and residual_graph[start][neighbor] > 0:
            # Verify edge exists in original graph and is not vulnerable
            if (start, neighbor) not in original_graph.vulnerable_edges:
                path = _dfs_augmenting_path(residual_graph, neighbor, end, original_graph, visited)
                if path is not None:
                    return [start] + path
    
    return None


def get_all_paths(graph, start, end, max_paths=5):
    """
    Finds multiple paths between two nodes (not necessarily disjoint).
    Useful for showing alternative routes.
    
    Time Complexity: O(V^E) in worst case, but limited by max_paths
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): Custom graph object
        start: Starting city
        end: Destination city
        max_paths: Maximum number of paths to find
    
    Returns:
        paths: List of paths
    """
    
    all_paths = []
    
    def dfs(current, target, path, visited):
        if len(all_paths) >= max_paths:
            return
        
        if current == target:
            all_paths.append(path[:])
            return
        
        visited.add(current)
        
        for neighbor, _ in graph.get_active_neighbors(current):
            if neighbor not in visited:
                path.append(neighbor)
                dfs(neighbor, target, path, visited)
                path.pop()
        
        visited.remove(current)
    
    dfs(start, end, [start], set())
    return all_paths


def get_affected_nodes(graph, disabled_node):
    """
    Returns nodes that become disconnected when a node fails.
    
    Algorithm: Find connected components before/after node failure.
    
    Time Complexity: O(V + E)
    Space Complexity: O(V)
    
    Parameters:
        graph (EmergencyGraph): Custom graph object
        disabled_node: The node that has failed
    
    Returns:
        affected: Set of nodes disconnected from critical hubs
    """
    
    # Temporarily disable the node
    graph.disable_city(disabled_node)
    
    # Find connected components using BFS
    visited = set()
    components = []
    
    for city in graph.get_all_cities():
        if city not in visited and city not in graph.disabled_nodes:
            component = set()
            queue = deque([city])
            visited.add(city)
            component.add(city)
            
            while queue:
                current = queue.popleft()
                for neighbor, _ in graph.get_active_neighbors(current):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        component.add(neighbor)
                        queue.append(neighbor)
            
            components.append(component)
    
    # Re-enable the node
    graph.enable_city(disabled_node)
    
    # Nodes that were in different components are now disconnected
    affected = set()
    if len(components) > 1:
        # All nodes except largest component are affected
        largest = max(components, key=len)
        for component in components:
            if component != largest:
                affected.update(component)
    
    return affected
