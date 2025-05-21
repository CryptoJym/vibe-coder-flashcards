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
