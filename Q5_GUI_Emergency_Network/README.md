# Emergency Network Simulator - Advanced Algorithm Design Project

## Overview
Interactive GUI-based tool for simulating and optimizing a national Emergency Communication & Response System using advanced algorithmic techniques. **All algorithms are implemented from scratch without external algorithm libraries.**

## Project Scope
- **Q1 [6 marks]:** Dynamic MST Visualization - Kruskal's Algorithm
- **Q2 [5 marks]:** Reliable Path Finder - Dijkstra + K-Disjoint Paths
- **Q3 [4 marks]:** Command Hierarchy Optimizer - AVL Tree Rebalancing
- **Q4 [5 marks]:** Failure Simulation & Rerouting - Network Impact Analysis
- **Bonus [+2 marks]:** Graph Coloring - Frequency Assignment
- **Total: 20 marks + 2 bonus**

## Features Implemented

### 1. Graph Algorithms (No External Libraries)
- **Kruskal's MST Algorithm** - O(E log E) time complexity
- **Dijkstra's Shortest Path** - O(V²) time complexity  
- **K-Disjoint Paths** - Max-flow based, O(K × (V + E))
- **Graph Coloring** - Welsh-Powell greedy, O(V² + E)
- **BFS/DFS** - For connectivity analysis

### 2. Tree Algorithms
- **Binary Search Tree** - Basic BST operations
- **AVL Tree** - Self-balancing with rotations, O(log n) guaranteed
- **Tree Rebalancing** - Converts unbalanced BST to balanced AVL
- **Height Analysis** - Measures communication path lengths

### 3. Network Analysis
- **Failure Simulation** - Node and edge failure analysis
- **Cascade Failure Detection** - Multi-phase failure propagation
- **Path Reliability Calculation** - Probability-based path assessment
- **Connectivity Metrics** - Network robustness measurement

## Installation & Usage

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the Streamlit Application
```bash
streamlit run app.py
```

### 3. Run Tests (Comprehensive Test Suite)
```bash
# Test individual modules
python -m pytest tests/test_mst.py -v
python -m pytest tests/test_paths.py -v
python -m pytest tests/test_failure.py -v
python -m pytest tests/test_coloring.py -v

# Or run all tests
python -m pytest tests/ -v

# Or run test files directly
python tests/test_mst.py
python tests/test_paths.py
python tests/test_failure.py
python tests/test_coloring.py
```

## Code Organization

```
Q5_GUI_Emergency_Network/
├── app.py                 # Main Streamlit GUI application
├── requirements.txt       # Package dependencies (Streamlit only)
├── README.md             # This file
│
├── graph/
│   ├── graph_model.py    # EmergencyGraph data structure
│   ├── mst.py            # Kruskal's MST implementation
│   ├── paths.py          # Dijkstra, BFS, K-Disjoint Paths
│   ├── failure.py        # Failure simulation & analysis
│   └── coloring.py       # Graph coloring algorithm
│
├── tree/
│   ├── tree_model.py     # Binary Search Tree
│   └── rebalance.py      # AVL Tree & rebalancing
│
├── utils/
│   ├── metrics.py        # Algorithm & graph metrics
│   └── visualization.py  # Streamlit visualization functions
│
└── tests/
    ├── test_mst.py       # MST algorithm tests (6 test cases)
    ├── test_paths.py     # Path finding tests (9 test cases)
    ├── test_failure.py   # Failure analysis tests (10 test cases)
    └── test_coloring.py  # Graph coloring tests (10 test cases)
```

## Algorithm Details

### Q1: Kruskal's Minimum Spanning Tree
**Time Complexity:** O(E log E)  
**Space Complexity:** O(V + E)

**Algorithm:**
1. Sort edges by weight
2. Initialize Union-Find for n vertices
3. For each edge in sorted order:
   - If endpoints are in different components, add edge to MST
   - Union the two components
4. Return MST when V-1 edges collected

**Why Greedy Works:** At each step, selecting minimum weight edge that doesn't create cycle guarantees global optimum.

### Q2: Dijkstra's Shortest Path & K-Disjoint Paths
**Dijkstra - Time:** O(V²) array-based, O((V+E) log V) with heap  
**K-Disjoint - Time:** O(K × (V + E)) - uses Ford-Fulkerson method

**Dijkstra Algorithm:**
1. Initialize distances: source=0, others=∞
2. While unvisited nodes exist:
   - Select unvisited with minimum distance
   - Update neighbors' distances
   - Mark as visited

**K-Disjoint Paths:**
- Uses residual graph technique from max-flow
- Each iteration finds augmenting path
- Reduces edge capacities along path
- Guarantees edge-disjoint paths

### Q3: AVL Tree Rebalancing
**Time Complexity:** O(log n) per operation after rebalancing  
**Space Complexity:** O(n) tree + O(log n) recursion stack

**Balance Factor:** height(left) - height(right), must be in [-1, 0, 1]

**Rotations (4 cases):**
- LL (Left-Left): Single right rotation
- RR (Right-Right): Single left rotation  
- LR (Left-Right): Left rotation, then right rotation
- RL (Right-Left): Right rotation, then left rotation

