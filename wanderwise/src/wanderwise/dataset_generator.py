import random
from .models import Attraction

TAGS_POOL = [
    "museum", "scenic", "outdoor", "historic",
    "food", "nature", "science", "indoor"
]


def generate_attractions(n: int, seed: int = 42):
    """Generate n synthetic attractions with random attributes for testing."""
    random.seed(seed)
    attractions = []
    for i in range(n):
        attractions.append(
            Attraction(
                id=f"A{i}",
                name=f"Attraction {i}",
                lat=random.uniform(37.70, 37.82),
                lon=random.uniform(-122.52, -122.37),
                tags=frozenset(random.sample(TAGS_POOL, random.randint(1, 3))),
                cost=random.randint(0, 30),
                rating=round(random.uniform(3.0, 5.0), 2),
                open_min=600,
                close_min=1080,
                duration_min=random.randint(30, 120),
            )
        )
    return attractions