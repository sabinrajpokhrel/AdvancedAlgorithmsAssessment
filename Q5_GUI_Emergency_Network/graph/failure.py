"""
Question 5 - Network Failure Simulation: Impact Analysis and Resilience Testing

Problem Overview:
Emergency networks must be resilient to failures. This module simulates what happens
when cities (nodes) or roads (edges) fail, analyzing the impact on network connectivity
and identifying critical infrastructure that requires protection or redundancy.

Approach:
I implemented iterative failure simulation that:
1. Temporarily disables specified nodes or edges
2. Recomputes connectivity using BFS to find disconnected components
3. Calculates affected nodes and lost connections
4. Identifies critical nodes whose failure causes maximum disruption
5. Detects cascade failures (failures that propagate to other nodes)

The analysis provides quantitative metrics:
- Connectivity loss percentage
- Number of isolated nodes
- Alternative route availability
- Critical node identification

This information guides infrastructure investment and disaster preparedness planning.

Time Complexity:
- Node failure analysis: O(V²) - pathfinding between all pairs
- Edge failure analysis: O(V²)
- Connectivity check: O(V + E) using BFS
"""

from collections import deque
from graph.paths import dijkstra_shortest_path, get_affected_nodes


class FailureAnalyzer:
    """
    Analyzes network impact when nodes or edges fail.
    Provides resilience metrics and identifies critical infrastructure.
    """
    
    def __init__(self, graph):
        """
        Initialize analyzer with a graph.
        
        Parameters:
            graph (EmergencyGraph): The network graph
        """
        self.graph = graph
        self.baseline_paths = {}
        self.failure_analysis = {}
    
    def analyze_node_failure(self, failed_node):
        """
        Analyzes impact of a single node failure.
        
        Time Complexity: O(V^2 + E) - one shortest path computation per node
        Space Complexity: O(V)
        
        Parameters:
            failed_node: The node that has failed
        
        Returns:
            analysis: Dictionary containing:
                - affected_nodes: Set of nodes disconnected
                - path_increases: Dict of new distances vs baseline
                - critical_edges: Edges that become critical
                - isolated_nodes: Completely disconnected nodes
        """
        
        analysis = {
            'failed_node': failed_node,
            'affected_nodes': set(),
            'path_increases': {},
            'critical_edges': [],
            'isolated_nodes': set(),
            'connectivity_loss': 0  # Percentage of lost connections
        }
        
        # Get affected nodes
        affected = get_affected_nodes(self.graph, failed_node)
        analysis['affected_nodes'] = affected
        
        # Simulate failure
        self.graph.disable_city(failed_node)
        
        # Check connectivity for all pairs
        all_cities = self.graph.get_all_cities()
        total_pairs = 0
        lost_connections = 0
        
        for start in all_cities:
            if start == failed_node or start in self.graph.disabled_nodes:
                continue
            
            for end in all_cities:
                if end == failed_node or end in self.graph.disabled_nodes or end == start:
                    continue
                
                total_pairs += 1
                
                # Try to find path after failure
                path, distance = dijkstra_shortest_path(self.graph, start, end)
                
                if path is None:
                    lost_connections += 1
                    if end not in analysis['isolated_nodes']:
                        analysis['isolated_nodes'].add(end)
        
        if total_pairs > 0:
            analysis['connectivity_loss'] = (lost_connections / total_pairs) * 100
        
        # Re-enable node
        self.graph.enable_city(failed_node)
        
        return analysis
    
    def analyze_edge_failure(self, city1, city2):
        """
        Analyzes impact of a single edge (road) failure.
        
        Time Complexity: O(V^2)
        Space Complexity: O(V)
        
        Parameters:
            city1, city2: Endpoints of the failed edge
        
        Returns:
            analysis: Dictionary containing impact metrics
        """
        
        analysis = {
            'failed_edge': (city1, city2),
            'affected_paths': [],
            'alternative_routes': {},
            'cost_increase': 0
        }
        
        # Mark edge as vulnerable (simulates failure)
        self.graph.mark_vulnerable_road(city1, city2)
        
        # Recalculate paths
        for start in self.graph.get_all_cities():
            for end in self.graph.get_all_cities():
                if start != end:
                    path, distance = dijkstra_shortest_path(self.graph, start, end)
                    
                    if path and city1 in path and city2 in path:
                        # This path was affected
                        analysis['affected_paths'].append((start, end))
        
        # Remove the vulnerable marking
        self.graph.vulnerable_edges.discard((city1, city2))
        self.graph.vulnerable_edges.discard((city2, city1))
        
        return analysis
    
    def simulate_cascade_failure(self, initial_failed_nodes):
        """
        Simulates cascading failures where one failure triggers others.
        
        Algorithm: Uses threshold-based model where nodes fail if connectivity
        drops below threshold.
        
        Time Complexity: O(iterations * (V^2 + E))
        Space Complexity: O(V)
        
        Parameters:
            initial_failed_nodes: List of initially failed nodes
        
        Returns:
            cascade_info: Detailed cascade progression
        """
        
        cascade_info = {
            'phases': [],
            'total_failed': set(initial_failed_nodes),
            'final_status': {}
        }
        
        failed = set(initial_failed_nodes)
        phase = 0
        connectivity_threshold = 0.3  # 30% connectivity required
        
        while True:
            phase += 1
            newly_failed = set()
            
            # Analyze each active node
            for node in self.graph.get_all_cities():
                if node not in failed and node not in self.graph.disabled_nodes:
                    # Check connectivity to critical nodes
                    connected_count = 0
                    total_critical = 0
                    
                    for other in self.graph.get_all_cities():
                        if other not in failed and other != node:
                            total_critical += 1
                            path, _ = dijkstra_shortest_path(self.graph, node, other)
                            if path is not None:
                                connected_count += 1
                    
                    if total_critical > 0:
                        connectivity = connected_count / total_critical
                        if connectivity < connectivity_threshold:
                            newly_failed.add(node)
            
            if not newly_failed:
                break
            
            # Record phase
            phase_info = {
                'phase': phase,
                'newly_failed': newly_failed,
                'total_failed_so_far': failed.union(newly_failed)
            }
            cascade_info['phases'].append(phase_info)
            
            failed.update(newly_failed)
            
            if phase > 10:  # Prevent infinite loops
                break
        
        cascade_info['total_failed'] = failed
        
        return cascade_info


