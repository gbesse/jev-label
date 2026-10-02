"""Reserve a holdout before choosing an uncertainty review queue."""
import json

from jev_label import select, split_holdout

ROWS = [
    {"id": "a", "probability": 0.51},
    {"id": "b", "probability": 0.10},
    {"id": "c", "probability": 0.48},
    {"id": "d", "probability": 0.90},
    {"id": "e", "probability": 0.60},
    {"id": "f", "probability": 0.30},
]


def example():
    pool, holdout = split_holdout(ROWS, fraction=1 / 3, seed=7)
    holdout_ids = {row["id"] for row in holdout}
    queue = select(pool, "uncertainty", 2, holdout_ids=holdout_ids)
    queue_ids = [row["id"] for row in queue]
    assert holdout_ids.isdisjoint(queue_ids)
    return {
        "source": "synthetic fixture; no model calls or quality claim",
        "holdout_ids": sorted(holdout_ids),
        "review_queue_ids": queue_ids,
        "holdout_leakage": False,
    }


if __name__ == "__main__":
    print(json.dumps(example(), indent=2, sort_keys=True))
