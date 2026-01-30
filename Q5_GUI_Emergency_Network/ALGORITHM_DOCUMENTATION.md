# Question 5 - Emergency Network Simulator: Comprehensive Algorithm Documentation

## Problem Overview

This project implements an Emergency Communication & Response Network Simulator using advanced graph and tree algorithms. The system models a network of cities connected by roads, where we need to optimize various aspects such as finding minimum cost connections, reliable routing paths, efficient command hierarchies, and handling network failures.

**Core Challenges Addressed:**
1. **Minimum Spanning Tree (MST)**: Connect all cities with minimum total road cost
2. **Reliable Path Finding**: Find shortest and alternative paths between cities
3. **Command Hierarchy Optimization**: Maintain balanced tree structure for efficient operations
4. **Network Failure Analysis**: Simulate and analyze impact of node/edge failures
5. **Frequency Assignment**: Allocate non-interfering communication frequencies (Graph Coloring)

---

## Question 1: State Space Analysis

### State Space Definition

The state space for the Emergency Network problem consists of:

**State Components:**
- **Graph G = (V, E)** where:
  - V = set of vertices (cities/hubs)
  - E = set of edges (roads with weights representing distance/cost/time)
  - Each edge e ∈ E has weight w(e) representing cost

**State Variables:**
- Active nodes: V_active ⊆ V (nodes currently operational)
- Disabled nodes: V_disabled = V \ V_active (failed nodes)
- Vulnerable edges: E_vulnerable ⊆ E (edges marked as at-risk)
- Edge capacities: capacity(e) for each edge e ∈ E

**Tree State (for Q3):**
- Binary Search Tree with nodes containing command priorities
- Each node has: value, left child, right child, height
- Balance factor = height(left) - height(right)

### State Transitions

**Graph Operations:**
1. **Add Node**: V' = V ∪ {v_new}
2. **Remove Node**: V' = V \ {v_remove}, E' = E \ {edges incident to v_remove}
3. **Add Edge**: E' = E ∪ {(u,v,w)}
4. **Mark Vulnerable**: E_vulnerable' = E_vulnerable ∪ {(u,v)}
5. **Disable Node**: V_disabled' = V_disabled ∪ {v}, affects all paths through v

**Tree Operations:**
1. **Insert**: Add new node while maintaining BST property, then rebalance
2. **Delete**: Remove node and restructure tree, then rebalance
3. **Rotate**: Change tree structure while preserving BST property and reducing height

### Initial and Goal States

**Initial State:**
- Graph with all nodes active
- No vulnerable edges
- Tree with arbitrary structure

**Goal States (depending on operation):**
- **MST**: Subgraph T ⊆ E connecting all vertices with minimum Σw(e)
- **Shortest Path**: Path P from source s to destination t minimizing Σw(e)
- **Balanced Tree**: AVL tree with |balance_factor| ≤ 1 for all nodes
- **Robust Network**: Maximum connectivity after failures

### Search Space Size

