"""Run a deterministic timing check with the Python standard library."""
from itertools import accumulate, product

from timing import summarize


def main():
    checked = 0
    for gaps in product(range(1, 5), repeat=5):
        times = [0, *accumulate(gaps)]
        result = summarize(times, 2)
        expected_misses = sum(gap in (3, 4) for gap in gaps)
        assert result == {
            "interval_count": 5,
            "deadline_misses": expected_misses,
            "miss_rate_pct": 20 * expected_misses,
            "max_gap_us": max(gaps),
            "p95_gap_us": max(gaps),
        }
        checked += 1
    print(f"Passed {checked} synthetic traces")


if __name__ == "__main__":
    main()
