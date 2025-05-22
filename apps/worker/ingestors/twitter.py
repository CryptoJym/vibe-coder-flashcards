"""Simple Twitter/X ingestor using v2 API.

Fetches latest tweets for configured accounts and stores in DB.
"""
from __future__ import annotations

import os
import httpx
from sqlmodel import Session

from packages.core.models import Feed, Post
from apps.worker import engine

BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN")
API_URL = "https://api.twitter.com/2/tweets"

_HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}


async def fetch_latest(handle: str, since_id: str | None = None) -> list[dict]:  # noqa: D401
    """Return latest tweets for handle since `since_id`."""
    params: dict[str, str | int] = {
        "screen_name": handle.lstrip("@"),
        "tweet_mode": "extended",
        "exclude_replies": "true",
        "count": 5,
    }
    if since_id:
        params["since_id"] = since_id

    async with httpx.AsyncClient() as client:
        response = await client.get(API_URL, params=params, headers=_HEADERS, timeout=20)
        response.raise_for_status()
        # Assume response.json() returns {"statuses": [...]} for v1.1; adapt as needed
        return response.json().get("statuses", [])


def ingest_handles(handles: list[str]) -> None:
    """Pull tweets and persist new posts."""
    with Session(engine) as session:
        for hnd in handles:
            feed = session.exec(Feed.select().where(Feed.handle == hnd)).first()
            if not feed:
                feed = Feed(handle=hnd)
                session.add(feed)
                session.commit()
                session.refresh(feed)

            tweets = []  # use sync for now
            import anyio

            tweets = anyio.run(fetch_latest, hnd, feed.last_post_id)  # noqa: WPS420
            for t in tweets:
                if session.exec(Post.select().where(Post.tweet_id == t["id_str"])).first():
                    continue
                post = Post(feed_id=feed.id, tweet_id=t["id_str"], text=t["full_text"])
                session.add(post)
                feed.last_post_id = t["id_str"]
            session.commit()
