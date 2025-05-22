"""APScheduler cron jobs for spaced repetition."""
from __future__ import annotations

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import date
from typing import Iterable

from packages.core.spaced_repetition import Card, schedule_cards

# In-memory card store used for demo & tests
CARDS: list[Card] = []


def daily_job(today: date | None = None, cards: Iterable[Card] | None = None) -> None:
    """Run daily scheduling for all cards."""
    if today is None:
        today = date.today()
    if cards is None:
        cards = CARDS
    schedule_cards(cards, today)


def start_scheduler() -> None:
    """Start APScheduler with daily job at midnight."""
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(daily_job, "cron", hour=0, minute=0)
    scheduler.start()


def main(argv: list[str] | None = None) -> None:
    """Simple CLI entrypoint."""
    import argparse

    parser = argparse.ArgumentParser(description="Worker cron utilities")
    parser.add_argument("command", choices=["daily", "run"], help="Run once or start scheduler")
    args = parser.parse_args(argv)

    if args.command == "daily":
        daily_job()
    elif args.command == "run":
        start_scheduler()


if __name__ == "__main__":
    main()

"""Simple AnyIO cron to run ingestor daily."""
from __future__ import annotations

import anyio
from loguru import logger

from packages.core.models import Feed
from apps.worker.ingestors.twitter import ingest_handles
from apps.worker import init_db

HANDLES = [
    "dr_cintas",
    "GoogleLabs",
    "kregenrek",
    "GeminiApp",
    "OpenAI",
    "AnthropicAI",
    "GoogleAI",
]


async def job() -> None:  # noqa: D401
    logger.info("Running ingest job…")
    ingest_handles(HANDLES)


async def main() -> None:  # noqa: D401
    init_db()
    while True:
        await job()
        # sleep 24h
        await anyio.sleep(60 * 60 * 24)


if __name__ == "__main__":
    anyio.run(main)
