"""
Test Suite for Failure Simulation & Analysis
Tests node/edge failures and cascade effects.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from graph.graph_model import EmergencyGraph
from graph.failure import FailureAnalyzer, calculate_path_reliability


def test_failure_analyzer_init():
    """Test FailureAnalyzer initialization."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    
    analyzer = FailureAnalyzer(g)
    
    assert analyzer.graph is not None, "Graph should be initialized"
    assert isinstance(analyzer.failure_analysis, dict), "Should have failure_analysis dict"
    print("✓ test_failure_analyzer_init passed")


def test_node_failure_simple():
    """Test node failure analysis on simple graph."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    # No alternative path from 0 to 2
    
    analyzer = FailureAnalyzer(g)
    analysis = analyzer.analyze_node_failure(1)
    
    assert analysis['failed_node'] == 1, "Should analyze node 1"
    # Node 1 failure disconnects 0 from 2
    assert analysis['connectivity_loss'] > 0, "Should lose some connectivity"
    print("✓ test_node_failure_simple passed")


def test_node_failure_no_impact():
    """Test failure with minimal impact."""
    g = EmergencyGraph()
    # Fully connected mesh
    g.add_road(0, 1, 1)
    g.add_road(0, 2, 1)
    g.add_road(1, 2, 1)
    
    analyzer = FailureAnalyzer(g)
    analysis = analyzer.analyze_node_failure(0)
    
    # Nodes 1 and 2 should still be connected
    # Loss should be less than 100%
    assert analysis['connectivity_loss'] < 100, "Should maintain some connectivity"
    print("✓ test_node_failure_no_impact passed")


def test_edge_failure():
    """Test edge failure analysis."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 3, 1)
    
    analyzer = FailureAnalyzer(g)
    analysis = analyzer.analyze_edge_failure(1, 2)
    
    assert analysis['failed_edge'] == (1, 2), "Should analyze correct edge"
    assert isinstance(analysis['affected_paths'], list), "Should have affected paths list"
    print("✓ test_edge_failure passed")


def test_cascade_failure():
    """Test cascade failure simulation."""
    g = EmergencyGraph()
    # Create a star topology vulnerable to cascade
    g.add_road(0, 1, 1)
    g.add_road(0, 2, 1)
    g.add_road(0, 3, 1)
    g.add_road(0, 4, 1)
    
    analyzer = FailureAnalyzer(g)
    cascade_info = analyzer.simulate_cascade_failure([0])
    
    assert isinstance(cascade_info['phases'], list), "Should have phases"
    assert 0 in cascade_info['total_failed'], "Should include initial failed node"
    print("✓ test_cascade_failure passed")


def test_cascade_failure_complex():
    """Test cascade failure on more complex topology."""
    g = EmergencyGraph()
    # Create interconnected network
    edges = [
        (0, 1, 1), (0, 2, 1), (1, 3, 1),
        (2, 3, 1), (2, 4, 1), (3, 5, 1), (4, 5, 1)
    ]
    
    for u, v, w in edges:
        g.add_road(u, v, w)
    
    analyzer = FailureAnalyzer(g)
    cascade_info = analyzer.simulate_cascade_failure([0, 1])
    
    assert len(cascade_info['total_failed']) > 0, "Should have failed nodes"
    print(f"✓ test_cascade_failure_complex passed (failed: {cascade_info['total_failed']})")


def test_path_reliability():
    """Test path reliability calculation."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    g.add_road(2, 3, 1)
    
    path = [0, 1, 2, 3]
    reliability = calculate_path_reliability(g, path)
    
    assert 0 <= reliability <= 1, f"Reliability should be between 0 and 1, got {reliability}"
    assert reliability < 1, "Reliability should be less than 1 (multiple edges)"
    print(f"✓ test_path_reliability passed (reliability={reliability:.2%})")


def test_path_reliability_with_vulnerable():
    """Test path reliability with vulnerable edges."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    
    # Mark edge as vulnerable
    g.mark_vulnerable_road(0, 1)
    
    path = [0, 1, 2]
    reliability = calculate_path_reliability(g, path)
    
    # Vulnerable edges should lower reliability
    assert reliability < 0.95**2, "Vulnerable path should have lower reliability"
    print(f"✓ test_path_reliability_with_vulnerable passed (reliability={reliability:.2%})")


def test_failure_analysis_graph_unchanged():
    """Test that analysis doesn't permanently change graph."""
    g = EmergencyGraph()
    g.add_road(0, 1, 1)
    g.add_road(1, 2, 1)
    
    initial_cities = set(g.get_all_cities())
    initial_disabled = set(g.disabled_nodes)
    
    analyzer = FailureAnalyzer(g)
    analyzer.analyze_node_failure(1)
    
    final_cities = set(g.get_all_cities())
    final_disabled = set(g.disabled_nodes)
    
    assert initial_cities == final_cities, "Cities should not change"
    assert initial_disabled == final_disabled, "Disabled nodes should be restored"
    print("✓ test_failure_analysis_graph_unchanged passed")


def test_multiple_failures():
    """Test analyzing multiple failures."""
    g = EmergencyGraph()
    edges = [(0, 1, 1), (1, 2, 1), (2, 3, 1), (3, 4, 1)]
    for u, v, w in edges:
        g.add_road(u, v, w)
    
    analyzer = FailureAnalyzer(g)
    
    # Analyze failures
    results = []
    for node in [0, 1, 2]:
        analysis = analyzer.analyze_node_failure(node)
        results.append(analysis)
    
    assert len(results) == 3, "Should analyze 3 nodes"
    
    # Central nodes (1, 2) should have more impact
    impact_1 = results[1]['connectivity_loss']
    impact_2 = results[2]['connectivity_loss']
    impact_0 = results[0]['connectivity_loss']
    
    print(f"✓ test_multiple_failures passed (impacts: {impact_0:.1f}%, {impact_1:.1f}%, {impact_2:.1f}%)")


if __name__ == "__main__":
    test_failure_analyzer_init()
    test_node_failure_simple()
    test_node_failure_no_impact()
    test_edge_failure()
    test_cascade_failure()
    test_cascade_failure_complex()
    test_path_reliability()
    test_path_reliability_with_vulnerable()
    test_failure_analysis_graph_unchanged()
    test_multiple_failures()
    
    print("\n✅ All failure tests passed!")
