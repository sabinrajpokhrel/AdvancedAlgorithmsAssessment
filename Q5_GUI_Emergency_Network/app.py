# Emergency Network Simulator - Simplified Visual Version
import streamlit as st
import pandas as pd
from graph.graph_model import EmergencyGraph
from graph.mst import kruskal_mst
from graph.paths import dijkstra_shortest_path, find_k_disjoint_paths
from graph.failure import FailureAnalyzer
from graph.coloring import greedy_graph_coloring, validate_coloring, analyze_coloring_efficiency
from tree.tree_model import BinarySearchTree
from tree.rebalance import rebalance_tree, analyze_tree_balance
from utils.visualization import render_graph_with_pyvis, visualize_tree, create_algorithm_info_panel


def build_sample_graph():
    """Build a sample emergency network for demonstration."""
    g = EmergencyGraph()
    g.add_road(0, 1, 4)
    g.add_road(0, 2, 4)
    g.add_road(1, 2, 2)
    g.add_road(1, 3, 5)
    g.add_road(2, 3, 8)
    g.add_road(3, 4, 2)
    g.add_road(2, 4, 10)
    g.add_road(0, 5, 7)
    g.add_road(5, 3, 1)
    return g


def build_sample_tree():
    """Build a sample tree for testing."""
    tree = BinarySearchTree()
    values = [50, 30, 70, 20, 40, 60, 80, 10, 25]
    for val in values:
        tree.insert(val)
    return tree


# Page configuration
st.set_page_config(page_title="Emergency Network Simulator", layout="wide", initial_sidebar_state="expanded")
st.title("Emergency Network Simulator")
st.markdown("*Interactive Visual Graph & Algorithm Simulator*")

# Initialize session state
if 'graph' not in st.session_state:
    st.session_state.graph = build_sample_graph()
if 'command_tree' not in st.session_state:
    st.session_state.command_tree = build_sample_tree()

graph = st.session_state.graph
command_tree = st.session_state.command_tree

# Navigation
page = st.sidebar.radio(
    "Select Algorithm",
    [
        "Q1: MST",
        "Q2: Path Finder",
        "Q3: Tree Optimizer",
        "Q4: Failure Simulation",
        "Q5: Graph Coloring"
    ]
)

# ============================================================================
# PAGE: Q1 - MST
# ============================================================================
if page == "Q1: MST":
    st.header("Q1: Minimum Spanning Tree")
    create_algorithm_info_panel("Kruskal")
    
    col1, col2 = st.columns([2, 1])
    
    with col2:
        st.subheader("Compute MST")
        
        if st.button("Calculate MST", use_container_width=True):
            with st.spinner("Computing..."):
                mst_edges, mst_weight = kruskal_mst(graph)
                st.session_state.mst_result = (mst_edges, mst_weight)
                st.rerun()
        
        if 'mst_result' in st.session_state:
            mst_edges, mst_weight = st.session_state.mst_result
            
            st.success("MST Computed")
            st.metric("Total Weight", mst_weight)
            st.metric("Edges", len(mst_edges))
            
            st.divider()
            st.write("**MST Edges:**")
            for u, v, w in mst_edges:
                st.write(f"  {u} ←→ {v} : {w}")
        
        st.divider()
        st.subheader("Edit Graph")
        
        # Add Node
        if st.button("Add Node", use_container_width=True, key="add_node_btn"):
            existing_nodes = graph.get_all_cities()
            new_node = max(existing_nodes) + 1 if existing_nodes else 0
            graph.add_city(new_node)
            st.success(f"Node {new_node} added")
            st.rerun()
        
        # Add Edge
        st.write("**Add Edge:**")
        col_a, col_b = st.columns(2)
        with col_a:
            edge_from = st.number_input("From", min_value=0, key="edge_from", step=1)
        with col_b:
            edge_to = st.number_input("To", min_value=0, key="edge_to", step=1)
        edge_weight = st.number_input("Weight", min_value=1, value=5, key="edge_weight", step=1)
        
        if st.button("Add Edge", use_container_width=True, key="add_edge_btn"):
            if edge_from != edge_to:
                graph.add_road(edge_from, edge_to, edge_weight)
                st.success(f"Edge {edge_from} ↔ {edge_to} added")
                if 'mst_result' in st.session_state:
                    del st.session_state.mst_result
                st.rerun()
            else:
                st.warning("Cannot add edge to same node")
    
    with col1:
        st.subheader("Network Graph")
        mst_edges_to_highlight = st.session_state.get('mst_result', ([], 0))[0]
        render_graph_with_pyvis(graph, height=500, mst_edges=mst_edges_to_highlight)

