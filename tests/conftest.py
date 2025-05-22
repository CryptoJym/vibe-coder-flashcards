"""Ensure project root is on sys.path during pytest collection."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import pytest
from alembic import command
from alembic.config import Config


@pytest.fixture(scope="session", autouse=True)
def apply_migrations() -> None:
    """Apply Alembic migrations before tests run."""

    cfg = Config(str(ROOT / "alembic.ini"))
    command.upgrade(cfg, "head")
    yield
