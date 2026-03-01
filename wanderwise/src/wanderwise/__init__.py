"""WanderWise - Intelligent travel itinerary planning engine."""
from .models import Attraction, UserPrefs, haversine_km
from .itinerary import WanderWiseEngine, PlanStop
from .tag_index import TagIndex
from .spatial_kdtree import KDTree
from .graph import TravelGraph
from .interval_tree import IntervalTree

__all__ = [
    "Attraction",
    "UserPrefs",
    "haversine_km",
    "WanderWiseEngine",
    "PlanStop",
    "TagIndex",
    "KDTree",
    "TravelGraph",
    "IntervalTree",
]
