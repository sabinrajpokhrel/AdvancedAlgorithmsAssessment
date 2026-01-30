"""
Visualization Utilities for Streamlit
Provides functions to render graphs and trees in the UI.
"""

import streamlit as st
import json
import os
from pathlib import Path
try:
    from pyvis.network import Network
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False


def visualize_graph_edges(graph, title="Graph Edges"):
    """
    Display graph edges in a formatted table.
    
    Parameters:
        graph: EmergencyGraph object
        title: Section title
    """
    st.subheader(title)
    
    edges = graph.get_all_edges()
    
    if not edges:
        st.info("No edges in graph")
        return
    
    # Display as columns
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**From**")
    with col2:
        st.write("**To**")
    with col3:
        st.write("**Weight**")
    
    st.divider()
    
    for u, v, w in edges:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"{u}")
        with col2:
            st.write(f"{v}")
        with col3:
            st.write(f"{w}")


def visualize_path(path, distance=None, title="Path"):
    """
    Display a path in visual format.
    
    Parameters:
        path: List of nodes in path
        distance: Total distance of path (optional)
        title: Section title
    """
    if path is None:
        st.warning(f"{title}: No path found")
        return
    
    st.subheader(title)
    
    # Create visual representation
    path_str = " → ".join(str(node) for node in path)
    st.write(f"**Path:** {path_str}")
    
    if distance is not None:
        st.write(f"**Distance:** {distance}")
    
    st.write(f"**Hops:** {len(path) - 1}")


def visualize_mst(mst_edges, total_weight=None, title="Minimum Spanning Tree"):
    """
    Display MST edges.
    
    Parameters:
        mst_edges: List of (u, v, weight) tuples
        total_weight: Total weight of MST
        title: Section title
    """
    st.subheader(title)
    
    if not mst_edges:
        st.info("No edges in MST")
        return
    
    # Display edges
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**From**")
    with col2:
        st.write("**To**")
    with col3:
        st.write("**Weight**")
    
    st.divider()
    
    for u, v, w in mst_edges:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write(f"{u}")
        with col2:
            st.write(f"{v}")
        with col3:
            st.write(f"{w}")
    
    if total_weight is not None:
        st.divider()
        st.metric("Total MST Weight", total_weight)


def visualize_coloring(coloring, color_to_frequency_func=None, title="Graph Coloring"):
    """
    Display graph coloring solution.
    
    Parameters:
        coloring: Dictionary mapping node -> color
        color_to_frequency_func: Function to convert color to readable name
        title: Section title
    """
    st.subheader(title)
    
    if not coloring:
        st.info("No coloring available")
        return
    
    # Group nodes by color
    color_groups = {}
    for node, color in coloring.items():
        if color not in color_groups:
            color_groups[color] = []
        color_groups[color].append(node)
    
    # Display by color
    for color in sorted(color_groups.keys()):
        nodes = color_groups[color]
        
        if color_to_frequency_func:
            color_label = color_to_frequency_func(color)
        else:
            color_label = f"Color {color}"
        
        st.write(f"**{color_label}:** {', '.join(str(n) for n in nodes)}")
    
    st.metric("Chromatic Number", len(color_groups))


def visualize_tree(tree, title="Command Hierarchy Tree"):
    """
    Display tree structure in hierarchical format.
    
    Parameters:
        tree: BinarySearchTree or AVLTree
        title: Section title
    """
    st.subheader(title)
    
    if tree.root is None:
        st.info("Tree is empty")
        return
    
    # Collect nodes with levels
    nodes_by_level = {}
    
    def collect_nodes(node, level):
        if node is None:
            return
        
        if level not in nodes_by_level:
            nodes_by_level[level] = []
        
        nodes_by_level[level].append(node.value)
        collect_nodes(node.left, level + 1)
        collect_nodes(node.right, level + 1)
    
    collect_nodes(tree.root, 0)
    
    # Display level by level
    for level in sorted(nodes_by_level.keys()):
        indent = "  " * level
        nodes = nodes_by_level[level]
        nodes_str = ", ".join(str(n) for n in nodes)
        st.write(f"{indent}└─ Level {level}: {nodes_str}")
    
    # Show metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Height", tree.get_height())
    with col2:
        st.metric("Size", tree.size)
    with col3:
        st.metric("Balanced", "✓" if tree.is_balanced() else "✗")


def visualize_failure_analysis(analysis, title="Failure Analysis Results"):
    """
    Display failure analysis results.
    
    Parameters:
        analysis: Dictionary from FailureAnalyzer
        title: Section title
    """
    st.subheader(title)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.metric(
            "Affected Nodes",
            len(analysis['affected_nodes']),
            delta_color="inverse"
        )
        
        st.metric(
            "Isolated Nodes",
            len(analysis['isolated_nodes']),
            delta_color="inverse"
        )
    
    with col2:
        st.metric(
            "Connectivity Loss",
            f"{analysis['connectivity_loss']:.1f}%",
            delta_color="inverse"
        )
    
    if analysis['affected_nodes']:
        st.write(f"**Affected nodes:** {', '.join(str(n) for n in analysis['affected_nodes'])}")
    
    if analysis['isolated_nodes']:
        st.write(f"**Isolated nodes:** {', '.join(str(n) for n in analysis['isolated_nodes'])}")


