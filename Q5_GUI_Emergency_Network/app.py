"""
Question 5 - Emergency Network Simulator: Interactive GUI Application

Problem Overview:
This is the main Streamlit application providing an interactive web-based interface
for the Emergency Communication & Response Network simulator. The GUI allows users to:
- Visualize the network graph with interactive node placement
- Execute and visualize algorithms (MST, shortest paths, tree rebalancing, etc.)
- Simulate network failures and analyze impact
- Edit the graph structure in real-time
- View algorithm results and performance metrics

Approach:
I used Streamlit for rapid web app development with Python. The application is organized
into multiple pages accessed via sidebar navigation:
- Dashboard: Main graph visualization and editing
- Q1: MST computation and visualization
- Q2: Path finding (Dijkstra, K-disjoint paths)
- Q3: Tree rebalancing and balance analysis
- Q4: Failure simulation and resilience testing
- Q5: Graph coloring for frequency assignment

The app uses session state to persist graph and tree data across page navigations,
and Pyvis for interactive network visualization with physics simulation.

Key Features:
- Real-time graph editing
- Interactive visualization
- Algorithm execution and results display
- Performance metrics and statistics
"""

# Emergency Network Simulator - Interactive GUI
import streamlit as st
import pandas as pd
from graph.graph_model import EmergencyGraph
from graph.mst import kruskal_mst
from graph.paths import find_k_disjoint_paths, dijkstra_shortest_path
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
# PAGE: Q2 - DISJOINT PATH FINDER
# ============================================================================
elif page == "Q2: Path Finder":
    st.header("Q2: K-Disjoint Paths")
    create_algorithm_info_panel("Disjoint Path Finder")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("Find Disjoint Paths")
        
        all_cities = sorted(graph.get_all_cities())
        
        start = st.selectbox("From", all_cities, key="path_start")
        end = st.selectbox("To", all_cities, key="path_end", index=min(1, len(all_cities)-1))
        
        if start != end:
            k = st.number_input("# Disjoint Paths", 1, 5, 2, key="k")
            if st.button("Find K-Disjoint Paths", use_container_width=True):
                paths = find_k_disjoint_paths(graph, start, end, k)
                st.session_state.disjoint_paths = paths
        
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
    
    st.markdown("""
    **Objective:** Optimize the command hierarchy tree to minimize communication latency.
    
    **Algorithm:** AVL Tree Rebalancing
    - Performs rotations to maintain balance
    - Minimizes the longest path from HQ to any command center
    - Time Complexity: O(log n) per operation
    """)
    
    st.divider()
    
    # Before optimization
    st.subheader("Current Tree Structure")
    
    col_before, col_info = st.columns([2, 1])
    
    with col_before:
        visualize_tree(command_tree, "Original Command Hierarchy")
    
    with col_info:
        analysis_before = analyze_tree_balance(command_tree)
        st.metric("Height", analysis_before['height'])
        st.metric("Balanced?", "Yes" if analysis_before['is_balanced'] else "No")
        
        if not analysis_before['is_balanced']:
            st.warning("Tree is unbalanced - optimize to improve performance")
    
    st.divider()
    
    # Optimization button
    st.subheader("Optimization")
    
    col_btn = st.columns([1, 3])[0]
    with col_btn:
        if st.button("Optimize (Rebalance)", use_container_width=True, key="rebal"):
            with st.spinner("Rebalancing tree..."):
                balanced = rebalance_tree(command_tree)
                st.session_state.balanced_tree = balanced
                st.session_state.optimization_done = True
            st.success("Rebalancing complete!")
    
    # After optimization
    if st.session_state.get('optimization_done'):
        st.divider()
        st.subheader("Optimized Tree Structure")
        
        col_after, col_info2 = st.columns([2, 1])
        
        with col_after:
            visualize_tree(st.session_state.balanced_tree, "Optimized Command Hierarchy")
        
        with col_info2:
            analysis_after = analyze_tree_balance(st.session_state.balanced_tree)
            st.metric("Height", analysis_after['height'])
            st.metric("Balanced?", "✓ Yes" if analysis_after['is_balanced'] else "✗ No")
            
            height_reduction = analysis_before['height'] - analysis_after['height']
            if height_reduction > 0:
                st.success(f"📉 Height reduced by {height_reduction}")
        
        # Comparison
        st.divider()
        st.subheader("Before vs After Comparison")
        
        comparison_data = {
            "Metric": ["Height", "Balanced", "Max Path Length"],
            "Before": [
                analysis_before['height'],
                "Yes" if analysis_before['is_balanced'] else "No",
                analysis_before['height']
            ],
            "After": [
                analysis_after['height'],
                "Yes" if analysis_after['is_balanced'] else "No",
                analysis_after['height']
            ]
        }
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
        
        st.markdown("""
        **Impact:** 
        - Reduced tree height improves communication latency
        - Balanced tree ensures fair distribution of command paths
        - All nodes are at most ⌈log₂(n)⌉ levels from HQ
        """)

