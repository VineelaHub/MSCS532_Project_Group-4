from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Tuple
from .models import Attraction, haversine_km


@dataclass
class _Node:
    a: Attraction
    axis: int
    left: Optional["_Node"] = None
    right: Optional["_Node"] = None


class KDTree:
    """2D KD-tree for radius queries over (lat, lon)."""

    def __init__(self) -> None:
        # Initialize empty KD-tree
        self.root: Optional[_Node] = None

    def build(self, items: List[Attraction]) -> None:
        # Build balanced KD-tree from attractions
        pts = items[:]
        self.root = self._build(pts, 0)

    def _build(self, pts: List[Attraction], depth: int) -> Optional[_Node]:
        # Recursively build balanced tree using median partitioning
        if not pts:
            return None
        axis = depth % 2
        pts.sort(key=lambda x: (x.lat, x.lon)[axis])
        m = len(pts) // 2
        return _Node(
            a=pts[m],
            axis=axis,
            left=self._build(pts[:m], depth + 1),
            right=self._build(pts[m + 1 :], depth + 1),
        )

    def radius_search(self, center: Tuple[float, float], r_km: float) -> List[Attraction]:
        # Find all attractions within a given radius from center point
        out: List[Attraction] = []
        self._rad(self.root, center, r_km, out)
        return out

    def _rad(self, node: Optional[_Node], center: Tuple[float, float], r_km: float, out: List[Attraction]) -> None:
        # Recursively search tree and prune branches outside radius
        if node is None:
            return

        # add if in radius
        if haversine_km((node.a.lat, node.a.lon), center) <= r_km:
            out.append(node.a)

        # choose traversal side based on split axis
        coord = center[0] if node.axis == 0 else center[1]
        split = node.a.lat if node.axis == 0 else node.a.lon

        first = node.left if coord < split else node.right
        second = node.right if coord < split else node.left

        self._rad(first, center, r_km, out)

        # prune: conservative conversion of degrees to km
        # 1 degree latitude ~111 km; longitude varies but this is safe for pruning.
        if abs(coord - split) * 111.0 <= r_km:
            self._rad(second, center, r_km, out)