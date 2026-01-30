# Interactive Emergency Network Simulator
# Advanced Algorithms with GUI Integration using Streamlit
# All algorithms are implemented from scratch without external algorithm libraries

import streamlit as st
import json
import os
from pathlib import Path
import pandas as pd

from graph.graph_model import EmergencyGraph
from graph.mst import kruskal_mst
from graph.paths import dijkstra_shortest_path, find_k_disjoint_paths, get_affected_nodes
from graph.failure import FailureAnalyzer
from graph.coloring import greedy_graph_coloring, validate_coloring, analyze_coloring_efficiency, color_to_frequency
from tree.tree_model import BinarySearchTree
from tree.rebalance import AVLTree, rebalance_tree, analyze_tree_balance
from utils.visualization import (
    visualize_graph_edges, visualize_mst, visualize_path, visualize_coloring,
    visualize_tree, visualize_failure_analysis, visualize_disjoint_paths,
    create_graph_input_panel, create_algorithm_info_panel, render_graph_with_pyvis
)
from utils.metrics import GraphMetrics, AlgorithmMetrics


def build_sample_graph():
    """Build a sample emergency network for demonstration."""
    g = EmergencyGraph()
    g.add_road(0, 1, 4)
    g.add_road(0, 2, 4)
    g.add_road(1, 2, 2)
    g.add_road(1, 3, 5)
    g.add_road(2, 3, 5)
    g.add_road(2, 4, 11)
    g.add_road(3, 4, 2)
    g.add_road(3, 5, 6)
    g.add_road(4, 5, 3)
    return g


def build_sample_command_tree():
    """Build a sample command hierarchy tree."""
    tree = BinarySearchTree()
    values = [5, 3, 7, 2, 4, 6, 8]
    for val in values:
        tree.insert(val)
    return tree


# Page Configuration
st.set_page_config(
    page_title="Emergency Network Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and Description
st.title("🚨 Emergency Communication & Response System Simulator")
st.markdown("""
**Interactive GUI for Advanced Algorithm Design**
- All algorithms implemented from scratch without external libraries
- Real-time graph visualization and optimization
- Network resilience analysis and failure simulation
""")

st.divider()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Module:",
    [
        "📊 Dashboard",
        "🌳 Q1: MST Visualization",
        "🛣️ Q2: Path Finder",
        "🎯 Q3: Command Hierarchy",
        "⚡ Q4: Failure Simulation",
        "📡 Bonus: Graph Coloring"
    ]
)

# Initialize session state for persistent graph
if 'graph' not in st.session_state:
    st.session_state.graph = build_sample_graph()

if 'command_tree' not in st.session_state:
    st.session_state.command_tree = build_sample_command_tree()

graph = st.session_state.graph
command_tree = st.session_state.command_tree