# ============================================================================
# PAGE: Q4 - FAILURE SIMULATION
# ============================================================================
elif page == "Q4: Failure Simulation":
    st.header("Q4: Network Failure Simulation")
    create_algorithm_info_panel("Failure Analysis")
    
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    
    with col1:
        st.subheader("Network")
        highlight_nodes = None
        if 'failure_result' in st.session_state:
            result = st.session_state.failure_result
            highlight_nodes = {}
            failed_node = result.get('failed_node')
            if failed_node is not None:
                highlight_nodes[failed_node] = '#808080'  # Failed node in grey

        render_graph_with_pyvis(graph, height=400, highlight_nodes=highlight_nodes)
    
    with col2:
        st.subheader("Test Failure")
        
        all_cities = sorted(graph.get_all_cities())
        start_node = st.selectbox("Start", all_cities, key="start_city")
        goal_node = st.selectbox("Goal", all_cities, key="goal_city", index=min(1, len(all_cities) - 1))
        failed = st.selectbox("Fail City", all_cities, key="fail_city")
        
        if st.button("Simulate", use_container_width=True):
            analyzer = FailureAnalyzer(graph)
            result = analyzer.analyze_node_failure(failed)
            st.session_state.failure_result = result

            # Shortest path before failure
            path_before, dist_before = dijkstra_shortest_path(graph, start_node, goal_node)

            # Shortest path after failure
            graph.disable_city(failed)
            path_after, dist_after = dijkstra_shortest_path(graph, start_node, goal_node)
            graph.enable_city(failed)

            # Baseline shortest paths from Start
            baseline_paths = {}
            baseline_distances = {}
            for city in all_cities:
                if city == start_node:
                    continue
                path, dist = dijkstra_shortest_path(graph, start_node, city)
                baseline_paths[city] = path
                baseline_distances[city] = dist

            # Recomputed shortest paths after failure
            graph.disable_city(failed)
            new_paths = {}
            new_distances = {}
            for city in all_cities:
                if city == start_node or city == failed:
                    continue
                path, dist = dijkstra_shortest_path(graph, start_node, city)
                new_paths[city] = path
                new_distances[city] = dist
            graph.enable_city(failed)

            st.session_state.failure_paths = {
                'start': start_node,
                'goal': goal_node,
                'failed': failed,
                'path_before': path_before,
                'dist_before': dist_before,
                'path_after': path_after,
                'dist_after': dist_after,
                'baseline_paths': baseline_paths,
                'baseline_distances': baseline_distances,
                'new_paths': new_paths,
                'new_distances': new_distances
            }
    
    with col3:
        if 'failure_result' in st.session_state:
            result = st.session_state.failure_result
            st.subheader("Impact")
            st.metric("Affected Nodes", len(result['affected_nodes']))
            st.metric("Disconnected", len(result.get('isolated_nodes', [])))
            impact = result.get('connectivity_loss', 0)
            st.metric("Impact %", f"{impact:.1f}%")

            if 'failure_paths' in st.session_state:
                path_info = st.session_state.failure_paths
                baseline_distances = path_info['baseline_distances']
                new_distances = path_info['new_distances']
                baseline_paths = path_info['baseline_paths']
                new_paths = path_info['new_paths']
                failed = path_info['failed']
                start_node = path_info['start']
                goal_node = path_info['goal']

                rows = []
                total_increase = 0
                increase_count = 0

                for city in all_cities:
                    if city == start_node or city == failed:
                        continue
                    base = baseline_distances.get(city, float('inf'))
                    new = new_distances.get(city, float('inf'))
                    base_path = baseline_paths.get(city)
                    new_path = new_paths.get(city)

                    if new == float('inf'):
                        status = "Disconnected"
                        increase = "∞"
                    else:
                        status = "Connected"
                        if base == float('inf'):
                            increase = "N/A"
                        else:
                            delta = new - base
                            increase = delta
                            total_increase += max(delta, 0)
                            increase_count += 1

                    rows.append({
                        "City": city,
                        "Baseline Path": " → ".join(map(str, base_path)) if base_path else "N/A",
                        "Baseline Distance": "∞" if base == float('inf') else base,
                        "New Path": " → ".join(map(str, new_path)) if new_path else "Disconnected",
                        "New Distance": "∞" if new == float('inf') else new,
                        "Increase": increase,
                        "Status": status
                    })

                st.divider()
                st.subheader("Recomputed Shortest Paths (from Start)")
                st.dataframe(pd.DataFrame(rows), use_container_width=True)

                if increase_count > 0:
                    avg_increase = total_increase / increase_count
                    st.metric("Avg. Increase in Delivery Time", f"{avg_increase:.2f}")

    # Shortest path canvas
    if 'failure_paths' in st.session_state:
        path_info = st.session_state.failure_paths
        path_after = path_info.get('path_after')
        start_node = path_info['start']
        goal_node = path_info['goal']
        failed = path_info['failed']

        st.divider()
        st.subheader("Shortest Path After Failure")

        highlight_nodes = {
            failed: '#808080'  # Failed node in grey
        }

        highlight_edges = []
        if path_after and len(path_after) > 1:
            highlight_edges = list(zip(path_after[:-1], path_after[1:]))

        render_graph_with_pyvis(
            graph,
            height=450,
            highlight_nodes=highlight_nodes,
            highlight_edges=highlight_edges
        )

        if path_after is None:
            st.warning("No available path after failure.")

