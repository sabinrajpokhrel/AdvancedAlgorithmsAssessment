"""
Question 6 - Search Algorithms Comparison Tool
Goal: execute and compare DFS, BFS, and A* algorithms on the same problem
to demonstrate their differences in optimality, efficiency, and search strategy.
"""

from dfs import DFSSearch
from bfs import BFSSearch
from a_star import AStarSearch


def print_header(title):
    """Print a formatted header"""
    print("\n" + "=" * 80)
    print(f"{title:^80}")
    print("=" * 80)


def run_comparison():
    """Run all three algorithms and compare results"""
    
    print_header("SEARCH ALGORITHMS COMPARISON")
    print("\nProblem: Find path from Glogow to Plock in Polish city network")
    print("Start City: Glogow (blue node)")
    print("Goal City: Plock (red node)")
    
    # Store results
    results = []
    
    # Run DFS
    print_header("1. DEPTH-FIRST SEARCH (DFS)")
    dfs = DFSSearch()
    print("Running DFS... (exploring deep paths first)")
    path_dfs, dist_dfs = dfs.dfs_search()
    if path_dfs:
        results.append({
            'algorithm': 'DFS',
            'path': path_dfs,
            'distance': dist_dfs,
            'cities': len(path_dfs)
        })
    
    print("\n" + "*" * 80)
    input("Press Enter to continue to BFS...")
    
    # Run BFS
    print_header("2. BREADTH-FIRST SEARCH (BFS)")
    bfs = BFSSearch()
    print("Running BFS... (exploring level by level)")
    path_bfs, dist_bfs = bfs.bfs_search()
    if path_bfs:
        results.append({
            'algorithm': 'BFS',
            'path': path_bfs,
            'distance': dist_bfs,
            'cities': len(path_bfs)
        })
    
    print("\n" + "*" * 80)
    input("Press Enter to continue to A*...")
    
    # Run A*
    print_header("3. A* SEARCH")
    astar = AStarSearch()
    print("Running A*... (using heuristic guidance)")
    path_astar, dist_astar = astar.a_star_search()
    if path_astar:
        results.append({
            'algorithm': 'A*',
            'path': path_astar,
            'distance': dist_astar,
            'cities': len(path_astar)
        })
    
    # Display comparison
    print_header("RESULTS COMPARISON")
    
    print("\n{:<10} {:<60} {:<12} {:<10}".format(
        "Algorithm", "Path", "Distance", "Cities"))
    print("-" * 80)
    
    for result in results:
        path_str = " → ".join(result['path'])
        if len(path_str) > 58:
            path_str = path_str[:55] + "..."
        print("{:<10} {:<60} {:<12} {:<10}".format(
            result['algorithm'],
            path_str,
            f"{result['distance']} km",
            result['cities']
        ))
    
    # Analysis
    print_header("ANALYSIS")
    
    if results:
        # Find shortest distance
        min_dist = min(r['distance'] for r in results)
        min_cities = min(r['cities'] for r in results)
        
        print("\nOptimality Analysis:")
        for result in results:
            status = ""
            if result['distance'] == min_dist:
                status += " ✓ OPTIMAL DISTANCE"
            if result['cities'] == min_cities:
                status += " ✓ MINIMUM HOPS"
            print(f"  {result['algorithm']:5} - {result['distance']} km, {result['cities']} cities{status}")
        
        print("\n" + "-" * 80)
        print("\nKey Observations:")
        print("1. DFS: Explores deep paths first → May find suboptimal solution")
        print("2. BFS: Explores level-by-level → Finds minimum hop path")
        print("3. A*:  Uses heuristic → Finds optimal distance efficiently")
        
        print("\n" + "-" * 80)
        print("\nConclusion:")
        print("For weighted graphs (where edge costs matter), A* is superior:")
        print("  • Uses domain knowledge (straight-line distances)")
        print("  • Guarantees optimal solution with admissible heuristic")
        print("  • More efficient than uninformed search")
        print("  • Perfect for robot parcel delivery routing")
    
    print("\n" + "=" * 80)
    print("Comparison complete!")
    print("=" * 80)


def quick_summary():
    """Display a quick summary without full trace"""
    print_header("QUICK COMPARISON (No detailed trace)")
    
    # Monkey-patch print to suppress detailed output
    import builtins
    original_print = builtins.print
    suppress_output = False
    
    def conditional_print(*args, **kwargs):
        if not suppress_output:
            original_print(*args, **kwargs)
    
    builtins.print = conditional_print
    
    results = []
    
    # DFS
    suppress_output = True
    dfs = DFSSearch()
    path_dfs, dist_dfs = dfs.dfs_search()
    suppress_output = False
    if path_dfs:
        results.append(('DFS', path_dfs, dist_dfs))
    
    # BFS
    suppress_output = True
    bfs = BFSSearch()
    path_bfs, dist_bfs = bfs.bfs_search()
    suppress_output = False
    if path_bfs:
        results.append(('BFS', path_bfs, dist_bfs))
    
    # A*
    suppress_output = True
    astar = AStarSearch()
    path_astar, dist_astar = astar.a_star_search()
    suppress_output = False
    if path_astar:
        results.append(('A*', path_astar, dist_astar))
    
    # Restore original print
    builtins.print = original_print
    
    # Display results
    print("\n" + "=" * 80)
    print("SUMMARY RESULTS")
    print("=" * 80)
    
    for algo, path, distance in results:
        print(f"\n{algo} Result:")
        print(f"  Path: {' → '.join(path)}")
        print(f"  Distance: {distance} km")
        print(f"  Cities: {len(path)}")
    
    print("\n" + "=" * 80)


if __name__ == "__main__":
    import sys
    
    print("\n" + "=" * 80)
    print("SEARCH ALGORITHMS COMPARISON TOOL")
    print("=" * 80)
    print("\nOptions:")
    print("1. Full comparison with detailed trace (recommended for learning)")
    print("2. Quick summary (just results)")
    print()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        quick_summary()
    else:
        choice = input("Enter choice (1 or 2) [default: 1]: ").strip()
        
        if choice == '2':
            quick_summary()
        else:
            run_comparison()