**Rebalancing Process:**
1. Insert/delete normally in BST
2. Update heights bottom-up
3. Check balance factors
4. Perform rotations if needed
5. Guarantees O(log n) tree height

### Q4: Failure Simulation & Analysis
**Algorithm:**
1. Disable target node in graph
2. Recompute shortest paths between all pairs
3. Count lost connections
4. Identify isolated subnetworks
5. Re-enable node (non-destructive)

**Cascade Failure:**
- Iterative algorithm with connectivity threshold
- Nodes fail if connectivity drops below 30%
- Each iteration identifies newly failing nodes
- Continues until stable state reached

### Bonus: Graph Coloring (Welsh-Powell Heuristic)
**Time Complexity:** O(V² + E)  
**Space Complexity:** O(V)

**Algorithm:**
1. Sort vertices by degree (descending)
2. For each vertex in order:
   - Find colors used by adjacent vertices
   - Assign smallest available color
3. Return coloring and chromatic number

**Properties:**
- Always produces valid coloring
- Near-optimal for many graphs
- Used for frequency/channel assignment

## Test Coverage

### Test Statistics
- **MST Tests:** 7 test cases covering basic, edge cases, and large graphs
- **Path Tests:** 9 test cases for shortest paths, disjoint paths, and reliability
- **Failure Tests:** 10 test cases for node failures, cascades, and recovery
- **Coloring Tests:** 10 test cases for valid colorings and efficiency

### Sample Test Output
```
✓ test_kruskal_basic passed
✓ test_dijkstra_basic passed
✓ test_k_disjoint_paths passed
✓ test_node_failure_simple passed
✓ test_greedy_coloring_basic passed
...
✅ All tests passed!
```

## Streamlit Features

### Interactive Modules
1. **Dashboard:** Network statistics and configuration
2. **MST Visualization:** Real-time MST computation with metrics
3. **Path Finder:** Multi-path computation and reliability analysis
4. **Command Hierarchy:** Tree optimization with before/after visualization
5. **Failure Simulation:** Node failure impact assessment
6. **Graph Coloring:** Frequency assignment with efficiency analysis

### Visualizations
- Graph topology as editable tables
- MST edge lists with total weight metrics
- Path rendering with hop counts
- Tree structure with height metrics
- Failure impact heatmaps
- Coloring with frequency bands

## Coding Standards

### Code Quality
✓ Well-commented with algorithm explanations  
✓ Clear variable naming following conventions  
✓ Consistent indentation and formatting  
✓ Time complexity documented for each function  
✓ Comprehensive docstrings  

### No External Algorithm Libraries
- ✗ No NetworkX for graph algorithms
- ✗ No NumPy for numerical operations
- ✗ No SciPy for scientific computing
- ✓ Only Streamlit for GUI rendering

### Testing & Validation
- 36+ test cases across all modules
- Edge case handling (empty graphs, single nodes, disconnected)
- Multiple input variations
- Performance on large graphs (10+ nodes)

## Complexity Analysis Summary

| Algorithm | Time | Space | Notes |
|-----------|------|-------|-------|
| Kruskal MST | O(E log E) | O(V + E) | Dominated by sorting |
| Dijkstra | O(V²) | O(V) | Array-based implementation |
| Dijkstra (heap) | O((V+E) log V) | O(V) | Requires priority queue |
| BFS | O(V + E) | O(V) | Unweighted or unit-weight |
| K-Disjoint Paths | O(K(V+E)) | O(V + E) | Ford-Fulkerson approach |
| Graph Coloring | O(V² + E) | O(V) | Welsh-Powell heuristic |
| AVL Rebalance | O(log n) | O(log n) | Per operation amortized |
| Failure Analysis | O(V²) | O(V) | Per node simulation |

## Future Enhancements

1. **Visualization Improvements**
   - Graph layout algorithms (force-directed)
   - Animated algorithm execution
   - 3D network visualization

2. **Additional Algorithms**
   - Floyd-Warshall all-pairs shortest paths
   - Prim's MST algorithm
   - A* pathfinding

3. **Performance Optimization**
   - Fibonacci heaps for Dijkstra
   - Better heuristics for graph coloring
   - Parallel failure analysis

4. **Real-World Data**
   - Load from CSV/JSON
   - Geographic coordinate visualization
   - Actual infrastructure data

## Author Notes

This implementation prioritizes:
1. **Algorithm Clarity** - Raw implementations with clear logic flow
2. **Educational Value** - Detailed comments and complexity analysis
3. **Comprehensive Testing** - 36+ test cases covering edge cases
4. **Code Quality** - Professional structure and documentation
5. **Functionality** - All requirements fully implemented

## License
Academic Project - Coventry University Advanced Algorithms (Semester 4)

## Contact & Support
For questions or issues, refer to the inline code documentation and test cases.

---
**Submission Date:** [Current Date]  
**Project Status:** ✅ Complete - All 5 core questions + Bonus implemented
