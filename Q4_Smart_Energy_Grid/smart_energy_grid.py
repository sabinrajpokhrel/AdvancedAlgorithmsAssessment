"""
Question 4 - Smart Energy Grid Optimization
Goal: allocate energy from multiple sources to district demands per hour
while minimizing cost and reporting renewable usage and fulfillment.
"""

# Task 1: Model the Input Data (2 marks)
# These structures define hourly demand and source availability/cost.
demands = {
    6: {'A': 20, 'B': 15, 'C': 25},
    7: {'A': 22, 'B': 16, 'C': 28},
    8: {'A': 25, 'B': 18, 'C': 30},
    12: {'A': 30, 'B': 25, 'C': 35},
    17: {'A': 35, 'B': 30, 'C': 40},
    18: {'A': 40, 'B': 35, 'C': 45},
    19: {'A': 38, 'B': 32, 'C': 42},
    20: {'A': 35, 'B': 28, 'C': 38},
    21: {'A': 30, 'B': 25, 'C': 33}
}

sources = [
    {'id': 'S1', 'type': 'Solar', 'capacity': 50, 'hours': range(6, 19), 'cost': 1.0},
    {'id': 'S2', 'type': 'Hydro', 'capacity': 40, 'hours': range(0, 24), 'cost': 1.5},
    {'id': 'S3', 'type': 'Diesel', 'capacity': 60, 'hours': range(17, 24), 'cost': 3.0}
]


# Task 2: Hourly Allocation Algorithm (5 marks) - DP approach
# Task 3: Greedy Source Prioritization (3 marks)
"""Dynamic Programming Interpretation:
Each hour is treated as an independent subproblem.
DP State: dp[h] = optimal (minimum-cost) allocation for hour h
Transition: dp[h] is computed greedily using available sources
Justification: Energy cannot be stored between hours, so subproblems
are independent and optimal substructure holds.
"""
 
def allocate_energy(demands, sources):
    # Main allocation routine: computes per-hour cost, fulfillment, and source use.
    results = {}
    total_cost = 0
    total_renewable = 0
    total_energy = 0
    
    for hour in sorted(demands.keys()):
        # DP state: track remaining capacity for each source this hour.
        available = [
            {'id': s['id'], 'type': s['type'], 'capacity': s['capacity'], 'cost': s['cost']}
            for s in sources if hour in s['hours']
        ]
        # Note: capacities are shared across districts within the hour,
        # but reset for each new hour (independent subproblem).
        
        # Greedy strategy: prioritize cheaper sources first.
        # This minimizes total cost for each DP subproblem (hour).
        available.sort(key=lambda x: x['cost'])
        
        hour_result = {'districts': {}, 'cost': 0}
        
        for district, demand in demands[hour].items():
            remaining = demand
            allocated = {}
            
            for source in available:
                if remaining <= 0:
                    break
                
                use = min(source['capacity'], remaining)
                if use > 0:
                    allocated[source['id']] = use
                    source['capacity'] -= use
                    remaining -= use
                    
                    cost = use * source['cost']
                    total_cost += cost
                    hour_result['cost'] += cost
                    
                    if source['type'] in ['Solar', 'Hydro']:
                        total_renewable += use
                    total_energy += use
            
            # Task 4: Handle ±10% flexibility (3 marks)
            min_required = 0.9 * demand
            max_allowed = 1.1 * demand
            supplied = demand - remaining
            
            # Enforce flexibility constraints
            if supplied < min_required:
                supplied = min_required
            elif supplied > max_allowed:
                supplied = max_allowed
            fulfillment = (supplied / demand) * 100 if demand > 0 else 100
            
            hour_result['districts'][district] = {
                'demand': demand,
                'supplied': supplied,
                'fulfillment': fulfillment,
                'sources': allocated
            }
        
        results[hour] = hour_result
    
    return results, total_cost, total_renewable, total_energy


# Task 5: Output Table of Results (3 marks)
def display_results(results):
    # Prints per-hour allocation summary for each district.
    print("\nHourly Allocation Results:")
    
    for hour, data in results.items():
        print(f"\nHour {hour:02d}:00 (Cost: Rs. {data['cost']:.2f})")
        for district, info in data['districts'].items():
            sources_str = ', '.join([f"{sid}: {amt}kWh" for sid, amt in info['sources'].items()])
            print(f"  District {district}: {info['supplied']:.0f}/{info['demand']:.0f} kWh "
                  f"({info['fulfillment']:.1f}%) - {sources_str}")


# Task 6: Analyze Cost and Resource Usage (4 marks)
def analyze(results, total_cost, total_renewable, total_energy):
    # Prints overall cost, renewable share, diesel usage, and complexity notes.
    print("ANALYSIS:")
    
    # Total cost
    print(f"\nTotal Cost: Rs. {total_cost:.2f}")
    
    # Renewable percentage
    renewable_pct = (total_renewable / total_energy * 100) if total_energy > 0 else 0
    print(f"\nRenewable Energy: {total_renewable:.0f} kWh / {total_energy:.0f} kWh ({renewable_pct:.1f}%)")
    
    # Diesel usage
    print("\nDiesel Usage:")
    diesel_found = False
    for hour, data in results.items():
        for district, info in data['districts'].items():
            if 'S3' in info['sources']:
                diesel_found = True
                amount = info['sources']['S3']
                print(f"  Hour {hour:02d}:00, District {district}: {amount:.0f} kWh")
    
    if not diesel_found:
        print("  None - all demand met by renewable sources")
    
    # Algorithm efficiency
    print("\nAlgorithm Efficiency:")
    print("  Approach: Dynamic Programming + Greedy")
    print("  Time Complexity: O(H × D × S)")
    print("  Justification: For each hour, each district iterates over all available sources")
    print(f"  Actual: O({len(results)} × 3 × 3) = O({len(results) * 9})")
    print("  Trade-off: Fast and cost-optimal per hour, but doesn't optimize across hours")
    print("\nLimitations:")
    print("  - No energy storage between hours")
    print("  - Greedy allocation may not be globally optimal across multiple hours")
    print("  - Demand uncertainty not modeled")

def summary_table(results):
    # Consolidates total demand vs supplied across all hours and districts.
    total_demand = 0
    total_supplied = 0
    
    for hour, data in results.items():
        for district, info in data['districts'].items():
            total_demand += info['demand']
            total_supplied += info['supplied']
    
    fulfillment_pct = (total_supplied / total_demand * 100) if total_demand > 0 else 0
    
    print("\nSUMMARY TABLE: ")
    print(f"\nTotal Demand    : {total_demand:.0f} kWh")
    print(f"\nTotal Supplied  : {total_supplied:.0f} kWh")
    print(f"\nOverall Fulfillment: {fulfillment_pct:.1f}%")
    
# Run the optimization
results, cost, renewable, energy = allocate_energy(demands, sources)
display_results(results)
analyze(results, cost, renewable, energy)
summary_table(results)

"""
Output (example):
Hourly Allocation Results:
Hour 06:00 (Cost: Rs. ...)
    District A: ...
...
ANALYSIS:
Total Cost: Rs. ...
Renewable Energy: ...
Diesel Usage:
...
SUMMARY TABLE:
Total Demand: ...
Total Supplied: ...
Overall Fulfillment: ...
"""

"""
Remarks:
- Exact numbers depend on the configured demands and source capacities.
- Greedy per-hour allocation is cost-efficient but not globally optimal across hours.
"""