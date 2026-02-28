from src.interval_tree import IntervalTree

def test_overlap_detection():
    t = IntervalTree()
    t.insert(600, 700)  # 10:00-11:40
    assert t.has_overlap(650, 680) is True
    assert t.has_overlap(700, 730) is False  # boundary touch is OK
    assert t.has_overlap(500, 600) is False