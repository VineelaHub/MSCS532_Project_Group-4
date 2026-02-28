from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, List, Tuple, Set
import heapq

from .models import Attraction, UserPrefs, haversine_km
from .tag_index import TagIndex
from .spatial_kdtree import KDTree
from .interval_tree import IntervalTree
from .graph import TravelGraph


@dataclass
class PlanStop:
    attraction_id: str
    name: str
    start_min: int
    end_min: int
    travel_min: int
    cost: float
    score: float


def _score(a: Attraction, prefs: UserPrefs, travel_min: float) -> float:
    """
    Simple normalized scoring for PoC.
    Higher rating + more tag matches, penalize travel time and cost.
    """
    tag_bonus = len(a.tags.intersection(prefs.desired_tags))
    return (a.rating * 2.0) + (tag_bonus * 1.5) - (travel_min / 15.0) - (a.cost / 20.0)


class WanderWiseEngine:
    def __init__(self, attractions: List[Attraction]) -> None:
        self.attractions_by_id: Dict[str, Attraction] = {a.id: a for a in attractions}

        self.tag_index = TagIndex()
        self.tag_index.build(attractions)

        self.kdtree = KDTree()
        self.kdtree.build(attractions)

        self.graph = TravelGraph()
        self.graph.build_knn(attractions, k=6)

    def build_day_plan(self, prefs: UserPrefs, start_latlon: Tuple[float, float]) -> List[PlanStop]:
        # Tag filtering (AND). If empty result, fall back to all.
        eligible = self.tag_index.filter_all(prefs.desired_tags)
        if not eligible:
            eligible = set(self.attractions_by_id.keys())

        used: Set[str] = set()
        schedule = IntervalTree()

        plan: List[PlanStop] = []
        current_time = prefs.day_start_min
        current_loc = start_latlon
        spent = 0.0

        while len(plan) < prefs.max_stops and current_time < prefs.day_end_min:
            nearby = self.kdtree.radius_search(current_loc, prefs.radius_km)

            heap: List[Tuple[float, str, int, int, int]] = []
            # heap items: (-score, id, travel_min, start, end)
            for a in nearby:
                if a.id in used:
                    continue
                if a.id not in eligible:
                    continue
                if spent + a.cost > prefs.budget:
                    continue

                # Quick travel estimate (cheap): haversine
                travel_min = int(haversine_km(current_loc, (a.lat, a.lon)) * 12.0)

                # compute feasible start and end times
                start = max(current_time + travel_min, a.open_min)
                end = start + a.duration_min

                # feasibility checks
                if end > prefs.day_end_min:
                    continue
                if end > a.close_min:
                    continue
                if schedule.has_overlap(start, end):
                    continue

                sc = _score(a, prefs, travel_min)
                heapq.heappush(heap, (-sc, a.id, travel_min, start, end))

            if not heap:
                break

            neg_sc, best_id, travel_min, start, end = heapq.heappop(heap)
            a = self.attractions_by_id[best_id]

            schedule.insert(start, end)
            used.add(best_id)
            spent += a.cost

            plan.append(
                PlanStop(
                    attraction_id=best_id,
                    name=a.name,
                    start_min=start,
                    end_min=end,
                    travel_min=travel_min,
                    cost=a.cost,
                    score=-neg_sc,
                )
            )

            current_time = end
            current_loc = (a.lat, a.lon)

        return plan