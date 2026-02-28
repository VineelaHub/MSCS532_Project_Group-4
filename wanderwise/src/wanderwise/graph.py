from __future__ import annotations
from typing import Dict, List, Tuple
import heapq

try:
    from models import Attraction, haversine_km
except ModuleNotFoundError:
    from .models import Attraction, haversine_km


class TravelGraph:
    """
    Sparse weighted graph (kNN) + Dijkstra shortest path.
    Edge weights represent approximate travel minutes.
    """

    def __init__(self) -> None:
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def build_knn(self, items: List[Attraction], k: int = 6, minutes_per_km: float = 12.0) -> None:
        self.adj.clear()
        for a in items:
            dists: List[Tuple[float, str]] = []
            for b in items:
                if a.id == b.id:
                    continue
                dist = haversine_km((a.lat, a.lon), (b.lat, b.lon))
                dists.append((dist, b.id))
            dists.sort(key=lambda x: x[0])
            neighbors = dists[:k]
            self.adj[a.id] = [(bid, dist * minutes_per_km) for dist, bid in neighbors]

    def shortest_time(self, src: str, dst: str) -> float:
        if src == dst:
            return 0.0

        pq: List[Tuple[float, str]] = [(0.0, src)]
        dist: Dict[str, float] = {src: 0.0}

        while pq:
            d, u = heapq.heappop(pq)
            if u == dst:
                return d
            if d != dist.get(u, float("inf")):
                continue
            for v, w in self.adj.get(u, []):
                nd = d + w
                if nd < dist.get(v, float("inf")):
                    dist[v] = nd
                    heapq.heappush(pq, (nd, v))

        return float("inf")