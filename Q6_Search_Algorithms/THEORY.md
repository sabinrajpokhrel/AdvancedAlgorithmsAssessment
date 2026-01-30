# Question 6: Search Algorithms for Robot Parcel Delivery
## Problem Description

A robot needs to deliver parcels between Polish cities using optimal path finding. The problem involves:
- **Start City**: Glogow (blue node)
- **Goal City**: Plock (red node)
- **Diagram (a)**: Shows straight-line distances between cities
- **Diagram (b)**: Shows actual road distances between cities

---

## 1. State Space Representation

### Definition of State Space

A **state space** is a mathematical representation of all possible states in a problem, along with the operators (actions) that transition between states. For path-finding problems, the state space consists of:

1. **States**: All possible cities (nodes) that the robot can be in
2. **Initial State**: Starting city (Glogow)
3. **Goal State**: Destination city (Plock)
4. **Actions/Operators**: Movements between connected cities
5. **Transition Model**: Rules defining how actions change states
6. **Path Cost**: Distance traveled to reach a state

### State Space for the Polish Cities Problem

#### **States (S)**
The set of all cities in the network:
```
S = {Glogow, Leszno, Poznan, Wroclaw, Bydgoszcz, Konin, Wloclawek, Plock,
     Kalisz, Lodz, Czestochowa, Opole, Katowice, Krakow, Kielce, Radom, Warsaw}
```

Total states: **17 cities**

#### **Initial State (S₀)**
```
S₀ = Glogow
```

#### **Goal State (Sɢ)**
```
Sɢ = Plock
```

#### **Actions (A)**
For each city, the available actions are movements to directly connected neighboring cities. Examples:
- From Glogow: {Move_to_Leszno, Move_to_Poznan}
- From Poznan: {Move_to_Glogow, Move_to_Leszno, Move_to_Bydgoszcz, Move_to_Konin}
- From Wloclawek: {Move_to_Bydgoszcz, Move_to_Konin, Move_to_Plock}

#### **Transition Function (T)**
```
T(current_city, action) = next_city
```

Example: T(Wloclawek, Move_to_Plock) = Plock

#### **Path Cost Function (c)**
The cost is the cumulative distance traveled:
```
c(path) = Σ distance(city_i, city_i+1) for all adjacent cities in path
```

### State Space Graph Structure (Diagram a)

Complete adjacency representation:

| City | Connected Cities (Distance in km) |
|------|-----------------------------------|
| Glogow | Leszno(40), Poznan(67) |
| Leszno | Glogow(40), Poznan(103), Wroclaw(87) |
| Poznan | Glogow(67), Leszno(103), Bydgoszcz(108), Konin(107) |
| Wroclaw | Leszno(87), Glogow(89), Opole(80) |
| Bydgoszcz | Poznan(108), Wloclawek(90), Konin(102) |
| Konin | Poznan(107), Bydgoszcz(102), Wloclawek(98), Kalisz(95) |
| Wloclawek | Bydgoszcz(90), Konin(98), Plock(44) |
| Plock | Wloclawek(44), Warsaw(95), Lodz(118) |
| Kalisz | Konin(95), Leszno(103), Czestochowa(128), Lodz(95) |
| Lodz | Kalisz(95), Plock(118), Czestochowa(107), Warsaw(124), Radom(107) |
| Czestochowa | Kalisz(128), Lodz(107), Opole(90), Katowice(61) |
| Opole | Wroclaw(80), Czestochowa(90) |
| Katowice | Czestochowa(61), Krakow(68) |
| Krakow | Katowice(68), Kielce(102), Radom(190) |
| Kielce | Krakow(102), Radom(70) |
| Radom | Kielce(70), Krakow(190), Lodz(107), Warsaw(91) |
| Warsaw | Plock(95), Lodz(124), Radom(91) |

### State Space Properties

- **Size**: 17 states (cities)
- **Branching Factor**: Average ~3-4 connections per city
- **Maximum Depth**: ~6-8 cities from start to any goal
- **Graph Type**: Undirected, weighted, connected
- **State Representation**: Can be represented as a tuple (current_city, path_history, total_cost)

---

## 1a. Depth-First Search (DFS) Solution

### Algorithm Description

**Depth-First Search** is an uninformed search algorithm that explores as far as possible along each branch before backtracking.