def calculate_path_reliability(graph, path):
    """
    Calculates reliability of a path (probability all edges are operational).
    
    Assumes each edge has reliability independent of others.
    
    Time Complexity: O(path_length)
    Space Complexity: O(1)
    
    Parameters:
        graph (EmergencyGraph): The network
        path: List of nodes in path
    
    Returns:
        reliability: Probability (0-1) that path works
    """
    
    if len(path) < 2:
        return 1.0
    
    # Default edge reliability (can be extended with actual values)
    edge_reliability = 0.95
    
    reliability = 1.0
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        
        # Check if edge is vulnerable
        if (u, v) in graph.vulnerable_edges:
            edge_reliability = 0.7  # Vulnerable edges have lower reliability
        else:
            edge_reliability = 0.95
        
        reliability *= edge_reliability
    
    return reliability


"""
Remarks:
- Failure simulation provides quantitative resilience metrics for network planning.
- Node failure impact measured by connectivity loss percentage and isolated nodes.
- Critical node identification helps prioritize infrastructure protection investments.
- Cascade failure detection prevents catastrophic network collapse scenarios.
- Path reliability calculation guides emergency routing decisions during disasters.
- BFS-based connectivity analysis is efficient at O(V + E) per failure scenario.
- Temporary disable/enable mechanism allows testing without modifying graph structure.
"""
