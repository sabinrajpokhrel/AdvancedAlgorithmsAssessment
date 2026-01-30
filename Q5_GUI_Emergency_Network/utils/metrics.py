"""
Metrics & Analysis Module
Provides time complexity analysis and performance metrics for algorithms.
"""


class AlgorithmMetrics:
    """
    Stores and analyzes algorithm performance metrics.
    """
    
    def __init__(self):
        self.metrics = {}
    
    def add_metric(self, algorithm_name, metric_name, value):
        """
        Add a metric for an algorithm.
        
        Parameters:
            algorithm_name: Name of the algorithm
            metric_name: Name of the metric
            value: Metric value
        """
        if algorithm_name not in self.metrics:
            self.metrics[algorithm_name] = {}
        
        self.metrics[algorithm_name][metric_name] = value
    
    def get_time_complexity_description(self, algorithm_name):
        """
        Get human-readable time complexity description.
        
        Returns:
            description: Time complexity in Big-O notation
        """
        descriptions = {
            'Kruskal MST': 'O(E log E) - dominated by sorting edges',
            'Prim MST': 'O(V^2) - simple implementation, O(E log V) with heap',
            'Dijkstra': 'O(V^2) - dense graphs, O((V+E) log V) - with heap',
            'BFS': 'O(V + E) - linear in graph size',
            'DFS': 'O(V + E) - linear in graph size',
            'K-Disjoint Paths': 'O(K * (V + E)) - K iterations of DFS',
            'Graph Coloring': 'O(V^2 + E) - greedy with degree check',
            'AVL Rebalance': 'O(log n) - amortized per operation',
            'Cascade Failure': 'O(iterations * V^2) - iterative analysis'
        }
        
        return descriptions.get(algorithm_name, 'O(?) - unknown')
    
    def get_space_complexity_description(self, algorithm_name):
        """
        Get space complexity description.
        
        Returns:
            description: Space complexity in Big-O notation
        """
        descriptions = {
            'Kruskal MST': 'O(V + E) - union-find + edges',
            'Dijkstra': 'O(V) - distance array',
            'BFS': 'O(V) - queue + visited set',
            'K-Disjoint Paths': 'O(V + E) - residual graph',
            'Graph Coloring': 'O(V) - coloring map',
            'AVL Rebalance': 'O(n + log n) - tree + recursion stack'
        }
        
        return descriptions.get(algorithm_name, 'O(?) - unknown')


class GraphMetrics:
    """
    Calculates metrics about a graph.
    """
    
    @staticmethod
    def density(graph):
        """
        Calculate graph density (ratio of actual to possible edges).
        
        Formula: density = 2*E / (V*(V-1)) for undirected graphs
        
        Parameters:
            graph: EmergencyGraph object
        
        Returns:
            density: Value between 0 and 1
        """
        all_cities = graph.get_all_cities()
        v = len(all_cities)
        
        if v <= 1:
            return 0
        
        edges = graph.get_all_edges()
        e = len(edges)
        
        max_edges = (v * (v - 1)) / 2
        
        return (e / max_edges) if max_edges > 0 else 0
    
    @staticmethod
    def average_degree(graph):
        """
        Calculate average degree of nodes.
        
        Parameters:
            graph: EmergencyGraph object
        
        Returns:
            avg_degree: Average number of neighbors per node
        """
        all_cities = graph.get_all_cities()
        
        if not all_cities:
            return 0
        
        total_degree = 0
        
        for city in all_cities:
            neighbors = graph.get_active_neighbors(city)
            total_degree += len(neighbors)
        
        return total_degree / len(all_cities)
    
    @staticmethod
    def diameter(graph):
        """
        Calculate graph diameter (longest shortest path).
        
        Time Complexity: O(V^3) with Floyd-Warshall or O(V^2) with repeated BFS
        
        Parameters:
            graph: EmergencyGraph object
        
        Returns:
            diameter: Maximum distance between any two nodes
        """
        from graph.paths import dijkstra_shortest_path
        
        all_cities = graph.get_all_cities()
        max_distance = 0
        
        for start in all_cities:
            for end in all_cities:
                if start != end:
                    _, distance = dijkstra_shortest_path(graph, start, end)
                    if distance != float('inf'):
                        max_distance = max(max_distance, distance)
        
        return max_distance
    
    @staticmethod
    def connectivity(graph):
        """
        Estimate connectivity of graph (percentage of connected node pairs).
        
        Parameters:
            graph: EmergencyGraph object
        
        Returns:
            connectivity: Percentage of connected pairs (0-100)
        """
        from graph.paths import dijkstra_shortest_path
        
        all_cities = graph.get_all_cities()
        
        if len(all_cities) <= 1:
            return 100
        
        connected_pairs = 0
        total_pairs = 0
        
        for start in all_cities:
            for end in all_cities:
                if start != end:
                    total_pairs += 1
                    _, distance = dijkstra_shortest_path(graph, start, end)
                    if distance != float('inf'):
                        connected_pairs += 1
        
        if total_pairs == 0:
            return 0
        
        return (connected_pairs / total_pairs) * 100