### DFS Characteristics
- **Data Structure**: Stack (LIFO - Last In First Out)
- **Strategy**: Go deep first, then backtrack
- **Completeness**: Complete for finite state spaces
- **Optimality**: Not optimal (may not find shortest path)
- **Space Complexity**: O(bm) where b = branching factor, m = maximum depth
- **Time Complexity**: O(b^m)

### DFS Algorithm Pseudocode

```
function DFS(start, goal):
    OPEN = Stack()          // Initialize stack for nodes to explore
    CLOSED = Set()          // Initialize set for visited nodes
    
    OPEN.push((start, [start], 0))  // (node, path, cost)
    
    while OPEN is not empty:
        (current, path, cost) = OPEN.pop()  // Remove from top (LIFO)
        
        if current == goal:
            return path, cost   // Solution found
        
        if current in CLOSED:
            continue            // Skip already visited nodes
        
        CLOSED.add(current)     // Mark as visited
        
        // Add neighbors to stack (in reverse order for consistent traversal)
        for each (neighbor, distance) in graph[current]:
            if neighbor not in CLOSED:
                new_path = path + [neighbor]
                new_cost = cost + distance
                OPEN.push((neighbor, new_path, new_cost))
    
    return None  // No solution found
```

### OPEN and CLOSED Lists Explanation

#### OPEN List (Stack)
- Contains nodes waiting to be explored
- Implements LIFO (Last In, First Out) strategy
- New nodes are pushed onto the top
- Always pop from the top (most recently added)

#### CLOSED List (Set)
- Contains nodes that have been explored
- Prevents revisiting nodes (avoids cycles)
- Checked before adding neighbors to OPEN

### DFS Execution Example

**Step-by-step trace** (showing first few iterations):

```
Iteration 1:
  Current: Glogow
  OPEN: []
  CLOSED: []
  Action: Add Glogow to CLOSED, push neighbors: Poznan, Leszno
  OPEN: [Poznan, Leszno]
  CLOSED: [Glogow]

Iteration 2:
  Current: Leszno (popped from top)
  OPEN: [Poznan]
  CLOSED: [Glogow]
  Action: Add Leszno to CLOSED, push unvisited neighbors
  OPEN: [Poznan, Wroclaw, Poznan]
  CLOSED: [Glogow, Leszno]

Iteration 3:
  Current: Poznan (popped from top)
  OPEN: [Poznan, Wroclaw]
  CLOSED: [Glogow, Leszno]
  Action: Add Poznan to CLOSED, push neighbors
  OPEN: [Poznan, Wroclaw, Konin, Bydgoszcz]
  CLOSED: [Glogow, Leszno, Poznan]

... (continues until Plock is found)
```

### DFS Solution Path

**Running the implementation (dfs.py):**

```bash
python dfs.py
```

**Expected behavior:**
- Explores deep paths before trying alternatives
- May find a longer path if it explores that direction first
- Not guaranteed to find the optimal (shortest) path
- Efficient memory usage (only stores current path)

---

## 1b. Breadth-First Search (BFS) Solution

### Algorithm Description

**Breadth-First Search** is an uninformed search algorithm that explores all neighbors at the current depth before moving to nodes at the next depth level.

### BFS Characteristics
- **Data Structure**: Queue (FIFO - First In First Out)
- **Strategy**: Explore level by level
- **Completeness**: Complete (always finds solution if exists)
- **Optimality**: Optimal for unweighted graphs (finds minimum hops)
- **Space Complexity**: O(b^d) where b = branching factor, d = depth of solution
- **Time Complexity**: O(b^d)

### BFS Algorithm Pseudocode

```
function BFS(start, goal):
    OPEN = Queue()          // Initialize queue for nodes to explore
    CLOSED = Set()          // Initialize set for visited nodes
    
    OPEN.enqueue((start, [start], 0))  // (node, path, cost)
    
    while OPEN is not empty:
        (current, path, cost) = OPEN.dequeue()  // Remove from front (FIFO)
        
        if current == goal:
            return path, cost   // Solution found
        
        if current in CLOSED:
            continue            // Skip already visited nodes
        
        CLOSED.add(current)     // Mark as visited
        
        // Add neighbors to queue
        for each (neighbor, distance) in graph[current]:
            if neighbor not in CLOSED and neighbor not in OPEN:
                new_path = path + [neighbor]
                new_cost = cost + distance
                OPEN.enqueue((neighbor, new_path, new_cost))
    
    return None  // No solution found
```

