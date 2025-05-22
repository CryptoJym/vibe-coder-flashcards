"""Pydantic + SQLModel domain models.

These models are used for both API schemas and DB tables.
All models inherit from SQLModel for seamless ORM + pydantic validation.
"""
from __future__ import annotations

import datetime as _dt
from typing import List
from sqlmodel import SQLModel, Field


class User(SQLModel, table=True):
    """Application user.

    For now only magic-link email auth, later we can add OAuth.
    """

    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True, nullable=False)
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)


class Feed(SQLModel, table=True):
    """Twitter account we track."""

    id: int | None = Field(default=None, primary_key=True)
    handle: str = Field(unique=True, index=True, nullable=False)
    last_post_id: str | None = None  # last ingested tweet id for incremental fetch


class Post(SQLModel, table=True):
    """Tweet that was summarised."""

    id: int | None = Field(default=None, primary_key=True)
    feed_id: int = Field(foreign_key="feed.id", nullable=False)
    tweet_id: str = Field(index=True, unique=True, nullable=False)
    text: str
    created_at: _dt.datetime = Field(default_factory=_dt.datetime.utcnow)


class Flashcard(SQLModel, table=True):
    """Generated flashcard."""

    id: int | None = Field(default=None, primary_key=True)
    owner_id: int = Field(foreign_key="user.id", nullable=False)
    post_id: int = Field(foreign_key="post.id", nullable=False)
    question: str
    answer: str
    ease_factor: float = 2.5  # SM-2 default
    interval: int = 1  # days until next review
    repetitions: int = 0
    next_review: _dt.date = Field(default_factory=_dt.date.today)



__all__: list[str] = [
    "User",
    "Feed",
    "Post",
    "Flashcard",
]
