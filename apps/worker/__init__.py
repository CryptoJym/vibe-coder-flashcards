"""Worker package setup."""

from __future__ import annotations

import os

from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL: str = os.environ.get("DATABASE_URL", "postgresql+psycopg2://postgres:postgres@localhost:5432/vibe")

engine = create_engine(DATABASE_URL, echo=False, future=True)


def init_db() -> None:
    """Create tables if they don't exist."""

    from packages.core import models as _m  # noqa: WPS433 (import inside function)

    SQLModel.metadata.create_all(engine)
