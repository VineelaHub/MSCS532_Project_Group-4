# WanderWise: Intelligent Itinerary Planning Engine

WanderWise is a sophisticated itinerary planning system that generates optimized day plans for tourists. It leverages advanced data structures and algorithms to efficiently filter, score, and sequence attractions based on user preferences, geographic location, and time constraints.

## 📋 Project Overview

WanderWise solves the tourist itinerary problem by:
- **Filtering attractions** based on user preferences (desired tags, budget constraints)
- **Spatial indexing** using K-D trees for proximity-based queries
- **Temporal scheduling** with interval trees for availability management
- **Score-based optimization** considering ratings, travel time, costs, and tag matches
- **Route planning** using graph algorithms to minimize travel between attractions

## 🔑 Key Components

### Core Data Structures

**models.py**: Defines the domain models:
- `Attraction`: Represents a tourist destination with location, tags, cost, hours, duration, and rating
- `UserPrefs`: Encodes user preferences (desired tags, budget, time window, max stops, search radius)
- `haversine_km()`: Calculates geographic distance between coordinates

**Tag Index** (`tag_index.py`): Fast filtering of attractions by tags
- Enables O(1) lookup of attractions matching user preferences

**K-D Tree** (`spatial_kdtree.py`): Spatial indexing for geographic queries
- Enables efficient radius searches to find attractions near a location
- Supports proximity-based candidate generation

**Interval Tree** (`interval_tree.py`): Manages temporal constraints
- Detects overlaps between attraction visiting times
- Validates schedule feasibility

**Travel Graph** (`graph.py`): Route optimization
- K-nearest neighbor graph construction
- Shortest path computation for travel planning

### Main Engine

**itinerary.py**: `WanderWiseEngine` orchestrates the planning workflow:
1. Builds spatial, tag, and graph indices on initialization
2. Filters candidate attractions using tag preferences and spatial constraints
3. Greedily selects attractions based on scoring function: `rating × 2 + tag_bonus × 1.5 - travel_time / 15 - cost / 20`
4. Validates time constraints and schedules feasible stops
5. Returns optimized list of stops with timing and travel info

## 🚀 Getting Started

### Installation

1. Install dependencies:
```bash
cd wanderwise
pip install -r requirements.txt
```

### Run Demo

Generate a sample itinerary for San Francisco attractions:
```bash
cd wanderwise
python -c "from src.wanderwise.demo import main; main()"
```

**Sample Output:**
```
WanderWise (SF) Day Plan
1. Golden Gate Bridge (ggb) | 10:00-11:00 | travel≈15m | cost=$0 | score=8.95
2. Twin Peaks Viewpoint (twinpeaks) | 11:10-12:10 | travel≈5m | cost=$0 | score=8.73
3. de Young Museum (deyoung) | 12:30-14:00 | travel≈20m | cost=$20 | score=7.31
Total cost: $20
```

## 🧪 Testing

Run the test suite:
```bash
cd wanderwise
python -m pytest tests/ -v
```

**Test Coverage:**
- `test_graph.py`: Shortest path computation
- `test_interval_tree.py`: Time overlap detection
- `test_itinerary.py`: Itinerary invariants
- `test_kdtree.py`: Radius search queries
- `test_tag_index.py`: Filtering and tag matching

All tests should pass:
```
============================= 5 passed =============================
```

## 📊 Benchmarking

Evaluate performance across different dataset sizes:
```bash
cd wanderwise
python -c "from src.wanderwise.benchmark import benchmark; benchmark()"
```

Benchmarks test on datasets of sizes: 50, 500, 2000, 5000 attractions
- Measures execution time and peak memory usage
- Generates CSV results and visualization plots
- Results saved in `results/` directory

## 🔍 Algorithm Complexity

| Operation | Time Complexity | Space Complexity |
|-----------|-----------------|------------------|
| Tag filtering | O(m) | O(i) |
| Radius search (K-D tree) | O(log n + m) | O(n) |
| Interval overlap detection | O(k log k) | O(k) |
| Graph construction (K-NN) | O(n²) | O(n + e) |
| Itinerary generation | O(c × n) | O(n) |

*n = attractions, m = matching attractions, k = stops, c = max_stops, i = tag index size, e = edges*

## 📋 Requirements

- Python 3.x
- pytest >= 7.0.0
- matplotlib >= 3.0.0
- numpy >= 1.20.0

## 🎯 Workflow

1. **User Input**: Specify preferences (tags, budget, time window, location)
2. **Index Building**: Create spatial, tag, and graph indices (one-time)
3. **Candidate Generation**: Filter by tags and spatial proximity
4. **Greedy Selection**: Score and select highest-value attractions
5. **Validation**: Check time feasibility with interval tree
6. **Optimization**: Route between selected attractions
7. **Output**: Return ordered itinerary with timing and travel info

## 📝 License

MSCS532 Project Group 4