# ============================================================================
# PAGE: DASHBOARD - VISUAL GRAPH EDITOR & SIMULATOR
# ============================================================================
if page == "📊 Dashboard":
    st.header("🖥️ Network Dashboard - Visual Graph Editor")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Interactive Network Visualization")
        # Render interactive graph visualization
        render_graph_with_pyvis(graph, height=600)
    
    with col2:
        st.subheader("Network Stats")
        st.metric("Total Cities", len(graph.get_all_cities()))
        st.metric("Total Roads", len(graph.get_all_edges()))
        st.metric("Density", f"{GraphMetrics.density(graph):.2%}")
        st.metric("Avg Degree", f"{GraphMetrics.average_degree(graph):.2f}")
    
    st.divider()
    st.subheader("🔧 Graph Configuration Panel")
    
    config_col1, config_col2, config_col3 = st.columns(3)
    
    with config_col1:
        st.write("**Add New Road**")
        node1 = st.number_input("From City", min_value=0, value=0, key="add_from")
        node2 = st.number_input("To City", min_value=0, value=1, key="add_to")
        weight = st.number_input("Weight/Cost", min_value=1, value=5, key="add_weight")
        
        if st.button("➕ Add Road", use_container_width=True):
            if node1 != node2:
                graph.add_road(int(node1), int(node2), int(weight))
                st.success(f"✓ Added road: {int(node1)} ↔ {int(node2)} (cost {int(weight)})")
                st.rerun()
            else:
                st.error("Cannot connect a city to itself")
    
    with config_col2:
        st.write("**Remove Road**")
        edges = graph.get_all_edges()
        if edges:
            edge_labels = [f"{u}←→{v} (w:{w})" for u, v, w in edges]
            selected_edge = st.selectbox("Select edge to remove", edge_labels, key="remove_edge")
            
            if st.button("❌ Remove Road", use_container_width=True):
                u, v, w = edges[edge_labels.index(selected_edge)]
                graph.remove_road(u, v)
                st.success(f"✓ Removed road: {u} ↔ {v}")
                st.rerun()
    
    with config_col3:
        st.write("**Mark Vulnerable**")
        edges = graph.get_all_edges()
        if edges:
            edge_labels = [f"{u}←→{v} (w:{w})" for u, v, w in edges]
            selected_edge = st.selectbox("Select edge to mark", edge_labels, key="mark_edge")
            
            if st.button("⚠️ Mark as Vulnerable", use_container_width=True):
                u, v, w = edges[edge_labels.index(selected_edge)]
                graph.mark_vulnerable_road(u, v)
                st.success(f"✓ Marked vulnerable: {u}—{v}")
                st.rerun()
    
    st.divider()
    st.subheader("📋 Current Network Edges")
    visualize_graph_edges(graph, "Network Topology")


# ============================================================================
# PAGE: Q1 - MST VISUALIZATION
# ============================================================================
elif page == "🌳 Q1: MST Visualization":
    st.header("Q1: Dynamic MST Visualization [6 marks]")
    
    create_algorithm_info_panel("Kruskal MST")
    
    st.divider()
    
    st.subheader("Algorithm Details")
    with st.expander("Click to expand algorithm explanation"):
        st.markdown("""
        **Kruskal's Algorithm** builds the Minimum Spanning Tree using a greedy approach:
        
        1. **Sort edges** by weight in ascending order
        2. **Initialize Union-Find** structure for cycle detection
        3. **For each edge** (in order):
           - If it connects two different components, add it to MST
           - Use Union-Find to check connectivity
        4. **Stop** when we have V-1 edges
        
        **Time Complexity:** O(E log E) - dominated by edge sorting
        **Space Complexity:** O(V + E) - for union-find and edge storage
        
        **Why this works:**
        - Greedy selection of lightest edges guarantees optimality
        - Union-Find prevents cycles in O(1) amortized time
        - Results in connected acyclic graph with minimum total weight
        """)
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("MST Computation")
        if st.button("🔄 Compute MST\n(Kruskal's Algorithm)", key="btn_mst", use_container_width=True):
            with st.spinner("Computing MST..."):
                mst_edges, total_weight = kruskal_mst(graph)
                st.session_state.mst_result = (mst_edges, total_weight)
        
        if 'mst_result' in st.session_state:
            mst_edges, total_weight = st.session_state.mst_result
            
            st.info(f"""
            ### ✓ MST Computed
            **Edges:** {len(mst_edges)}  
            **Expected:** {len(graph.get_all_cities()) - 1}  
            **Total Weight:** {total_weight}
            """)
            
            with st.expander("View MST Edges"):
                visualize_mst(mst_edges, total_weight)


