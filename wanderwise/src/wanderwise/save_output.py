"""Demo script that saves output to a file."""
from .models import Attraction, UserPrefs, haversine_km
from .tag_index import TagIndex
from .spatial_kdtree import KDTree
from .graph import TravelGraph
from .interval_tree import IntervalTree
from .itinerary import WanderWiseEngine

output = []

def log(msg=""):
    """Log message to both console and file."""
    output.append(msg)
    print(msg)

log('=' * 60)
log('WANDERWISE PROJECT - COMPLETE MODULE OUTPUT')
log('=' * 60)

# TAG INDEX
log('\n1. TAG INDEX - Filter attractions by tags')
log('-' * 60)
a1 = Attraction('1', 'Museum', 0, 0, frozenset({'museum', 'art'}), 20, 4.6, 600, 1020, 60)
a2 = Attraction('2', 'Park', 0, 0, frozenset({'park', 'scenic'}), 0, 4.7, 0, 1439, 60)
idx = TagIndex()
idx.build([a1, a2])
log(f'Available attractions: Museum, Park')
log(f'Places with tag "museum": {idx.filter_all(["museum"])}')
log(f'Places with tag "park": {idx.filter_all(["park"])}')
log(f'Places with both "museum" AND "art": {idx.filter_all(["museum", "art"])}')

# SPATIAL SEARCH (KDTree)
log('\n2. SPATIAL KDTREE - Find nearby attractions')
log('-' * 60)
near = Attraction('near', 'Nearby Place', 0.0, 0.0, frozenset({'x'}), 0, 5, 0, 1000, 10)
far = Attraction('far', 'Distant Place', 10.0, 10.0, frozenset({'x'}), 0, 5, 0, 1000, 10)
kd = KDTree()
kd.build([near, far])
results = kd.radius_search((0.0, 0.0), 50.0)
log(f'Query: Find places within 50km of coordinates (0.0, 0.0)')
log(f'Results: {[r.name for r in results]}')

# HAVERSINE DISTANCE
log('\n3. HAVERSINE DISTANCE - Calculate travel distance')
log('-' * 60)
dist_km = haversine_km((0.0, 0.0), (0.001, 0.001))
log(f'Distance from (0.0, 0.0) to (0.001, 0.001): {dist_km:.2f} km')

# GRAPH & SHORTEST PATH
log('\n4. TRAVEL GRAPH - Compute shortest travel times')
log('-' * 60)
g = TravelGraph()
attractions = [
    Attraction('a', 'Attraction A', 0, 0, frozenset(), 0, 5, 0, 1000, 10),
    Attraction('b', 'Attraction B', 0, 0.01, frozenset(), 0, 5, 0, 1000, 10),
    Attraction('c', 'Attraction C', 0, 0.02, frozenset(), 0, 5, 0, 1000, 10),
]
g.build_knn(attractions, k=2)
log(f'Built k-NN graph with k=2')
log(f'Shortest time from A to B: {g.shortest_time("a", "b"):.2f} minutes')
log(f'Shortest time from A to C: {g.shortest_time("a", "c"):.2f} minutes')
log(f'Shortest time from A to A: {g.shortest_time("a", "a"):.2f} minutes')

# INTERVAL TREE
log('\n5. INTERVAL TREE - Check scheduling conflicts')
log('-' * 60)
t = IntervalTree()
t.insert(600, 700)  # 10:00 - 11:40 (minutes)
log(f'Booked interval: [600-700] (10:00-11:40)')
log(f'Does [650-680] overlap? {t.has_overlap(650, 680)}')
log(f'Does [700-730] overlap? {t.has_overlap(700, 730)} (boundary touching is OK)')
log(f'Does [500-600] overlap? {t.has_overlap(500, 600)}')

# ITINERARY ENGINE
log('\n6. ITINERARY ENGINE - Generate daily itineraries')
log('-' * 60)
prefs = UserPrefs(
    desired_tags=frozenset({'museum', 'park'}),
    budget=100,
    day_start_min=600,
    day_end_min=1020,
    radius_km=10.0
)
engine = WanderWiseEngine([a1, a2])
plan = engine.build_day_plan(prefs, start_latlon=(0, 0))
log(f'User preferences:')
log(f'  Tags: {list(prefs.desired_tags)}')
log(f'  Budget: ${prefs.budget}')
log(f'  Hours: {prefs.day_start_min//60}:00 - {prefs.day_end_min//60}:00')
log(f'\nGenerated itinerary ({len(plan)} stops):')
total_cost = 0
for i, stop in enumerate(plan, 1):
    log(f'  {i}. {stop.name}')
    log(f'     Time: {stop.start_min}-{stop.end_min} minutes')
    log(f'     Cost: ${stop.cost}')
    total_cost += stop.cost
log(f'  Total Cost: ${total_cost}')

log('\n' + '=' * 60)
log('✓ All modules executed successfully!')
log('=' * 60)

# Save to file
output_file = 'output.md'
with open(output_file, 'w', encoding='utf-8') as f:
    f.write('\n'.join(output))

print(f'\n✓ Output saved to: {output_file}')
