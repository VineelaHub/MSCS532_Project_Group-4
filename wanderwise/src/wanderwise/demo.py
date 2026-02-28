from __future__ import annotations
from models import Attraction, UserPrefs
from .itinerary import WanderWiseEngine


def mm(h: int, m: int) -> int:
    return h * 60 + m


def fmt(t: int) -> str:
    return f"{t//60:02d}:{t%60:02d}"


def main() -> None:
    # San Francisco-style mini dataset (PoC)
    attractions = [
        Attraction(
            id="ggb",
            name="Golden Gate Bridge",
            lat=37.8199,
            lon=-122.4783,
            tags=frozenset({"scenic", "outdoor"}),
            cost=0,
            rating=4.8,
            open_min=mm(0, 0),
            close_min=mm(23, 59),
            duration_min=60,
        ),
        Attraction(
            id="ggp",
            name="Golden Gate Park",
            lat=37.7694,
            lon=-122.4862,
            tags=frozenset({"nature", "outdoor", "scenic"}),
            cost=0,
            rating=4.7,
            open_min=mm(6, 0),
            close_min=mm(20, 0),
            duration_min=75,
        ),
        Attraction(
            id="deyoung",
            name="de Young Museum",
            lat=37.7715,
            lon=-122.4687,
            tags=frozenset({"museum", "art", "indoor"}),
            cost=20,
            rating=4.6,
            open_min=mm(9, 30),
            close_min=mm(17, 15),
            duration_min=90,
        ),
        Attraction(
            id="twinpeaks",
            name="Twin Peaks Viewpoint",
            lat=37.7544,
            lon=-122.4477,
            tags=frozenset({"scenic", "outdoor"}),
            cost=0,
            rating=4.7,
            open_min=mm(0, 0),
            close_min=mm(23, 59),
            duration_min=60,
        ),
        Attraction(
            id="ferry",
            name="Ferry Building Marketplace",
            lat=37.7955,
            lon=-122.3937,
            tags=frozenset({"food", "scenic"}),
            cost=15,
            rating=4.5,
            open_min=mm(10, 0),
            close_min=mm(18, 0),
            duration_min=60,
        ),
        Attraction(
            id="exploratorium",
            name="Exploratorium",
            lat=37.8014,
            lon=-122.3977,
            tags=frozenset({"museum", "science", "indoor"}),
            cost=25,
            rating=4.7,
            open_min=mm(10, 0),
            close_min=mm(17, 0),
            duration_min=120,
        ),
    ]

    prefs = UserPrefs(
        desired_tags=frozenset({"museum", "scenic"}),
        budget=60,
        day_start_min=mm(10, 0),
        day_end_min=mm(18, 0),
        max_stops=6,
        radius_km=8.0,  # larger radius for PoC so we get candidates across SF
    )

    engine = WanderWiseEngine(attractions)

    # Union Square approximate coordinates
    plan = engine.build_day_plan(prefs, start_latlon=(37.7879, -122.4074))

    print("\nWanderWise (SF) Day Plan")
    if not plan:
        print("No feasible plan found for the given constraints.")
        return

    total_cost = 0.0
    for i, s in enumerate(plan, 1):
        total_cost += s.cost
        print(
            f"{i}. {s.name} ({s.attraction_id}) | {fmt(s.start_min)}-{fmt(s.end_min)} "
            f"| travel≈{s.travel_min}m | cost=${s.cost:.0f} | score={s.score:.2f}"
        )
    print(f"Total cost: ${total_cost:.0f}\n")


if __name__ == "__main__":
    main()