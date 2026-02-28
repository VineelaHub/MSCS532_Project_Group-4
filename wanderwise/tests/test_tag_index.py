from src.models import Attraction
from src.tag_index import TagIndex

def test_filter_all():
    a1 = Attraction("1","A",0,0,frozenset({"museum","art"}),0,5,0,1000,60)
    a2 = Attraction("2","B",0,0,frozenset({"museum"}),0,5,0,1000,60)
    idx = TagIndex()
    idx.build([a1,a2])

    assert idx.filter_all(["museum"]) == {"1","2"}
    assert idx.filter_all(["museum","art"]) == {"1"}
    assert idx.filter_all(["scenic"]) == set()