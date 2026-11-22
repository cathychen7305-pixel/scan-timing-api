from decimal import Decimal


def summarize(timestamps: list[int], deadline_us: int) -> dict:
    """Evaluate the gaps between successive synthetic scan commands."""
    gaps = [end - start for start, end in zip(timestamps, timestamps[1:])]
    if any(gap <= 0 for gap in gaps):
        raise ValueError("timestamps_us must be strictly increasing")
    ordered = sorted(gaps)
    misses = sum(gap > deadline_us for gap in gaps)
    return {
        "interval_count": len(gaps),
        "deadline_misses": misses,
        "miss_rate_pct": float(round(Decimal(100 * misses) / len(gaps), 3)),
        "max_gap_us": ordered[-1],
        "p95_gap_us": ordered[(95 * len(gaps) + 99) // 100 - 1],
    }