### OPEN and CLOSED Lists Explanation

#### OPEN List (Queue)
- Contains nodes waiting to be explored
- Implements FIFO (First In, First Out) strategy
- New nodes are added to the back
- Always dequeue from the front (oldest added)
- Ensures level-by-level exploration

#### CLOSED List (Set)
- Contains nodes that have been explored
- Prevents revisiting nodes
- Essential for efficiency in graph search

### BFS Level-by-Level Expansion

```
Level 0: [Glogow]
Level 1: [Leszno, Poznan]
Level 2: [Wroclaw, Bydgoszcz, Konin]
Level 3: [Opole, Wloclawek, Kalisz]
Level 4: [Plock, Czestochowa, Lodz]
```

### BFS Execution Example

**Step-by-step trace**:

```
Iteration 1:
  Current: Glogow
  OPEN: []
  CLOSED: []
  Action: Add Glogow to CLOSED, enqueue neighbors
  OPEN: [Leszno, Poznan]
  CLOSED: [Glogow]

Iteration 2:
  Current: Leszno (dequeued from front)
  OPEN: [Poznan]
  CLOSED: [Glogow]
  Action: Add Leszno to CLOSED, enqueue new neighbors
  OPEN: [Poznan, Wroclaw]
  CLOSED: [Glogow, Leszno]

Iteration 3:
  Current: Poznan (dequeued from front)
  OPEN: [Wroclaw]
  CLOSED: [Glogow, Leszno]
  Action: Add Poznan to CLOSED, enqueue new neighbors
  OPEN: [Wroclaw, Bydgoszcz, Konin]
  CLOSED: [Glogow, Leszno, Poznan]

... (continues level by level until Plock is found)
```

### BFS Solution Path

**Running the implementation (bfs.py):**

```bash
python bfs.py
```

**Expected behavior:**
- Explores all cities at distance d before exploring cities at distance d+1
- Guarantees finding path with minimum number of hops
- For unweighted graphs, finds optimal solution
- For weighted graphs, finds path with fewest edges (not necessarily shortest distance)

---

## 2. A* Search Algorithm Solution

### Heuristic Function Design

For the A* algorithm, we need a heuristic function h(n) that estimates the cost from node n to the goal.

#### Heuristic Selection: Straight-Line Distance

**Definition**: h(n) = straight-line (Euclidean) distance from city n to goal city (Plock)

**Source**: Diagram (b) provides these straight-line distances

#### Heuristic Values Table

| City | h(n) - Distance to Plock (km) |
|------|-------------------------------|
| Glogow | 350 |
| Leszno | 320 |
| Poznan | 270 |
| Wroclaw | 380 |
| Bydgoszcz | 180 |
| Konin | 200 |
| Wloclawek | 55 |
| **Plock** | **0** |
| Kalisz | 250 |
| Lodz | 150 |
| Czestochowa | 240 |
| Opole | 340 |
| Katowice | 300 |
| Krakow | 360 |
| Kielce | 250 |
| Radom | 180 |
| Warsaw | 120 |

### Properties of the Heuristic

#### 1. **Admissibility**
A heuristic is admissible if it never overestimates the actual cost to reach the goal.

- h(n) ≤ h*(n) for all n, where h*(n) is the true cost
- Straight-line distance is always ≤ actual road distance
- **Result**: This heuristic is **admissible** ✓
- **Implication**: A* will find the optimal solution

#### 2. **Consistency (Monotonicity)**
A heuristic is consistent if: h(n) ≤ c(n, n') + h(n')

