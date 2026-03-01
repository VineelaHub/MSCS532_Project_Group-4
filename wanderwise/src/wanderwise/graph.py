from __future__ import annotations
from typing import Dict, List, Tuple
import heapq
from .models import Attraction, haversine_km
from functools import lru_cache


class TravelGraph:
    """
    Sparse weighted graph (kNN) + Dijkstra shortest path.
    Edge weights represent approximate travel minutes.

    Phase 3 upgrade:
    - Added LRU caching for shortest_time() to avoid repeated Dijkstra calls.
    """

    def __init__(self) -> None:
        self.adj: Dict[str, List[Tuple[str, float]]] = {}

    def build_knn(self, items: List[Attraction], k: int = 6, minutes_per_km: float = 12.0) -> None:
        """Build k-NN graph with travel time edge weights."""
        self.adj.clear()
        self.shortest_time.cache_clear()  # Clear cache when graph changes

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

    def _shortest_time_dijkstra(self, src: str, dst: str) -> float:
        """Dijkstra's algorithm for shortest path."""
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

    @lru_cache(maxsize=5000)
    def shortest_time(self, src: str, dst: str) -> float:
        """Get shortest travel time (cached) between attractions."""
        return self._shortest_time_dijkstra(src, dst)