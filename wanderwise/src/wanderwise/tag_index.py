from __future__ import annotations
from typing import Dict, Iterable, Set
from .models import Attraction


class TagIndex:
    """Inverted index: tag -> set(attraction_id)."""

    def __init__(self) -> None:
        self.inv: Dict[str, Set[str]] = {}

    def build(self, attractions: Iterable[Attraction]) -> None:
        self.inv.clear()
        for a in attractions:
            for t in a.tags:
                self.inv.setdefault(t, set()).add(a.id)

    def filter_all(self, tags: Iterable[str]) -> Set[str]:
        """AND query: intersection of posting lists."""
        tags = list(tags)
        if not tags:
            return set()
        sets = [self.inv.get(t, set()) for t in tags]
        sets.sort(key=len)
        if not sets or not sets[0]:
            return set()
        out = sets[0].copy()
        for s in sets[1:]:
            out.intersection_update(s)
            if not out:
                break
        return out