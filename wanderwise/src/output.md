============================================================
WANDERWISE PROJECT - COMPLETE MODULE OUTPUT
============================================================

1. TAG INDEX - Filter attractions by tags
------------------------------------------------------------
Available attractions: Museum, Park
Places with tag "museum": {'1'}
Places with tag "park": {'2'}
Places with both "museum" AND "art": {'1'}

2. SPATIAL KDTREE - Find nearby attractions
------------------------------------------------------------
Query: Find places within 50km of coordinates (0.0, 0.0)
Results: ['Nearby Place']

3. HAVERSINE DISTANCE - Calculate travel distance
------------------------------------------------------------
Distance from (0.0, 0.0) to (0.001, 0.001): 0.16 km

4. TRAVEL GRAPH - Compute shortest travel times
------------------------------------------------------------
Built k-NN graph with k=2
Shortest time from A to B: 13.34 minutes
Shortest time from A to C: 26.69 minutes
Shortest time from A to A: 0.00 minutes

5. INTERVAL TREE - Check scheduling conflicts
------------------------------------------------------------
Booked interval: [600-700] (10:00-11:40)
Does [650-680] overlap? True
Does [700-730] overlap? False (boundary touching is OK)
Does [500-600] overlap? False

6. ITINERARY ENGINE - Generate daily itineraries
------------------------------------------------------------
User preferences:
  Tags: ['park', 'museum']
  Budget: $100
  Hours: 10:00 - 17:00

Generated itinerary (2 stops):
  1. Park
     Time: 600-660 minutes
     Cost: $0
  2. Museum
     Time: 660-720 minutes
     Cost: $20
  Total Cost: $20

============================================================
✓ All modules executed successfully!
============================================================