class PathMetrics:
    """
    Metrics for paths and connectivity.
    """
    
    @staticmethod
    def path_length_distribution(graph, all_paths):
        """
        Analyze distribution of path lengths.
        
        Parameters:
            graph: EmergencyGraph object
            all_paths: List of paths (lists of nodes)
        
        Returns:
            distribution: Dictionary mapping length -> count
        """
        distribution = {}
        
        for path in all_paths:
            length = len(path) - 1  # Number of edges
            distribution[length] = distribution.get(length, 0) + 1
        
        return distribution
    
    @staticmethod
    def average_path_distance(graph, paths_with_distances):
        """
        Calculate average distance of paths.
        
        Parameters:
            paths_with_distances: List of (path, distance) tuples
        
        Returns:
            average: Mean distance of paths
        """
        if not paths_with_distances:
            return 0
        
        total = sum(distance for _, distance in paths_with_distances)
        return total / len(paths_with_distances)


class TreeMetrics:
    """
    Metrics for tree structures.
    """
    
    @staticmethod
    def imbalance_ratio(tree):
        """
        Calculate imbalance ratio (max_height / min_height).
        Closer to 1.0 means more balanced.
        
        Parameters:
            tree: BinarySearchTree or AVLTree
        
        Returns:
            ratio: Imbalance ratio (>= 1.0)
        """
        def min_max_height(node):
            if node is None:
                return 0, 0  # min, max
            
            if node.is_leaf() if hasattr(node, 'is_leaf') else (node.left is None and node.right is None):
                return 1, 1
            
            left_min, left_max = min_max_height(node.left)
            right_min, right_max = min_max_height(node.right)
            
            overall_min = 1 + min(left_min, right_min) if left_min > 0 or right_min > 0 else 1
            overall_max = 1 + max(left_max, right_max)
            
            return overall_min, overall_max
        
        min_h, max_h = min_max_height(tree.root)
        
        return (max_h / min_h) if min_h > 0 else 1.0
    
    @staticmethod
    def depth_statistics(tree):
        """
        Calculate depth statistics for tree.
        
        Parameters:
            tree: BinarySearchTree or AVLTree
        
        Returns:
            stats: Dictionary with min, max, avg depths
        """
        depths = []
        
        def collect_depths(node, depth):
            if node is None:
                return
            
            if node.left is None and node.right is None:
                depths.append(depth)
            
            collect_depths(node.left, depth + 1)
            collect_depths(node.right, depth + 1)
        
        collect_depths(tree.root, 0)
        
        if not depths:
            return {'min': 0, 'max': 0, 'avg': 0}
        
        return {
            'min': min(depths),
            'max': max(depths),
            'avg': sum(depths) / len(depths)
        }
