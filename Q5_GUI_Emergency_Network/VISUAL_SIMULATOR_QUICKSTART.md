# Quick Start Guide - Visual Simulator

## Setup (One-Time)

### 1. Install Dependencies
```bash
cd Q5_GUI_Emergency_Network
pip install -r requirements.txt
```

This installs:
- `streamlit>=1.28.0` - Web application framework
- `pyvis>=0.1.9` - Interactive graph visualization
- `pandas>=1.0.0` - Data handling

### 2. Run the Application
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Application Overview

### Navigation
The sidebar contains 6 main sections:
1. 📊 **Dashboard** - Interactive network graph editor
2. 🌳 **Q1: MST** - Minimum spanning tree computation
3. 🛣️ **Q2: Path Finder** - Shortest paths and disjoint paths
4. 🎋 **Q3: Tree Optimizer** - AVL tree rebalancing
5. ⚡ **Q4: Failure Simulation** - Network failure analysis
6. 📡 **Q5: Graph Coloring** - Frequency assignment (Bonus)

### Common Interactions

#### Dashboard - Interactive Network
1. **Drag Nodes**: Click and drag any node to move it
2. **Zoom**: Scroll mouse wheel
3. **Pan**: Right-click and drag to pan around
4. **Add Road**: Use sidebar controls to add a new road
5. **Mark Vulnerable**: Select a road and mark it as vulnerable

#### Q2: Path Finder
1. **Select Source**: Choose starting city from dropdown
2. **Select Destination**: Choose destination city
3. **Find Shortest Path**: Click button, see path and distance
4. **Find K-Disjoint Paths**: Adjust K value, click to find alternate routes

#### Q3: Tree Optimizer
1. **View Original Tree**: Left panel shows current command hierarchy
2. **Rebalance**: Click button to optimize tree balance
3. **Compare Results**: Right panel shows optimized tree with metrics
4. **View Improvements**: See height reduction and path length changes

#### Q4: Failure Simulation
1. **Select City to Fail**: Choose which city to simulate failure
2. **Run Simulation**: Click button to analyze impact
3. **View Metrics**: See affected nodes and network impact percentage
4. **Check Alternatives**: Automatic alternative routes below

#### Q5: Graph Coloring
1. **Compute Coloring**: Click button to assign frequencies
2. **View Results**: See color assignment visualization
3. **Check Metrics**: View efficiency and conflict status
4. **Read Assignments**: Each city's frequency band shown in list

## Keyboard Shortcuts

| Action | Keyboard |
|--------|----------|
| Zoom In | Mouse Scroll Up |
| Zoom Out | Mouse Scroll Down |
| Pan | Right Click + Drag |
| Center View | Double Click |
| Reload Page | F5 |

## Mouse Controls

| Action | Behavior |
|--------|----------|
| Left Click | Select node |
| Left Click + Drag | Move node |
| Right Click | Pan (hold and drag) |
| Scroll Wheel | Zoom in/out |
| Double Click | Re-center view |

## Tips & Tricks

1. **Better Layout**: Let physics simulation run for a few seconds for optimal node positioning
2. **Large Graphs**: Add nodes gradually to avoid cluttered layout
3. **Path Finding**: Use K=2 or K=3 for redundancy analysis
4. **Failure Testing**: Try failing central hub nodes to see network impact
5. **Performance**: Graphs with <50 nodes render smoothly on most machines

## Troubleshooting

### Graph Not Showing
- **Problem**: Blank white area where graph should be
- **Solution**: Refresh page (F5), or reload app with `streamlit run app.py`

### Slow Performance
- **Problem**: Dragging nodes is laggy
- **Solution**: 
  - Reduce number of nodes
  - Disable physics simulation in graph controls
  - Use a faster browser (Chrome > Firefox > Safari)

### No Alternative Routes Found
- **Problem**: Q4 shows "No route exists" 
- **Solution**: The network may be disconnected without that node. Try a less central city.

### Python Not Found
- **Problem**: `streamlit: command not found`
- **Solution**: 
  ```bash
  # Use Python directly
  python -m streamlit run app.py
  ```

## Testing Scenarios

### Scenario 1: MST Computation
1. Go to **Q1: MST**
2. Click "🔄 Compute MST"
3. View spanning tree edges and total distance
4. Compare to original graph total distance

### Scenario 2: Path Finding with Redundancy
1. Go to **Q2: Path Finder**
2. Select any source and destination
3. Click "🎯 Find Shortest Path"
4. Set K=3 and click "📍 Find K-Disjoint Paths"
5. Compare single optimal path vs. 3 independent paths

### Scenario 3: Network Resilience
1. Go to **Q4: Failure Simulation**
2. Click each city and run simulation
3. Observe which cities have highest impact
4. Identify critical infrastructure nodes

### Scenario 4: Frequency Allocation
1. Go to **Q5: Graph Coloring** 
2. Click "🎨 Compute Graph Coloring"
3. View frequency band assignment
4. Check that adjacent hubs have different frequencies

## Data Persistence

- **Graph State**: Persists during session (while app is running)
- **Session**: Resets when you refresh page or restart app
- **No External Storage**: All data is in-memory (educational tool)

## Export & Integration

### Exporting Graph Data
```python
# From Python REPL after running app
from graph.graph_model import EmergencyGraph
graph = EmergencyGraph()
# ... populate graph ...

# Get edges
edges = graph.get_all_edges()
for u, v, weight in edges:
    print(f"{u} -> {v}: {weight}")
```

### API for Integration
All core algorithms are available as Python functions:
```python
from graph.mst import kruskal_mst
from graph.paths import dijkstra_shortest_path
from graph.failure import FailureAnalyzer
from graph.coloring import greedy_graph_coloring
from tree.rebalance import rebalance_tree
```

## Performance Guidelines

| Network Size | Rendering | Algorithms |
|--------------|-----------|-----------|
| <20 nodes | Instant | <100ms |
| 20-50 nodes | Smooth | <500ms |
| 50-100 nodes | Acceptable | <2s |
| 100+ nodes | Slow | >5s |

## Need Help?

- **Algorithm Details**: See `IMPLEMENTATION_SUMMARY.md`
- **Code Structure**: See project README.md
- **Assignment**: See `SUBMISSION_CHECKLIST.md`
- **Dependencies**: See `requirements.txt`

---

**Happy Simulating!** 🎉