# ============================================================================
# PAGE: Q2 - PATH FINDER
# ============================================================================
elif page == "🛣️ Q2: Reliable Path Finder with GUI Controls":
    st.header("Q2: Path Finder & K-Disjoint Paths [5 marks]")
    
    create_algorithm_info_panel("Dijkstra")
    
    st.divider()
    
    st.subheader("Algorithm Explanation")
    with st.expander("Click to expand"):
        st.markdown("""
        **Dijkstra's Algorithm** finds the shortest path between two nodes:
        
        1. Initialize distances: source=0, others=infinity
        2. Repeatedly select unvisited node with minimum distance
        3. Update distances to neighbors: new_dist = current_dist + edge_weight
        4. Continue until destination is reached
        
        **Time Complexity:** O(V²) for dense graphs, O((V+E) log V) with binary heap
        **Space Complexity:** O(V) for distance and previous node arrays
        
        **K-Disjoint Paths** uses Ford-Fulkerson (max-flow) approach:
        - Find augmenting paths in residual graph
        - Each path found is edge-disjoint from others
        - Time: O(K × (V + E))
        """)
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("🔍 Path Search")
        all_cities = sorted(graph.get_all_cities())
        
        start_node = st.selectbox("Source City", all_cities, key="path_start")
        end_node = st.selectbox("Destination City", all_cities, key="path_end", index=min(1, len(all_cities)-1))
        
        if start_node != end_node:
            if st.button("🎯 Find Shortest Path", use_container_width=True):
                with st.spinner("Computing..."):
                    path, distance = dijkstra_shortest_path(graph, start_node, end_node)
                    st.session_state.shortest_path = (path, distance)
            
            k = st.number_input("# Disjoint Paths", min_value=1, max_value=5, value=2, key="k_paths")
            if st.button("📍 Find K-Disjoint Paths", use_container_width=True):
                with st.spinner(f"Computing {k} paths..."):
                    paths = find_k_disjoint_paths(graph, start_node, end_node, k)
                    st.session_state.disjoint_paths = paths
        
        # Results
        if 'shortest_path' in st.session_state:
            path, distance = st.session_state.shortest_path
            if path:
                st.success(f"✓ Path Found")
                st.info(f"""
                **Path:** {' → '.join(map(str, path))}  
                **Distance:** {distance}  
                **Hops:** {len(path)-1}
                """)
            else:
                st.error("❌ No path found")
        
        if 'disjoint_paths' in st.session_state:
            paths = st.session_state.disjoint_paths
            st.success(f"✓ Found {len(paths)} disjoint paths")
            for i, p in enumerate(paths, 1):
                st.write(f"Path {i}: {' → '.join(map(str, p))}")