def visualize_disjoint_paths(paths, title="K-Disjoint Paths"):
    """
    Display multiple disjoint paths.
    
    Parameters:
        paths: List of paths (each path is list of nodes)
        title: Section title
    """
    st.subheader(title)
    
    if not paths:
        st.warning("No disjoint paths found")
        return
    
    for i, path in enumerate(paths, 1):
        path_str = " → ".join(str(node) for node in path)
        st.write(f"**Path {i}:** {path_str}")


def create_graph_input_panel():
    """
    Create interactive panel for graph input.
    
    Returns:
        graph_data: Dictionary with user inputs
    """
    st.subheader("Graph Input Panel")
    
    graph_data = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        node1 = st.text_input("From City", "0")
        try:
            graph_data['node1'] = int(node1)
        except:
            graph_data['node1'] = node1
    
    with col2:
        node2 = st.text_input("To City", "1")
        try:
            graph_data['node2'] = int(node2)
        except:
            graph_data['node2'] = node2
    
    with col3:
        weight = st.number_input("Weight", min_value=1, value=5)
        graph_data['weight'] = weight
    
    return graph_data


def create_algorithm_info_panel(algorithm_name):
    """
    Display algorithm information (complexity, description).
    
    Parameters:
        algorithm_name: Name of algorithm
    """
    st.info(f"**{algorithm_name}** - Raw implementation without external libraries")
    
    descriptions = {
        'Kruskal MST': {
            'time': 'O(E log E)',
            'space': 'O(V + E)',
            'desc': 'Greedy algorithm that builds MST by selecting edges in increasing weight order, using Union-Find for cycle detection.'
        },
        'Dijkstra': {
            'time': 'O(V²)',
            'space': 'O(V)',
            'desc': 'Finds shortest paths from a source node to all other nodes. Uses greedy selection of unvisited node with minimum distance.'
        },
        'K-Disjoint Paths': {
            'time': 'O(K × (V + E))',
            'space': 'O(V + E)',
            'desc': 'Finds K edge-disjoint paths using max-flow approach with Ford-Fulkerson algorithm.'
        },
        'Graph Coloring': {
            'time': 'O(V² + E)',
            'space': 'O(V)',
            'desc': 'Assigns colors to nodes such that no adjacent nodes share same color, using greedy Welsh-Powell heuristic.'
        },
        'AVL Rebalance': {
            'time': 'O(log n)',
            'space': 'O(log n)',
            'desc': 'Rebalances binary search tree through rotations to maintain height-balance property.'
        },
    }
    
    if algorithm_name in descriptions:
        info = descriptions[algorithm_name]
        col1, col2 = st.columns(2)
        with col1:
            st.write(f"**Time:** {info['time']}")
        with col2:
            st.write(f"**Space:** {info['space']}")
        st.write(f"**Approach:** {info['desc']}")


def render_graph_with_pyvis(graph, height=600, mst_edges=None):
    """
    Render an interactive network graph visualization using pyvis.
    """
    
    if not PYVIS_AVAILABLE:
        st.error("⚠️ Pyvis library not installed. Install with: pip install pyvis")
        return
    
    try:
        import tempfile
        import os
        
        # Create pyvis network
        net = Network(height=f"{height}px", width="100%", directed=False, notebook=False)
        
        # Add nodes
        nodes = graph.get_all_cities()
        if not nodes:
            st.info("No nodes in the graph. Add some cities to get started!")
            return
            
        for node in nodes:
            net.add_node(
                node, 
                label=str(node), 
                size=40, 
                color='#FF6B6B',
                font={'size': 18, 'color': 'white', 'bold': True},
                shape='circle'
            )
        
        # Create MST edge set for quick lookup
        mst_edge_set = set()
        if mst_edges:
            for u, v, w in mst_edges:
                mst_edge_set.add(tuple(sorted([u, v])))
        
        # Add edges
        edges = graph.get_all_edges()
        added_edges = set()
        
        for u, v, weight in edges:
            edge_key = tuple(sorted([u, v]))
            if edge_key in added_edges:
                continue
            added_edges.add(edge_key)
            
            # Determine edge color
            if edge_key in mst_edge_set:
                edge_color = '#00FF00'  # Green for MST edges
                edge_width = 4
            elif graph.is_road_vulnerable(u, v):
                edge_color = '#FF6B6B'  # Red for vulnerable
                edge_width = 3
            else:
                edge_color = '#4ECDC4'  # Teal for normal
                edge_width = 2
            
            net.add_edge(
                u, v, 
                label=str(weight),
                title=f"Distance: {weight}", 
                color=edge_color, 
                width=edge_width,
                font={'size': 14, 'color': '#333333', 'strokeWidth': 0, 'align': 'middle'}
            )
        
        # Generate HTML file
        html_file = tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False)
        html_path = html_file.name
        html_file.close()
        
        # Save network to HTML file
        net.save_graph(html_path)
        
        # Read HTML content
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Clean up temp file
        try:
            os.unlink(html_path)
        except:
            pass
        
        # Display in Streamlit
        st.components.v1.html(html_content, height=height, scrolling=False)
        
        # Display stats
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Nodes", len(nodes))
        with col2:
            st.metric("Roads", len(edges))
        with col3:
            total_distance = sum(w for _, _, w in edges) if edges else 0
            st.metric("Distance", total_distance)
        with col4:
            vulnerable = sum(1 for u, v, _ in edges if graph.is_road_vulnerable(u, v))
            st.metric("Vulnerable", vulnerable)
    
    except Exception as e:
        st.error(f"Graph error: {str(e)}")
        import traceback
        st.code(traceback.format_exc())