# ============================================================================
# PAGE: Q2 - PATH FINDER
# ============================================================================
elif page == "Q2: Path Finder":
    st.header("Q2: Shortest Path & K-Disjoint Paths")
    create_algorithm_info_panel("Dijkstra")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("Find Paths")
        
        all_cities = sorted(graph.get_all_cities())
        
        start = st.selectbox("From", all_cities, key="path_start")
        end = st.selectbox("To", all_cities, key="path_end", index=min(1, len(all_cities)-1))
        
        if start != end:
            if st.button("Shortest Path", use_container_width=True):
                path, dist = dijkstra_shortest_path(graph, start, end)
                st.session_state.shortest_path = (path, dist)
            
            k = st.number_input("# Disjoint Paths", 1, 5, 2, key="k")
            if st.button("K-Disjoint Paths", use_container_width=True):
                paths = find_k_disjoint_paths(graph, start, end, k)
                st.session_state.disjoint_paths = paths
        
        if 'shortest_path' in st.session_state:
            path, dist = st.session_state.shortest_path
            st.success("Shortest Path Found")
            st.write(f"Path: {' → '.join(map(str, path))}")
            st.metric("Distance", dist)
        
        if 'disjoint_paths' in st.session_state:
            paths = st.session_state.disjoint_paths
            st.success(f"{len(paths)} Disjoint Paths Found")
            for i, p in enumerate(paths, 1):
                st.write(f"Path {i}: {' → '.join(map(str, p))}")

# ============================================================================
# PAGE: Q3 - TREE OPTIMIZER
# ============================================================================
elif page == "Q3: Tree Optimizer":
    st.header("Q3: AVL Tree Rebalancing")
    create_algorithm_info_panel("AVL Rebalance")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.subheader("Original Tree")
        visualize_tree(command_tree, "before")
        analysis_before = analyze_tree_balance(command_tree)
        st.metric("Height", analysis_before['height'])
        st.metric("Balanced?", "Yes" if analysis_before['is_balanced'] else "No")
    
    with col2:
        st.subheader("Controls")
        st.write("")
        if st.button("Rebalance", use_container_width=True, key="rebal"):
            balanced = rebalance_tree(command_tree)
            st.session_state.balanced_tree = balanced
            st.success("Rebalancing complete!")
    
    with col3:
        st.subheader("Balanced Tree")
        if 'balanced_tree' in st.session_state:
            visualize_tree(st.session_state.balanced_tree, "after")
            analysis_after = analyze_tree_balance(st.session_state.balanced_tree)
            st.metric("Height", analysis_after['height'])
            st.metric("Balanced?", "Yes" if analysis_after['is_balanced'] else "No")

# ============================================================================
# PAGE: Q4 - FAILURE SIMULATION
# ============================================================================
elif page == "Q4: Failure Simulation":
    st.header("Q4: Network Failure Simulation")
    create_algorithm_info_panel("Failure Analysis")
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col1:
        st.subheader("Network")
        render_graph_with_pyvis(graph, height=400)
    
    with col2:
        st.subheader("Test Failure")
        
        all_cities = sorted(graph.get_all_cities())
        failed = st.selectbox("Fail City", all_cities, key="fail_city")
        
        if st.button("Simulate", use_container_width=True):
            analyzer = FailureAnalyzer(graph)
            result = analyzer.analyze_node_failure(failed)
            st.session_state.failure_result = result
    
    with col3:
        if 'failure_result' in st.session_state:
            result = st.session_state.failure_result
            st.subheader("Impact")
            st.metric("Affected Nodes", len(result['affected_nodes']))
            st.metric("Disconnected", len(result['disconnected_nodes']))
            impact = (len(result['disconnected_nodes']) / len(all_cities) * 100) if all_cities else 0
            st.metric("Impact %", f"{impact:.1f}%")

# ============================================================================
# PAGE: Q5 - GRAPH COLORING
# ============================================================================
elif page == "Q5: Graph Coloring":
    st.header("Q5: Graph Coloring (Bonus)")
    create_algorithm_info_panel("Graph Coloring")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("Compute Coloring")
        
        if st.button("Color Graph", use_container_width=True):
            coloring, chromatic = greedy_graph_coloring(graph)
            is_valid, violations = validate_coloring(graph, coloring)
            analysis = analyze_coloring_efficiency(graph, coloring)
            st.session_state.coloring = (coloring, chromatic, is_valid)
        
        if 'coloring' in st.session_state:
            coloring, chromatic, is_valid = st.session_state.coloring
            st.success("Coloring Complete")
            st.metric("Colors Used", chromatic)
            st.metric("Valid?", "Yes" if is_valid else "No")
            
            st.divider()
            for city in sorted(coloring.keys()):
                st.write(f"City {city}: Color {coloring[city]}")

st.divider()
st.markdown("**Emergency Network Simulator** | All algorithms implemented from scratch")
