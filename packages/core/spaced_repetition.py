from __future__ import annotations

"""Simple SM-2 spaced repetition implementation."""

from dataclasses import dataclass, field
from datetime import date, timedelta
from typing import Optional, Iterable, List

MIN_EASE = 1.3


def sm2(repetition: int, interval: int, ease: float, grade: int) -> tuple[int, int, float]:
    """Apply the SM-2 algorithm for a single review.

    Parameters
    ----------
    repetition:
        Current repetition count for the card.
    interval:
        Current review interval (days).
    ease:
        Current ease factor.
    grade:
        Recall quality grade (0-5).

    Returns
    -------
    tuple[new_repetition, new_interval, new_ease]
    """
    if not 0 <= grade <= 5:
        raise ValueError("grade must be between 0 and 5")

    if grade >= 3:
        if repetition == 0:
            interval = 1
        elif repetition == 1:
            interval = 6
        else:
            interval = int(round(interval * ease))
        repetition += 1
        ease = ease + (0.1 - (5 - grade) * (0.08 + (5 - grade) * 0.02))
        if ease < MIN_EASE:
            ease = MIN_EASE
    else:
        repetition = 0
        interval = 1
        # EF is not changed when answer was incorrect (<3)
    return repetition, interval, ease


@dataclass
class Card:
    """Minimal flashcard model used for scheduling tests."""

    id: int
    question: str
    answer: str
    repetition: int = 0
    interval: int = 0
    ease_factor: float = 2.5
    next_review: date = field(default_factory=date.today)
    grade: Optional[int] = None

    def apply_grade(self, today: date) -> None:
        """Update scheduling fields using stored grade."""
        if self.grade is None:
            return
        self.repetition, self.interval, self.ease_factor = sm2(
            self.repetition, self.interval, self.ease_factor, self.grade
        )
        self.next_review = today + timedelta(days=self.interval)
        self.grade = None


def schedule_cards(cards: Iterable[Card], today: date) -> None:
    """Apply scheduling to all cards."""
    for card in cards:
        card.apply_grade(today)


def due_cards(cards: Iterable[Card], today: date) -> List[Card]:
    """Return cards due for review today."""
    return [c for c in cards if c.next_review <= today]
=======
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
