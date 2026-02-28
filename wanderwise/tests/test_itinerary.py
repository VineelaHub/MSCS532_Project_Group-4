from src.models import Attraction, UserPrefs
from src.itinerary import WanderWiseEngine

def mm(h,m): return h*60+m

def test_itinerary_invariants():
    attractions = [
        Attraction("a1","Museum",37.78,-122.41,frozenset({"museum","scenic"}),20,4.6,mm(10,0),mm(17,0),60),
        Attraction("a2","View",37.79,-122.42,frozenset({"scenic"}),0,4.7,mm(0,0),mm(23,59),60),
        Attraction("a3","Food",37.80,-122.40,frozenset({"food"}),15,4.4,mm(11,0),mm(18,0),60),
    ]
    prefs = UserPrefs(desired_tags=frozenset({"museum","scenic"}), budget=60, day_start_min=mm(10,0), day_end_min=mm(18,0), radius_km=10.0)
    engine = WanderWiseEngine(attractions)
    plan = engine.build_day_plan(prefs, start_latlon=(37.78,-122.41))

    # Invariants: no overlap, within day window, cost <= budget
    total = sum(s.cost for s in plan)
    assert total <= 60

    for s in plan:
        assert prefs.day_start_min <= s.start_min < s.end_min <= prefs.day_end_min

    # Overlap check
    intervals = [(s.start_min, s.end_min) for s in plan]
    intervals.sort()
    for i in range(1, len(intervals)):
        assert intervals[i-1][1] <= intervals[i][0]