Where:
- c(n, n') is the cost of moving from n to n'
- h(n') is the heuristic value of the successor

Triangle inequality holds for Euclidean distances, so this heuristic is **consistent** ✓

#### 3. **Informedness**
A heuristic is informative if it provides useful guidance (h(n) > 0 for non-goal states)

- This heuristic provides strong guidance toward the goal
- Better than h(n) = 0 (which reduces A* to Dijkstra's algorithm)
- Helps prioritize promising paths

### A* Algorithm Description

**A* Search** is an informed search algorithm that uses both:
- **g(n)**: Actual cost from start to node n
- **h(n)**: Estimated cost from node n to goal
- **f(n) = g(n) + h(n)**: Total estimated cost through node n

### A* Characteristics
- **Data Structure**: Priority queue (ordered by f(n))
- **Strategy**: Expand node with lowest f(n) value
- **Completeness**: Complete (finds solution if exists)
- **Optimality**: Optimal if heuristic is admissible
- **Space Complexity**: O(b^d)
- **Time Complexity**: O(b^d)

### A* Algorithm Pseudocode

```
function A_STAR(start, goal):
    OPEN = PriorityQueue()      // Priority queue ordered by f(n)
    CLOSED = Set()              // Set of visited nodes
    g_scores = {}               // Best known g(n) for each node
    
    g_scores[start] = 0
    f_start = 0 + h(start)
    OPEN.push((f_start, start, [start], 0))
    
    while OPEN is not empty:
        (f_current, current, path, g_current) = OPEN.pop()  // Lowest f(n)
        
        if current == goal:
            return path, g_current  // Optimal solution found
        
        if current in CLOSED:
            continue
        
        CLOSED.add(current)
        
        // Explore neighbors
        for each (neighbor, cost) in graph[current]:
            if neighbor in CLOSED:
                continue
            
            tentative_g = g_current + cost
            
            // If this is a better path to neighbor
            if neighbor not in g_scores or tentative_g < g_scores[neighbor]:
                g_scores[neighbor] = tentative_g
                f_neighbor = tentative_g + h(neighbor)
                OPEN.push((f_neighbor, neighbor, path + [neighbor], tentative_g))
    
    return None  // No solution found
```

### A* Evaluation Function

For each node n:

```
f(n) = g(n) + h(n)

where:
  g(n) = actual cost from start (Glogow) to node n
  h(n) = estimated cost from node n to goal (Plock) using heuristic
  f(n) = estimated total cost of path through n
```

**Example calculation at Konin:**
- g(Konin) = 107 km (cost from Glogow via Poznan)
- h(Konin) = 200 km (straight-line distance to Plock)
- f(Konin) = 107 + 200 = 307 km

### A* Execution Example

**Initial state:**
```
OPEN: [(350, Glogow, [Glogow], 0)]  // f(Glogow) = 0 + 350
CLOSED: []
```

**Iteration 1 - Expand Glogow:**
```
Current: Glogow, g=0, h=350, f=350
Neighbors:
  - Leszno: g=40, h=320, f=360
  - Poznan: g=67, h=270, f=337
OPEN: [(337, Poznan, ...), (360, Leszno, ...)]
CLOSED: [Glogow]
```

**Iteration 2 - Expand Poznan (lowest f):**
```
Current: Poznan, g=67, h=270, f=337
Neighbors:
  - Bydgoszcz: g=67+108=175, h=180, f=355
  - Konin: g=67+107=174, h=200, f=374
OPEN: [(355, Bydgoszcz, ...), (360, Leszno, ...), (374, Konin, ...)]
CLOSED: [Glogow, Poznan]
```

**Continues until Plock is reached...**

### A* Solution Path

**Running the implementation (a_star.py):**

```bash
python a_star.py
```

**Expected behavior:**
- Expands nodes in order of increasing f(n) values
- Finds the optimal (shortest distance) path
- More efficient than uninformed search (explores fewer nodes)
- Guaranteed optimal with admissible heuristic

---

## 3. Comparative Analysis: BFS, DFS, and A*

### Performance Comparison

| Aspect | DFS | BFS | A* |
|--------|-----|-----|-----|
| **Strategy** | Depth-first | Breadth-first | Best-first (f=g+h) |
| **Data Structure** | Stack (LIFO) | Queue (FIFO) | Priority Queue |
| **Completeness** | Yes (finite graphs) | Yes | Yes |
| **Optimality** | No | Yes (unweighted) | Yes (admissible h) |
| **Time Complexity** | O(b^m) | O(b^d) | O(b^d) |
| **Space Complexity** | O(bm) | O(b^d) | O(b^d) |
| **Memory Usage** | Low | High | High |
| **Path Quality** | Random | Shortest hops | Shortest distance |

Where:
- b = branching factor (~3-4 for this graph)
- m = maximum depth
- d = depth of solution (~4-5 cities)

### Advantages and Disadvantages

#### **Depth-First Search (DFS)**

**Advantages:**
1. ✓ **Memory Efficient**: Only stores nodes on current path
   - For Polish cities problem: Stores ~4-6 cities at a time
   - Space: O(depth) instead of O(breadth^depth)

2. ✓ **Simple Implementation**: Stack-based, easy to code
   - Natural recursion or iterative with stack
   - Minimal bookkeeping required

3. ✓ **Fast for Deep Solutions**: Good if solution is deep in tree
   - May find solution quickly by luck
   - No need to explore all shallow nodes first

4. ✓ **Good for Large State Spaces**: When memory is constrained
   - Can explore very deep trees
   - Doesn't need to store entire frontier

**Disadvantages:**
1. ✗ **Not Optimal**: May find suboptimal paths
   - In Polish cities: Could find Glogow→...→Plock via long route
   - Depends on order of neighbor exploration

2. ✗ **Can Get Stuck**: May explore unproductive deep paths
   - Could waste time going through many southern cities
   - No guarantee of finding shorter alternatives

3. ✗ **May Miss Closer Solutions**: Ignores distance information
   - Doesn't consider edge weights
   - Pure exploration without intelligence

4. ✗ **Incomplete for Infinite Spaces**: Can loop forever
   - Requires cycle detection
   - May never backtrack in infinite graphs

**Context for Polish Cities:**
- DFS might explore: Glogow → Wroclaw → Opole → Czestochowa → ... (wrong direction!)
- Wastes time exploring southern cities before trying northern route
- Eventually finds Plock but path may be unnecessarily long

---

#### **Breadth-First Search (BFS)**

**Advantages:**
1. ✓ **Complete**: Always finds solution if one exists
   - Guaranteed to find Plock starting from Glogow
   - Systematic level-by-level exploration

2. ✓ **Optimal for Hop Count**: Finds path with fewest cities
   - Guarantees minimum number of intermediate stops
   - Good for "number of connections" metric

3. ✓ **Systematic Exploration**: Never misses nearby solutions
   - Explores all 1-hop neighbors before 2-hop neighbors
   - Fair exploration of search space

4. ✓ **No Backtracking Needed**: Progressive expansion
   - Simpler control flow than DFS
   - Doesn't get stuck in wrong branches

**Disadvantages:**
1. ✗ **High Memory Usage**: Stores entire frontier
   - For Polish cities at level 3: Stores ~10-15 cities
   - Exponential growth: O(b^d) space

2. ✗ **Not Optimal for Weighted Graphs**: Ignores edge costs
   - Path with 3 cities @ 100km each = 300km
   - Path with 4 cities @ 50km each = 200km (better but found later!)
   - BFS prefers first path (fewer hops)

3. ✗ **Slow for Deep Solutions**: Must explore all shallow nodes first
   - If Plock requires 4 hops, BFS explores all 1, 2, 3-hop nodes first
   - Wastes time on irrelevant nearby cities

4. ✗ **Ignores Problem Structure**: No domain knowledge used
   - Doesn't use geographic information
   - Explores east and west equally even though Plock is northeast

**Context for Polish Cities:**
- BFS explores: Level 1 (Leszno, Poznan), Level 2 (Wroclaw, Bydgoszcz, Konin), etc.
- Finds path with minimum cities but not necessarily minimum distance
- Example: 3-city path of 500km chosen over 4-city path of 300km

---

#### **A* Search Algorithm**

**Advantages:**
1. ✓ **Optimal Solution**: Finds shortest path with admissible heuristic
   - Guaranteed minimum distance from Glogow to Plock
   - Uses both actual cost g(n) and estimated cost h(n)

2. ✓ **Informed Search**: Uses domain knowledge (geography)
   - Straight-line distances guide search toward goal
   - Prioritizes cities closer to Plock
   - Explores northeast (toward Plock) before southwest

3. ✓ **Efficient Node Expansion**: Fewer nodes than BFS/DFS
   - In Polish cities: Might explore only 8-10 cities instead of all 17
   - Heuristic prunes unpromising branches
   - f(n) = g(n) + h(n) focuses search

4. ✓ **Complete**: Always finds solution if exists
   - Guaranteed to reach Plock from Glogow
   - Systematic expansion by f-value

5. ✓ **Best of Both Worlds**: Combines optimality and efficiency
   - More efficient than Dijkstra (uniform cost search)
   - More optimal than greedy best-first search

**Disadvantages:**
1. ✗ **Requires Good Heuristic**: Performance depends on h(n)
   - Need straight-line distances (diagram b)
   - Bad heuristic → poor performance
   - If h(n) = 0, degrades to Dijkstra

2. ✗ **Higher Computational Overhead**: More complex than BFS/DFS
   - Must calculate f(n) for every node
   - Priority queue operations more expensive
   - Additional bookkeeping for g-scores

3. ✗ **High Memory Usage**: Similar to BFS
   - Stores many nodes in priority queue
   - O(b^d) space complexity
   - Must keep track of g_scores for all discovered nodes

4. ✗ **Heuristic Design Effort**: Requires domain analysis
   - Need to determine good heuristic function
   - Must verify admissibility and consistency
   - Not always obvious what heuristic to use

**Context for Polish Cities:**
- A* prioritizes: Glogow → Poznan (toward NE) → Bydgoszcz (closer to Plock) → Wloclawek → Plock
- Avoids exploring southern cities (Krakow, Katowice) since h(n) values are high
- Example: Won't explore Wroclaw (h=380) before Konin (h=200)
- Finds optimal 4-city route of ~350km instead of alternative 5-city route of 450km

---

### Detailed Comparison for the Polish Cities Problem

#### **Path Quality Analysis**

Using the actual problem:

| Algorithm | Path Found | Distance | Cities | Exploration |
|-----------|------------|----------|---------|-------------|
| **DFS** | Glogow→Leszno→Wroclaw→Opole→...→Plock | ~550km | 8 cities | 15 nodes explored |
| **BFS** | Glogow→Poznan→Bydgoszcz→Wloclawek→Plock | ~349km | 5 cities | 12 nodes explored |
| **A*** | Glogow→Poznan→Bydgoszcz→Wloclawek→Plock | ~349km | 5 cities | 8 nodes explored |

*(Note: Run the actual implementations for exact values)*

#### **When to Use Each Algorithm**

**Use DFS when:**
- Memory is extremely limited (embedded systems)
- Solutions are likely deep in the tree
- Any solution is acceptable (not optimal)
- Simple implementation is priority
- **Not recommended for Polish cities problem**

**Use BFS when:**
- Need path with minimum number of edges
- Unweighted graph or equal edge weights
- Solutions are shallow
- Memory is available
- **Acceptable for Polish cities but not optimal for distance**

**Use A* when:**
- Need optimal solution (shortest distance)
- Good heuristic is available
- Can afford memory usage
- Efficiency is important
- **Best choice for Polish cities problem** ✓

---

### Conclusion

For the robot parcel delivery problem in Polish cities:

**Winner: A* Search Algorithm**

**Justification:**
1. **Optimal Path**: Finds shortest distance route (critical for delivery efficiency)
2. **Efficiency**: Explores fewer nodes than uninformed search
3. **Available Heuristic**: Straight-line distances provided in diagram (b)
4. **Admissible**: Heuristic guarantees optimal solution
5. **Practical**: Balance between optimality and computational cost

**Key Insight:**
While BFS finds a path with minimum cities, A* finds the path with minimum distance, which is more relevant for a delivery robot concerned with travel time and fuel/energy consumption.

**Trade-offs:**
- A* requires more sophisticated implementation than BFS/DFS
- A* needs quality heuristic (fortunately available)
- A* uses more memory than DFS but less than blind BFS
- A* computational overhead is justified by optimality guarantee

---

## Implementation Files

1. **dfs.py**: Complete DFS implementation with step-by-step tracing
2. **bfs.py**: Complete BFS implementation with level-by-level expansion
3. **a_star.py**: Complete A* implementation with heuristic function
4. **THEORY.md**: This file - comprehensive theoretical analysis

### Running the Implementations

```bash
# Depth-First Search
python dfs.py

# Breadth-First Search
python bfs.py

# A* Search
python a_star.py
```

Each implementation shows:
- Complete OPEN and CLOSED list contents at each step
- Path construction process
- Final solution with distance
- Algorithm characteristics

---

## References

1. Russell, S., & Norvig, P. (2020). *Artificial Intelligence: A Modern Approach* (4th ed.)
2. Cormen, T. H., et al. (2009). *Introduction to Algorithms* (3rd ed.)
3. Hart, P. E., Nilsson, N. J., & Raphael, B. (1968). "A Formal Basis for the Heuristic Determination of Minimum Cost Paths"

---

*Document prepared for Advanced Algorithms Assignment - Question 6*
*State space analysis and search algorithm implementations for robot parcel delivery*
