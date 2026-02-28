from src.models import Attraction
from src.spatial_kdtree import KDTree

def test_radius_search():
    # Points near (0,0) and far away
    near = Attraction("n","Near",0.0,0.0,frozenset({"x"}),0,5,0,1000,10)
    far = Attraction("f","Far",10.0,10.0,frozenset({"x"}),0,5,0,1000,10)

    kd = KDTree()
    kd.build([near, far])

    res = kd.radius_search((0.0, 0.0), 50.0)  # 50km radius
    ids = {a.id for a in res}
    assert "n" in ids
    assert "f" not in ids