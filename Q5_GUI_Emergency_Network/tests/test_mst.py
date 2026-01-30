"""
Test Suite for MST Algorithms
Tests Kruskal's algorithm with various graph configurations.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph_model import EmergencyGraph
from graph.mst import kruskal_mst
from utils.metrics import GraphMetrics


def test_kruskal_basic():
    """Test Kruskal with basic graph."""
    g = EmergencyGraph()
    g.add_road(0, 1, 4)
    g.add_road(0, 2, 2)
    g.add_road(1, 2, 1)
    g.add_road(1, 3, 5)
    g.add_road(2, 3, 8)
    
    mst, weight = kruskal_mst(g)
    
    assert len(mst) == 3, f"MST should have 3 edges, got {len(mst)}"
    # Expected MST: (1,2)=1 + (0,2)=2 + (1,3)=5 = 8
    assert weight == 8, f"MST weight should be 8, got {weight}"
    print("✓ test_kruskal_basic passed")


def test_kruskal_single_node():
    """Test with single node."""
    g = EmergencyGraph()
    g.add_city(0)
    
    mst, weight = kruskal_mst(g)
    
    assert len(mst) == 0, "MST of single node should be empty"
    assert weight == 0, "Weight should be 0"
    print("✓ test_kruskal_single_node passed")


def test_kruskal_disconnected():
    """Test with disconnected graph."""
    g = EmergencyGraph()
    # Component 1
    g.add_road(0, 1, 1)
    # Component 2
    g.add_road(2, 3, 2)
    
    mst, weight = kruskal_mst(g)
    
    # Should have 2 edges (one for each component)
    assert len(mst) == 2, f"Expected 2 edges, got {len(mst)}"
    assert weight == 3, f"Expected weight 3, got {weight}"
    print("✓ test_kruskal_disconnected passed")


def test_kruskal_duplicate_weights():
    """Test with duplicate edge weights."""
    g = EmergencyGraph()
    g.add_road(0, 1, 5)
    g.add_road(1, 2, 5)
    g.add_road(2, 3, 5)
    g.add_road(0, 3, 5)
    
    mst, weight = kruskal_mst(g)
    
    assert len(mst) == 3, f"Expected 3 edges, got {len(mst)}"
    assert weight == 15, f"Expected weight 15, got {weight}"
    print("✓ test_kruskal_duplicate_weights passed")


def test_kruskal_large_graph():
    """Test with larger graph (10 nodes)."""
    g = EmergencyGraph()
    
    # Create a more complex graph
    edges = [
        (0, 1, 2), (0, 2, 3), (1, 2, 1), (1, 3, 6),
        (2, 3, 4), (2, 4, 5), (3, 4, 2), (3, 5, 1),
        (4, 5, 3), (4, 6, 7), (5, 6, 8), (6, 7, 2),
        (7, 8, 5), (8, 9, 3), (7, 9, 4)
    ]
    
    for u, v, w in edges:
        g.add_road(u, v, w)
    
    mst, weight = kruskal_mst(g)
    
    assert len(mst) == 9, f"MST of 10 nodes should have 9 edges, got {len(mst)}"
    assert weight > 0, "Weight should be positive"
    print(f"✓ test_kruskal_large_graph passed (weight={weight})")


def test_kruskal_with_vulnerable_edges():
    """Test Kruskal with marked vulnerable roads (should still work for MST)."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 2)
    g.add_road(0, 2, 4)
    
    # Mark edge as vulnerable
    g.mark_vulnerable_road(0, 2)
    
    # MST algorithm works on all edges (doesn't check vulnerability)
    mst, weight = kruskal_mst(g)
    
    assert len(mst) == 2, f"Expected 2 edges, got {len(mst)}"
    print("✓ test_kruskal_with_vulnerable_edges passed")


def test_mst_properties():
    """Test that MST satisfies properties."""
    g = EmergencyGraph()
    
    # Create a spanning graph
    for i in range(5):
        for j in range(i + 1, 5):
            g.add_road(i, j, (i + j) % 3 + 1)
    
    mst, weight = kruskal_mst(g)
    
    # Properties:
    # 1. Number of edges should be V-1
    assert len(mst) == 4, f"MST should have 4 edges, got {len(mst)}"
    
    # 2. Should be connected (all nodes reachable)
    # 3. No cycles
    
    print("✓ test_mst_properties passed")


if __name__ == "__main__":
    test_kruskal_basic()
    test_kruskal_single_node()
    test_kruskal_disconnected()
    test_kruskal_duplicate_weights()
    test_kruskal_large_graph()
    test_kruskal_with_vulnerable_edges()
    test_mst_properties()
    
    print("\n✅ All MST tests passed!")
