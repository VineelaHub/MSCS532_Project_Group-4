
import time
import tracemalloc
import os
import csv
import matplotlib.pyplot as plt

from .dataset_generator import generate_attractions

# import your actual itinerary builder
from .itinerary import WanderWiseEngine
from .models import UserPrefs


def run_pipeline(attractions):
    """Execute full WanderWise pipeline on attractions dataset."""
    engine = WanderWiseEngine(attractions)
    
    prefs = UserPrefs(
        desired_tags=frozenset({"museum", "scenic"}),
        budget=60,
        day_start_min=600,
        day_end_min=1080,
        max_stops=6,
        radius_km=2.0
    )
    
    itinerary = engine.build_day_plan(prefs, start_latlon=(37.7749, -122.4194))

    return itinerary


def benchmark():
    sizes = [50, 500, 2000, 5000]
    results = []

    os.makedirs("results", exist_ok=True)

    for n in sizes:
        attractions = generate_attractions(n)

        tracemalloc.start()
        start = time.perf_counter()

        run_pipeline(attractions)

        end = time.perf_counter()
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        runtime = end - start
        peak_kb = peak / 1024

        print(f"N={n} | Runtime={runtime:.4f}s | PeakMem={peak_kb:.1f}KB")

        results.append((n, runtime, peak_kb))

    # Save CSV
    with open("results/benchmark_results.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["N", "RuntimeSeconds", "PeakMemoryKB"])
        writer.writerows(results)

    # Plot runtime
    xs = [r[0] for r in results]
    ys = [r[1] for r in results]

    plt.plot(xs, ys, marker="o")
    plt.xlabel("Number of Attractions")
    plt.ylabel("Runtime (seconds)")
    plt.title("WanderWise Scaling Performance")
    plt.savefig("results/runtime_plot.png")
    plt.close()

    # Plot memory
    ys_mem = [r[2] for r in results]

    plt.plot(xs, ys_mem, marker="o")
    plt.xlabel("Number of Attractions")
    plt.ylabel("Peak Memory (KB)")
    plt.title("Memory Usage vs Dataset Size")
    plt.savefig("results/memory_plot.png")
    plt.close()


if __name__ == "__main__":
    benchmark()