# ============================================================================
# PAGE: Q3 - COMMAND HIERARCHY OPTIMIZER
# ============================================================================
elif page == "🎯 Q3: Command Hierarchy Optimizer":
    st.header("Q3: Command Hierarchy Tree Optimization [4 marks]")
    
    create_algorithm_info_panel("AVL Rebalance")
    
    st.divider()
    
    st.subheader("Algorithm Explanation")
    with st.expander("Click to expand"):
        st.markdown("""
        **AVL Tree Rebalancing** maintains a balanced binary search tree:
        
        **Balance Factor = Height(Left) - Height(Right)**
        - Must be in [-1, 0, 1] for AVL property
        
        **Rotations (O(1) operations):**
        1. **Left Rotation** - Right-heavy case
        2. **Right Rotation** - Left-heavy case  
        3. **Left-Right Rotation** - Left-Right case
        4. **Right-Left Rotation** - Right-Left case
        
        **Time Complexity:** O(log n) per operation after rebalancing
        **Space Complexity:** O(n) for tree + O(log n) for recursion
        
        **Benefits:**
        - Guarantees O(log n) height (vs O(n) for unbalanced)
        - Minimizes maximum communication path length
        """)
    
    st.divider()
    
    col1, col2, col3 = st.columns([1.5, 1.5, 1.5])
    
    with col1:
        st.subheader("Before Rebalancing")
        visualize_tree(command_tree, "original")
        
        analysis_before = analyze_tree_balance(command_tree)
        
        metric_col1, metric_col2 = st.columns(2)
        with metric_col1:
            st.metric("Height", analysis_before['height'], delta=None)
        with metric_col2:
            st.metric("Balanced?", "✓" if analysis_before['is_balanced'] else "✗")
    
    with col2:
        st.subheader("🔄 Rebalance")
        
        if st.button("Convert to AVL Tree", use_container_width=True, key="btn_rebalance"):
            with st.spinner("Rebalancing..."):
                balanced_tree = rebalance_tree(command_tree)
                st.session_state.balanced_tree = balanced_tree
                st.session_state.rebalance_done = True
    
    with col3:
        st.subheader("After Rebalancing")
        
        if 'balanced_tree' in st.session_state:
            balanced_tree = st.session_state.balanced_tree
            visualize_tree(balanced_tree, "balanced")
            
            analysis_after = analyze_tree_balance(balanced_tree)
            
            metric_col3, metric_col4 = st.columns(2)
            with metric_col3:
                height_reduction = analysis_before['height'] - analysis_after['height']
                st.metric("Height", analysis_after['height'], 
                         delta=f"-{height_reduction}" if height_reduction > 0 else "No change")
            with metric_col4:
                st.metric("Balanced?", "✓" if analysis_after['is_balanced'] else "✗")
        else:
            st.info("Click rebalance to see result")
    
    st.divider()
    
    if 'rebalance_done' in st.session_state and st.session_state.rebalance_done:
        st.subheader("📊 Optimization Metrics")
        
        analysis_after = analyze_tree_balance(st.session_state.balanced_tree)
        
        metric_data = {
            'Metric': ['Height', 'Max Path Length', 'Is Balanced', 'Balance Factor Range'],
            'Before': [
                analysis_before['height'],
                analysis_before['max_path_length'],
                '✓' if analysis_before['is_balanced'] else '✗',
                analysis_before['balance_factors']
            ],
            'After': [
                analysis_after['height'],
                analysis_after['max_path_length'],
                '✓' if analysis_after['is_balanced'] else '✗',
                analysis_after['balance_factors']
            ]
        }
        
        st.dataframe(pd.DataFrame(metric_data), use_container_width=True, hide_index=True)
        
        if not analysis_before['is_balanced'] and analysis_after['is_balanced']:
            st.success("✅ Tree successfully balanced! Max path length reduced.")



# ============================================================================
# PAGE: Q4 - FAILURE SIMULATION
# ============================================================================
elif page == "⚡ Q4: Failure Simulation & Rerouting":
    st.header("Q4: Network Failure Simulation [5 marks]")
    
    st.subheader("Failure Analysis Features")
    with st.expander("Click to expand"):
        st.markdown("""
        **Node Failure Impacts:**
        - Simulates critical hub going down
        - Identifies disconnected nodes
        - Calculates connectivity loss percentage
        - Proposes alternative routes
        
        **Algorithm:**
        1. Disable node in graph
        2. Recompute shortest paths for all pairs
        3. Count lost connections
        4. Calculate affected subnetworks
        5. Re-enable node (analysis is non-destructive)
        
        **Time Complexity:** O(V²) per node analyzed
        **Space Complexity:** O(V)
        """)
    
    st.divider()
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("⚠️ Failure Scenario")
        
        all_cities = sorted(graph.get_all_cities())
        failed_node = st.selectbox("City to fail", all_cities, key="fail_node")
        
        if st.button("Run Simulation", use_container_width=True, key="btn_simulate"):
            with st.spinner(f"Analyzing {failed_node} failure..."):
                analyzer = FailureAnalyzer(graph)
                analysis = analyzer.analyze_node_failure(failed_node)
                st.session_state.failure_analysis = analysis
    
    with col3:
        st.subheader("📊 Results")
        
        if 'failure_analysis' in st.session_state:
            analysis = st.session_state.failure_analysis
            
            affected_count = len(analysis['affected_nodes'])
            disconnected = len(analysis['disconnected_nodes'])
            
            col_x, col_y = st.columns(2)
            with col_x:
                st.metric("Affected Nodes", affected_count)
            with col_y:
                st.metric("Disconnected", disconnected)
            
            impact_pct = (disconnected / len(all_cities)) * 100 if all_cities else 0
            st.metric("Network Impact", f"{impact_pct:.1f}%")
            
            if affected_count > 0:
                st.warning(f"⚠️ {affected_count} nodes unable to reach destination")
            else:
                st.success("✓ Network remains fully connected")
    
    st.divider()
    
    if 'failure_analysis' in st.session_state:
        st.subheader("Alternative Routes Analysis")
        
        analysis = st.session_state.failure_analysis
        affected_list = sorted(list(analysis['affected_nodes']))[:5]
        
        if affected_list:
            col_routes = st.columns(len(affected_list) if affected_list else 1)
            
            for idx, (col, target) in enumerate(zip(col_routes, affected_list)):
                with col:
                    st.markdown(f"**To {target}:**")
                    
                    # Try to find alternative path without failed node
                    graph.disable_city(failed_node)
                    alt_path, alt_dist = dijkstra_shortest_path(graph, 0, target)
                    graph.enable_city(failed_node)
                    
                    if alt_path:
                        st.success(f"✓ {' → '.join(map(str, alt_path))}")
                    else:
                        st.error("✗ No route exists")



