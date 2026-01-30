"""
Minimum Spanning Tree implementation using
RAW Kruskal's Algorithm with Union-Find.

NO external algorithm libraries are used.
"""

# ---------------------------------------------------
# Union-Find (Disjoint Set) Helper Functions
# ---------------------------------------------------

def find(parent, city):
    if parent[city] != city:
        parent[city] = find(parent, parent[city])
    return parent[city]


def union(parent, rank, city1, city2):
    root1 = find(parent, city1)
    root2 = find(parent, city2)

    if root1 != root2:
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

    Parameters:
        graph (EmergencyGraph): Custom graph object

    Returns:
        mst_edges: list of edges in MST
        total_weight: sum of weights
    """

    mst_edges = []
    total_weight = 0

    # Initialize Union-Find structures
    parent = {}
    rank = {}

    for city in graph.get_all_cities():
        parent[city] = city
        rank[city] = 0

    # Sort edges by weight (no library sort helpers)
    edges = graph.get_all_edges()
    edges.sort(key=lambda edge: edge[2])

    for city1, city2, weight in edges:
        if find(parent, city1) != find(parent, city2):
            union(parent, rank, city1, city2)
            mst_edges.append((city1, city2, weight))
            total_weight += weight

    return mst_edges, total_weight
