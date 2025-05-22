"""SM-2 algorithm helper functions."""
from __future__ import annotations

import datetime as _dt

# Google style
def sm2(review_date: _dt.date, quality: int, ease: float, interval: int, reps: int) -> tuple[_dt.date, float, int, int]:
    """Return next review date and updated factors.

    Args:
        review_date: today (usually _dt.date.today())
        quality: 0–5 response quality
        ease: current ease factor
        interval: current interval in days
        reps: number of successful repetitions

    Returns:
        (next_review_date, new_ease, new_interval, new_reps)
    """
    assert 0 <= quality <= 5, "quality must be 0–5"

    if quality < 3:
        # reset
        return review_date + _dt.timedelta(days=1), ease, 1, 0

    new_reps = reps + 1
    if new_reps == 1:
        new_interval = 1
    elif new_reps == 2:
        new_interval = 6
    else:
        new_interval = int(interval * ease)

    # update ease factor
    new_ease = max(1.3, ease + 0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))

    next_review = review_date + _dt.timedelta(days=new_interval)
    return next_review, new_ease, new_interval, new_reps


__all__: list[str] = ["sm2"]
