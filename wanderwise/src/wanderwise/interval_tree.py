from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Tuple


def _overlap(a: Tuple[int, int], b: Tuple[int, int]) -> bool:
    """Half-open interval overlap: [a0,a1) overlaps [b0,b1) iff a0<b1 and b0<a1."""
    return a[0] < b[1] and b[0] < a[1]


@dataclass
class _INode:
    lo: int
    hi: int
    max_hi: int
    left: Optional["_INode"] = None
    right: Optional["_INode"] = None


class IntervalTree:
    """
    Interval tree implemented as an augmented BST:
    each node stores max_hi in its subtree for pruning overlap search.
    """

    def __init__(self) -> None:
        self.root: Optional[_INode] = None

    def insert(self, lo: int, hi: int) -> None:
        if hi <= lo:
            raise ValueError("Invalid interval: hi must be > lo")
        self.root = self._ins(self.root, lo, hi)

    def _ins(self, node: Optional[_INode], lo: int, hi: int) -> _INode:
        if node is None:
            return _INode(lo=lo, hi=hi, max_hi=hi)

        if lo < node.lo:
            node.left = self._ins(node.left, lo, hi)
        else:
            node.right = self._ins(node.right, lo, hi)

        node.max_hi = max(node.max_hi, hi, (node.left.max_hi if node.left else hi), (node.right.max_hi if node.right else hi))
        return node

    def has_overlap(self, lo: int, hi: int) -> bool:
        if hi <= lo:
            return False
        return self._has(self.root, (lo, hi))

    def _has(self, node: Optional[_INode], it: Tuple[int, int]) -> bool:
        if node is None:
            return False

        if _overlap((node.lo, node.hi), it):
            return True

        if node.left is not None and node.left.max_hi > it[0]:
            return self._has(node.left, it)

        return self._has(node.right, it)