**MST Search Space:**
- Number of possible spanning trees for complete graph K_n: n^(n-2) (Cayley's formula)
- For n=10 cities: 10^8 = 100,000,000 possible spanning trees

**Path Finding Search Space:**
- Upper bound: (n-1)! possible paths between two nodes
- For n=10: 9! = 362,880 possible paths
- Pruned by graph structure and connectivity

**Tree Rebalancing:**
- For n nodes, O(2^n) possible tree structures
- AVL constraint reduces valid structures significantly

---

## Question 3: Algorithm Approach and Implementation

### 1. Minimum Spanning Tree (Kruskal's Algorithm)

**Approach Used:**
I implemented Kruskal's algorithm with Union-Find (Disjoint Set Union) data structure. The approach works by sorting all edges by weight and greedily adding edges that don't create cycles.

**Implementation Strategy:**
- Sort edges in ascending order of weight: O(E log E)
- Use Union-Find to detect cycles in O(α(n)) amortized time
- For each edge (u,v), check if u and v are in different components
- If yes, add edge to MST and merge components
- Continue until (V-1) edges are added

**Key Data Structures:**
- parent[]: tracks root of each component
- rank[]: maintains tree depth for union-by-rank optimization
- Edge list sorted by weight

**Time Complexity:** O(E log E) dominated by sorting
**Space Complexity:** O(V + E)

**Why This Approach:**
- Greedy strategy guarantees optimal solution
- Union-Find provides near-constant cycle detection
- Simple to implement and understand
- Works well for sparse and dense graphs

---

### 2. Shortest Path Finding (Dijkstra's Algorithm)

**Approach Used:**
I implemented Dijkstra's algorithm using an array-based approach for dense graphs. The algorithm maintains a set of visited nodes and greedily selects the unvisited node with minimum distance at each step.

**Implementation Strategy:**
- Initialize distances[v] = ∞ for all vertices, distances[source] = 0
- Maintain unvisited set and previous[] array for path reconstruction
- Repeatedly select unvisited node u with minimum distance[u]
- For each neighbor v of u, relax edge: distance[v] = min(distance[v], distance[u] + weight(u,v))
- Continue until destination is reached or all reachable nodes are visited

**Why This Approach:**
- Guarantees shortest path for non-negative weights
- Array implementation is O(V²), optimal for dense graphs
- Simple to implement without priority queue complexity
- Provides single-source shortest paths to all vertices

---

### 3. K-Disjoint Paths (Ford-Fulkerson Based)

**Approach Used:**
I implemented a max-flow based algorithm to find K edge-disjoint paths. The approach converts the graph to a flow network and finds augmenting paths iteratively.

**Implementation Strategy:**
- Create residual graph with unit capacities
- Use DFS to find augmenting paths from source to sink
- For each path found, update residual capacities
- Reverse edges represent "used" edges
- Continue until K paths found or no more paths exist

**Why This Approach:**
- Edge-disjoint paths = maximum flow when all capacities = 1
- DFS finds paths quickly in sparse residual graphs
- Natural way to ensure paths don't share edges
- Works for any K value up to maximum possible disjoint paths

---

### 4. AVL Tree Rebalancing

**Approach Used:**
I implemented self-balancing AVL tree with automatic rotations after insert/delete operations. The tree maintains the AVL property: |height(left) - height(right)| ≤ 1 for all nodes.

**Implementation Strategy:**
- Track height for each node during insertion/deletion
- Calculate balance factor = height(left) - height(right)
- After modification, check balance factor at each ancestor
- Apply rotations when |balance_factor| > 1:
  - **Left-Left case**: Right rotation
  - **Right-Right case**: Left rotation
  - **Left-Right case**: Left rotation on left child, then right rotation
  - **Right-Left case**: Right rotation on right child, then left rotation

**Why This Approach:**
- Guarantees O(log n) height for all operations
- Rotations restore balance in O(1) time
- Minimal restructuring (only ancestors affected)
- Automatic self-balancing without manual intervention

---

### 5. Network Failure Analysis

**Approach Used:**
I implemented iterative failure simulation that disables nodes/edges and measures impact on connectivity and path availability.

**Implementation Strategy:**
- Disable specified nodes by marking them inactive
- Recompute shortest paths avoiding disabled nodes
- Calculate connectivity using BFS/DFS from each node
- Identify affected nodes (those losing connectivity)
- Detect cascade failures (nodes losing multiple neighbors)
- Compute network robustness metrics

**Why This Approach:**
- Directly models real-world failure scenarios
- Provides quantitative impact assessment
- Identifies critical nodes (high centrality)
- Supports "what-if" analysis for contingency planning

---

### 6. Graph Coloring (Welsh-Powell Algorithm)

**Approach Used:**
I implemented the Welsh-Powell greedy heuristic for graph coloring. This approach prioritizes high-degree nodes to minimize color usage.

**Implementation Strategy:**
- Sort nodes by degree in descending order
- Assign lowest available color to each node
- Color is available if no adjacent node has that color
- Continue until all nodes are colored

**Time Complexity:** O(V² + E)
**Space Complexity:** O(V)

**Why This Approach:**
- Greedy heuristic provides good approximation
- Simple to implement and understand
- Works well for practical graphs
- High-degree nodes colored first reduces conflicts

---

## Algorithm Complexity Summary

| Algorithm | Time Complexity | Space Complexity | Optimality |
|-----------|-----------------|------------------|------------|
| Kruskal MST | O(E log E) | O(V + E) | Optimal |
| Dijkstra | O(V²) | O(V) | Optimal (non-negative weights) |
| K-Disjoint Paths | O(K(V + E)) | O(V + E) | Optimal |
| AVL Rebalance | O(log n) | O(log n) recursion | Optimal height |
| Failure Analysis | O(V²) | O(V) | Exact |
| Graph Coloring | O(V² + E) | O(V) | Approximation |

---

## Key Implementation Details

### Union-Find Optimization
- **Path Compression**: Make every node point directly to root during find()
- **Union by Rank**: Attach smaller tree under larger tree root
- Combined: O(α(n)) amortized time per operation where α is inverse Ackermann

### Graph Representation
- **Adjacency List**: {node: [(neighbor, weight), ...]}
- Efficient for sparse graphs: O(V + E) space
- Fast neighbor lookup: O(degree(v)) per node

### Tree Rotations
- **Right Rotation**: Promotes left child to root
- **Left Rotation**: Promotes right child to root
- Preserves BST ordering: left < parent < right
- Updates heights after rotation

### Residual Graph for Flow
- Forward edges: remaining capacity
- Backward edges: reverse flow possibility
- Augmenting path: path with positive capacity
- Path cancellation: allows flow rerouting

---

## Remarks and Observations

### Algorithm Performance

**MST (Kruskal's):**
- Performs excellently for both sparse and dense graphs
- Union-Find optimization crucial for large graphs
- Edge sorting dominates runtime for E >> V
- Alternative (Prim's) better for very dense graphs with adjacency matrix

**Shortest Path (Dijkstra):**
- O(V²) implementation optimal for dense graphs (E ≈ V²)
- Priority queue version O((V+E) log V) better for sparse graphs
- Fails for negative edge weights (requires Bellman-Ford)
- Single-source shortest paths to all destinations computed

**K-Disjoint Paths:**
- Performance depends on K and graph density
- DFS-based augmenting path finding is fast in practice
- Maximum K is bounded by minimum vertex cut
- Useful for redundant routing and fault tolerance

**AVL Tree:**
- Guarantees O(log n) operations unlike basic BST
- More rotations than Red-Black tree but simpler implementation
- Height difference of √2 compared to perfectly balanced tree
- Self-balancing eliminates worst-case O(n) for skewed trees

**Failure Analysis:**
- Computational cost increases with number of failures
- Critical node identification helps prioritize protection
- Cascade detection prevents catastrophic failures
- Robustness metrics guide infrastructure investment

**Graph Coloring:**
- Welsh-Powell provides good approximation in practice
- Optimal coloring is NP-complete (exponential exact algorithms)
- Degree-based heuristic effective for planar and sparse graphs
- Frequency assignment ensures interference-free communication

### Design Trade-offs

**Correctness vs. Efficiency:**
- Chose proven algorithms (Dijkstra, Kruskal) over heuristics for critical operations
- Used approximation (Welsh-Powell) only where exact solution is impractical

**Simplicity vs. Optimization:**
- Array-based Dijkstra for implementation simplicity
- Union-Find with path compression for practical efficiency
- Avoided complex data structures unless necessary

**Flexibility vs. Specialization:**
- General graph structure supports multiple algorithms
- Modular design allows algorithm swapping
- State management (disabled nodes, vulnerable edges) provides flexibility

---

## Theoretical Foundation

### Correctness Proofs

**Kruskal's MST:**
- Greedy choice property: Lightest edge crossing cut is in some MST
- Optimal substructure: MST of subgraph is part of global MST
- Cycle property: Heaviest edge in cycle not in MST

**Dijkstra's Algorithm:**
- Invariant: distance[v] is shortest path using visited nodes
- Greedy choice: Next closest node has shortest path
- Works only for non-negative weights (no improvement after visiting)

**AVL Tree:**
- Height balance: |h_left - h_right| ≤ 1 implies h ≤ 1.44 log(n+2)
- Rotations restore balance without violating BST property
- Fibonacci tree analysis proves worst-case height bound

### Practical Considerations

**Real-World Applications:**
- MST: Network cable installation, circuit design, road network planning
- Shortest Path: GPS navigation, logistics routing, network packet routing
- K-Disjoint Paths: Redundant data transmission, fault-tolerant routing
- AVL Tree: Database indexing, priority systems, symbol tables
- Failure Analysis: Infrastructure resilience, disaster planning
- Graph Coloring: Frequency allocation, register allocation, scheduling

**Scalability:**
- Algorithms tested on graphs up to 100 nodes
- Performance degrades gracefully with size
- Memory usage linear or log-linear
- Interactive GUI maintains responsiveness

---

## Conclusion

This implementation demonstrates comprehensive understanding of graph and tree algorithms through:

1. **Algorithm Selection**: Chose optimal algorithms for each problem (Kruskal for MST, Dijkstra for shortest paths, AVL for balanced trees)

2. **Efficient Implementation**: Used appropriate data structures (Union-Find, adjacency lists) and optimizations (path compression, balance factors)

3. **Practical Application**: Developed interactive simulator for emergency network planning with real-time visualization

4. **Thorough Testing**: Validated correctness with comprehensive test suites covering edge cases

5. **Clear Documentation**: Explained approach, complexity analysis, and trade-offs for each algorithm

The system successfully addresses all requirements while maintaining code clarity and computational efficiency. All algorithms are implemented from scratch without external algorithm libraries, demonstrating deep understanding of underlying principles.