# ============================================================================
# PAGE: BONUS - GRAPH COLORING
# ============================================================================
elif page == "📡 Bonus: Graph Coloring":
    st.header("Bonus: Graph Coloring for Frequency Assignment [+2 marks]")
    
    create_algorithm_info_panel("Graph Coloring")
    
    st.divider()
    
    st.subheader("Algorithm Explanation")
    with st.expander("Click to expand"):
        st.markdown("""
        **Welsh-Powell Greedy Coloring:**
        
        1. **Sort vertices** by degree (highest first)
        2. **For each vertex:**
           - Find all colors used by adjacent vertices
           - Assign smallest available color
        
        **Chromatic Number:**
        - Minimum colors needed to color graph
        - Lower bound: 1
        - Upper bound: Δ + 1 (max degree + 1)
        - Equals to max clique size for some graphs
        
        **Time Complexity:** O(V² + E)
        **Space Complexity:** O(V)
        
        **Application:** Assign communication frequencies so adjacent hubs don't interfere
        """)
    
    st.divider()
    
    col1, col2 = st.columns([2.5, 1.5])
    
    with col1:
        st.subheader("Network Frequency Assignment")
        
        if st.button("🎨 Compute Graph Coloring", use_container_width=True, key="btn_coloring"):
            with st.spinner("Computing optimal frequency assignment..."):
                coloring, chromatic = greedy_graph_coloring(graph)
                is_valid, violations = validate_coloring(graph, coloring)
                analysis = analyze_coloring_efficiency(graph, coloring)
                
                st.session_state.coloring_result = (coloring, chromatic, is_valid, violations, analysis)
        
        if 'coloring_result' in st.session_state:
            coloring, chromatic, is_valid, violations, analysis = st.session_state.coloring_result
            
            # Create visual representation of coloring
            render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("📊 Coloring Stats")
        
        if 'coloring_result' in st.session_state:
            coloring, chromatic, is_valid, violations, analysis = st.session_state.coloring_result
            
            st.metric("Colors Used", chromatic)
            st.metric("Valid", "✓ Yes" if is_valid else "✗ No")
            st.metric("Efficiency", f"{analysis['efficiency']:.1f}%")
            
            if not is_valid:
                st.error(f"⚠️ {len(violations)} conflicts found")
            else:
                st.success("✓ No conflicts")
            
            st.divider()
            st.subheader("Frequency Bands")
            
            frequency_map = {
                0: "2.4 GHz",
                1: "3.6 GHz", 
                2: "5.8 GHz",
                3: "28 GHz",
                4: "39 GHz"
            }
            
            for city in sorted(coloring.keys()):
                color = coloring[city]
                freq = frequency_map.get(color, f"Band {color}")
                st.write(f"City {city}: **{freq}**")
        else:
            st.info("Click 'Compute Graph Coloring' to see results")

st.divider()

# Footer
st.markdown("""
---
**Emergency Network Simulator** | Advanced Algorithm Design Project  
All algorithms implemented from scratch without external libraries  
""")

