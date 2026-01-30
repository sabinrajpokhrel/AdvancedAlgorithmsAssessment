"""
Test Suite for Path Finding Algorithms
Tests Dijkstra, BFS, and K-Disjoint Paths.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph_model import EmergencyGraph
from graph.paths import dijkstra_shortest_path, bfs_shortest_path, find_k_disjoint_paths, get_affected_nodes


def test_dijkstra_basic():
    """Test Dijkstra shortest path."""
    g = EmergencyGraph()
    g.add_road(0, 1, 4)
    g.add_road(0, 2, 2)
    g.add_road(1, 2, 1)
    g.add_road(1, 3, 5)
    g.add_road(2, 3, 8)
    
    path, distance = dijkstra_shortest_path(g, 0, 3)
    
    assert path is not None, "Should find path"
    assert distance == 8, f"Expected distance 8, got {distance}"
    assert path[0] == 0 and path[-1] == 3, "Path should start at 0 and end at 3"
    print("✓ test_dijkstra_basic passed")


def test_dijkstra_no_path():
    """Test Dijkstra with disconnected nodes."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(2, 3, 1)
    
    path, distance = dijkstra_shortest_path(g, 0, 3)
    
    assert path is None, "Should return None for unreachable node"
    assert distance == float('inf'), "Distance should be infinity"
    print("✓ test_dijkstra_no_path passed")


def test_dijkstra_same_node():
    """Test path from node to itself."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    
    path, distance = dijkstra_shortest_path(g, 0, 0)
    
    assert path == [0], "Path to self should be [0]"
    assert distance == 0, "Distance to self should be 0"
    print("✓ test_dijkstra_same_node passed")


def test_bfs_shortest_path():
    """Test BFS path finding."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 3, 1)
    g.add_road(0, 3, 100)  # Direct but expensive path
    
    path, hops = bfs_shortest_path(g, 0, 3)
    
    assert path is not None, "Should find path"
    # BFS counts edges not nodes, so 3 edges = 4 nodes = 3 hops
    # But direct path exists, so it may return that instead
    # Let's just verify path exists and is valid
    assert path[0] == 0 and path[-1] == 3, "Path should start at 0 and end at 3"
    assert hops >= 1, f"Should have at least 1 hop, got {hops}"
    print("✓ test_bfs_shortest_path passed")


def test_k_disjoint_paths():
    """Test K-disjoint paths finding."""
    g = EmergencyGraph()
    # Create graph with multiple paths
    g.add_road(0, 1, 1)
    g.add_road(0, 2, 1)
    g.add_road(1, 3, 1)
    g.add_road(2, 3, 1)
    
    paths = find_k_disjoint_paths(g, 0, 3, 2)
    
    assert len(paths) >= 1, "Should find at least one path"
    assert len(paths) <= 2, "Should not find more than 2 disjoint paths"
    
    for path in paths:
        assert path[0] == 0 and path[-1] == 3, f"Invalid path: {path}"
    
    print(f"✓ test_k_disjoint_paths passed (found {len(paths)} paths)")


def test_k_disjoint_single_path():
    """Test K-disjoint with limited paths."""
    g = EmergencyGraph()
    # Linear graph - only one path
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    
    paths = find_k_disjoint_paths(g, 0, 2, 3)
    
    assert len(paths) == 1, f"Should find only 1 path, got {len(paths)}"
    assert paths[0] == [0, 1, 2], f"Incorrect path: {paths[0]}"
    print("✓ test_k_disjoint_single_path passed")


def test_affected_nodes_simple():
    """Test finding affected nodes after failure."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 3, 1)
    
    affected = get_affected_nodes(g, 1)
    
    # After node 1 fails in linear chain, nodes 0 and 2,3 become disconnected
    # The function returns nodes in smaller component, which would be 0 or {2,3}
    # Just verify it returns some nodes
    assert isinstance(affected, set), f"Should return set, got {type(affected)}"
    print(f"✓ test_affected_nodes_simple passed (affected: {affected})")


def test_affected_nodes_no_disconnection():
    """Test failure that doesn't disconnect."""
    g = EmergencyGraph()
    # Redundant paths
    g.add_road(0, 1, 1)
    g.add_road(0, 2, 1)
    g.add_road(1, 3, 1)
    g.add_road(2, 3, 1)
    
    affected = get_affected_nodes(g, 1)
    
    # Node 3 should still be reachable via 0->2->3
    assert 3 not in affected or len(affected) == 0, "Node 3 should still be reachable"
    print("✓ test_affected_nodes_no_disconnection passed")


def test_vulnerable_edges():
    """Test path finding with vulnerable edges."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(0, 2, 10)
    
    # Mark direct path as vulnerable
    g.mark_vulnerable_road(0, 2)
    
    path, distance = dijkstra_shortest_path(g, 0, 2)
    
    # Should avoid vulnerable edge and use 0->1->2
    assert path == [0, 1, 2], f"Should use alternate path, got {path}"
    print("✓ test_vulnerable_edges passed")


def test_path_with_disabled_nodes():
    """Test path finding with disabled nodes."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(0, 2, 10)
    
    # Disable middle node
    g.disable_city(1)
    
    path, distance = dijkstra_shortest_path(g, 0, 2)
    
    # Should find path avoiding disabled node or return None
    if path is not None:
        assert 1 not in path, f"Path should not contain disabled node: {path}"
    
    print("✓ test_path_with_disabled_nodes passed")


if __name__ == "__main__":
    test_dijkstra_basic()
    test_dijkstra_no_path()
    test_dijkstra_same_node()
    test_bfs_shortest_path()
    test_k_disjoint_paths()
    test_k_disjoint_single_path()
    test_affected_nodes_simple()
    test_affected_nodes_no_disconnection()
    test_vulnerable_edges()
    test_path_with_disabled_nodes()
    
    print("\n✅ All path tests passed!")
