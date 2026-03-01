from wanderwise.models import Attraction
from wanderwise.graph import TravelGraph

def test_shortest_time_basic():
    a = Attraction("a","A",0,0,frozenset({"x"}),0,5,0,1000,10)
    b = Attraction("b","B",0,0.01,frozenset({"x"}),0,5,0,1000,10)
    c = Attraction("c","C",0,0.02,frozenset({"x"}),0,5,0,1000,10)

    g = TravelGraph()
    g.build_knn([a,b,c], k=2)

    assert g.shortest_time("a","a") == 0.0
    assert g.shortest_time("a","b") != float("inf")