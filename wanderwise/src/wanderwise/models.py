from __future__ import annotations
from dataclasses import dataclass
from typing import FrozenSet, Tuple
import math


@dataclass(frozen=True)
class Attraction:
    id: str
    name: str
    lat: float
    lon: float
    tags: FrozenSet[str]
    cost: float
    rating: float
    open_min: int
    close_min: int
    duration_min: int


@dataclass(frozen=True)
class UserPrefs:
    desired_tags: FrozenSet[str]
    budget: float
    day_start_min: int
    day_end_min: int
    max_stops: int = 6
    radius_km: float = 2.0


def haversine_km(a: Tuple[float, float], b: Tuple[float, float]) -> float:
    """Calculate distance between two geographic points (lat, lon) in km."""
    lat1, lon1 = a
    lat2, lon2 = b
    r = 6371.0  # Earth's radius in km
    p1 = math.radians(lat1)
    p2 = math.radians(lat2)
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    x = (math.sin(dlat / 2) ** 2) + math.cos(p1) * math.cos(p2) * (math.sin(dlon / 2) ** 2)
    return 2 * r * math.asin(math.sqrt(x))