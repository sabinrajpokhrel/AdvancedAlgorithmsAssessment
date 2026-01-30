"""
Question 5 - Minimum Spanning Tree (MST): Kruskal's Algorithm

Problem Overview:
Find the minimum cost network that connects all cities. The MST ensures every city
is reachable from every other city using the minimum total road cost. This is crucial
for planning emergency communication infrastructure with budget constraints.

Approach:
I implemented Kruskal's algorithm which works by sorting all edges by weight and
greedily adding edges that don't create cycles. To efficiently detect cycles, I used
the Union-Find (Disjoint Set Union) data structure with path compression and union by rank.

Steps:
1. Sort all edges by weight in ascending order
2. Initialize Union-Find structure with each city as its own set
3. For each edge (u,v,w) in sorted order:
   - Check if u and v are in different sets (no cycle)
   - If yes, add edge to MST and union the sets
   - If no, skip (would create cycle)
4. Stop when (V-1) edges are added

Time Complexity: O(E log E) dominated by sorting
Space Complexity: O(V) for Union-Find structures
"""

# ---------------------------------------------------
# Union-Find (Disjoint Set) Helper Functions
# ---------------------------------------------------

def find(parent, city):
    """
    Finds the root of the set containing city.
    Uses path compression to flatten tree structure for faster future lookups.
    """
    if parent[city] != city:
        parent[city] = find(parent, parent[city])  # Path compression
    return parent[city]


def union(parent, rank, city1, city2):
    """
    Merges two sets containing city1 and city2.
    Uses union by rank to keep tree shallow, ensuring O(log n) depth.
    """
    root1 = find(parent, city1)
    root2 = find(parent, city2)

    if root1 != root2:
        # Attach smaller tree under larger tree
        if rank[root1] < rank[root2]:
            parent[root1] = root2
        elif rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root2] = root1
            rank[root1] += 1


# ---------------------------------------------------
# Kruskal's Algorithm (RAW IMPLEMENTATION)
# ---------------------------------------------------

def kruskal_mst(graph):
    """
    Computes the Minimum Spanning Tree using Kruskal's algorithm.
    
    Greedy strategy: Always pick the lightest edge that doesn't create a cycle.
    This guarantees optimal MST by the cut property of graphs.

    Parameters:
        graph (EmergencyGraph): Custom graph object

    Returns:
        mst_edges: list of edges (u, v, weight) in MST
        total_weight: sum of weights in MST
    """

    mst_edges = []
    total_weight = 0

    # Initialize Union-Find structures for cycle detection
    parent = {}
    rank = {}

    for city in graph.get_all_cities():
        parent[city] = city  # Each city starts in its own set
        rank[city] = 0       # Initial rank is 0

    # Sort edges by weight (greedy choice: lightest first)
    edges = graph.get_all_edges()
    edges.sort(key=lambda edge: edge[2])

    # Process edges in sorted order
    for city1, city2, weight in edges:
        # Check if adding this edge creates a cycle
        if find(parent, city1) != find(parent, city2):
            # No cycle - add edge to MST and merge sets
            union(parent, rank, city1, city2)
            mst_edges.append((city1, city2, weight))
            total_weight += weight

    return mst_edges, total_weight


"""
Remarks:
- Kruskal's algorithm is optimal for MST problem (proven by cut property).
- Union-Find with path compression and union by rank provides O(α(n)) per operation,
  where α is the inverse Ackermann function (effectively constant for practical inputs).
- Total complexity O(E log E) makes it efficient for both sparse and dense graphs.
- MST is unique if all edge weights are distinct; multiple MSTs possible with duplicate weights.
- Algorithm works on disconnected graphs (produces minimum spanning forest).
"""
