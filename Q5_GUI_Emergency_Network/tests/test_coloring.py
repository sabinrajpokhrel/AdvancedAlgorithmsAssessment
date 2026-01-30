"""
Test Suite for Graph Coloring Algorithm
Tests greedy coloring and validation.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph_model import EmergencyGraph
from graph.coloring import (
    greedy_graph_coloring, validate_coloring, find_maximum_independent_set,
    multi_coloring_heuristics, analyze_coloring_efficiency
)


def test_greedy_coloring_basic():
    """Test basic graph coloring."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 0, 1)  # Triangle
    
    coloring, chromatic = greedy_graph_coloring(g)
    
    assert chromatic == 3, f"Triangle needs 3 colors, got {chromatic}"
    assert len(coloring) == 3, "Should color all nodes"
    print("✓ test_greedy_coloring_basic passed")


def test_greedy_coloring_bipartite():
    """Test coloring of bipartite graph."""
    g = EmergencyGraph()
    # Bipartite graph
    g.add_road(0, 2, 1)
    g.add_road(0, 3, 1)
    g.add_road(1, 2, 1)
    g.add_road(1, 3, 1)
    
    coloring, chromatic = greedy_graph_coloring(g)
    
    assert chromatic == 2, f"Bipartite graph needs 2 colors, got {chromatic}"
    print("✓ test_greedy_coloring_bipartite passed")


def test_greedy_coloring_independent_set():
    """Test coloring of independent set (no edges)."""
    g = EmergencyGraph()
    g.add_city(0)
    g.add_city(1)
    g.add_city(2)
    
    coloring, chromatic = greedy_graph_coloring(g)
    
    # All nodes can have same color
    assert chromatic == 1, f"Independent set needs 1 color, got {chromatic}"
    print("✓ test_greedy_coloring_independent_set passed")


def test_validate_coloring_valid():
    """Test validation of valid coloring."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    
    coloring, _ = greedy_graph_coloring(g)
    is_valid, violations = validate_coloring(g, coloring)
    
    assert is_valid, f"Valid coloring marked invalid. Violations: {violations}"
    assert len(violations) == 0, "Should have no violations"
    print("✓ test_validate_coloring_valid passed")


def test_validate_coloring_invalid():
    """Test validation detects invalid coloring."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    
    # Create invalid coloring (adjacent nodes same color)
    invalid_coloring = {0: 0, 1: 0, 2: 1}  # 0 and 1 same color but adjacent
    
    is_valid, violations = validate_coloring(g, invalid_coloring)
    
    assert not is_valid, "Should detect invalid coloring"
    assert len(violations) > 0, "Should report violations"
    print("✓ test_validate_coloring_invalid passed")


def test_maximum_independent_set():
    """Test finding maximum independent set."""
    g = EmergencyGraph()
    # Create graph where {0, 3} is independent set
    g.add_road(1, 0, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 3, 1)
    
    indep_set = find_maximum_independent_set(g)
    
    assert isinstance(indep_set, list), "Should return list"
    
    # Verify no two nodes in set are adjacent
    for i, u in enumerate(indep_set):
        for v in indep_set[i+1:]:
            neighbors = [n for n, _ in g.get_active_neighbors(u)]
            assert v not in neighbors, f"Nodes {u} and {v} are adjacent but in independent set"
    
    print(f"✓ test_maximum_independent_set passed (size={len(indep_set)})")


def test_multi_coloring_heuristics():
    """Test multiple coloring heuristics."""
    g = EmergencyGraph()
    edges = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 0, 1), (0, 2, 1)]
    for u, v, w in edges:
        g.add_road(u, v, w)
    
    best_coloring, best_chromatic, all_results = multi_coloring_heuristics(g)
    
    assert len(all_results) >= 2, "Should have multiple heuristics"
    assert best_chromatic is not None, "Should return best chromatic number"
    assert best_coloring is not None, "Should return best coloring"
    
    # All results should be valid
    for heur, (coloring, chromatic) in all_results.items():
        is_valid, _ = validate_coloring(g, coloring)
        assert is_valid, f"Heuristic {heur} produced invalid coloring"
    
    print(f"✓ test_multi_coloring_heuristics passed (best={best_chromatic} colors)")


def test_coloring_efficiency():
    """Test coloring efficiency analysis."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 3, 1)
    
    coloring, chromatic = greedy_graph_coloring(g)
    analysis = analyze_coloring_efficiency(g, coloring)
    
    assert 'chromatic_number' in analysis, "Should have chromatic_number"
    assert 'efficiency' in analysis, "Should have efficiency metric"
    assert analysis['chromatic_number'] == chromatic, "Chromatic number should match"
    
    print(f"✓ test_coloring_efficiency passed (efficiency={analysis['efficiency']:.1f}%)")


def test_large_graph_coloring():
    """Test coloring on larger graph."""
    g = EmergencyGraph()
    
    # Create larger graph (10 nodes)
    for i in range(10):
        for j in range(i+1, min(i+4, 10)):  # Each node connects to next 3
            g.add_road(i, j, 1)
    
    coloring, chromatic = greedy_graph_coloring(g)
    
    assert len(coloring) == 10, "Should color all nodes"
    assert chromatic <= 4, "Should use reasonable number of colors"
    
    is_valid, _ = validate_coloring(g, coloring)
    assert is_valid, "Coloring should be valid"
    
    print(f"✓ test_large_graph_coloring passed (chromatic={chromatic})")


def test_coloring_empty_graph():
    """Test coloring of empty graph."""
    g = EmergencyGraph()
    
    coloring, chromatic = greedy_graph_coloring(g)
    
    assert len(coloring) == 0, "Empty graph should have no colors"
    assert chromatic == 0, "Chromatic number should be 0"
    print("✓ test_coloring_empty_graph passed")


if __name__ == "__main__":
    test_greedy_coloring_basic()
    test_greedy_coloring_bipartite()
    test_greedy_coloring_independent_set()
    test_validate_coloring_valid()
    test_validate_coloring_invalid()
    test_maximum_independent_set()
    test_multi_coloring_heuristics()
    test_coloring_efficiency()
    test_large_graph_coloring()
    test_coloring_empty_graph()
    
    print("\n✅ All coloring tests passed!")