# ============================================================================
# PAGE: Q5 - GRAPH COLORING
# ============================================================================
elif page == "Q5: Graph Coloring":
    st.header("Q5: Graph Coloring - Frequency Assignment")
    
    st.markdown("""
    **Objective:** Assign frequencies to communication hubs such that no adjacent hubs use the same channel.
    
    **Algorithm:** Greedy Graph Coloring
    - Ensures no two adjacent nodes share the same frequency
    - Minimizes interference in the communication network
    - Time Complexity: O(V + E)
    """)
    
    st.divider()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Network Graph")
        render_graph_with_pyvis(graph, height=500)
    
    with col2:
        st.subheader("Assign Frequencies")
        
        if st.button("Color Graph", use_container_width=True):
            coloring, chromatic = greedy_graph_coloring(graph)
            is_valid, violations = validate_coloring(graph, coloring)
            analysis = analyze_coloring_efficiency(graph, coloring)
            st.session_state.coloring = (coloring, chromatic, is_valid)
            st.rerun()
        
        if 'coloring' in st.session_state:
            coloring, chromatic, is_valid = st.session_state.coloring
            st.success("Coloring Complete")
            st.metric("Frequencies Used", chromatic)
            st.metric("Valid?", "Yes" if is_valid else "No")
            
            st.divider()
            st.write("**Frequency Assignment:**")
            for city in sorted(coloring.keys()):
                st.write(f"Hub {city}: Frequency {coloring[city] + 1}")
    
    # Colored graph visualization
    if 'coloring' in st.session_state:
        st.divider()
        st.subheader("📡 Frequency-Colored Network")
        
        coloring, chromatic, is_valid = st.session_state.coloring
        
        # Color palette for frequencies (similar to reference image)
        frequency_colors = [
            '#E74C3C',  # Red - Frequency 1
            '#3498DB',  # Blue - Frequency 2
            '#2ECC71',  # Green - Frequency 3
            '#F39C12',  # Orange - Frequency 4
            '#9B59B6',  # Purple - Frequency 5
            '#1ABC9C',  # Teal - Frequency 6
            '#E67E22',  # Dark Orange - Frequency 7
            '#34495E',  # Dark Gray - Frequency 8
        ]
        
        # Map nodes to colors
        node_colors = {}
        for node, color_idx in coloring.items():
            node_colors[node] = frequency_colors[color_idx % len(frequency_colors)]
        
        render_graph_with_pyvis(graph, height=500, node_colors=node_colors)
        
        # Frequency legend
        st.divider()
        st.subheader("Frequency Legend")
        
        legend_cols = st.columns(min(chromatic, 4))
        for i in range(chromatic):
            with legend_cols[i % 4]:
                color = frequency_colors[i % len(frequency_colors)]
                st.markdown(f"""
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="width: 30px; height: 30px; background-color: {color}; border-radius: 50%;"></div>
                    <span style="font-size: 16px;"><b>Frequency {i + 1}</b></span>
                </div>
                """, unsafe_allow_html=True)
                st.write("")

st.divider()
st.markdown("**Emergency Network Simulator** | All algorithms implemented from scratch")
