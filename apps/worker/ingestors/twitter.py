"""Twitter/X ingestion using the v2 API."""
from __future__ import annotations

import os

import anyio
import httpx
from sqlmodel import Session, select

from packages.core.models import Feed, Flashcard, Post
from apps.worker import engine
from apps.worker.main import generate_flashcards, summarise, TextIn

BEARER_TOKEN = os.environ.get("TWITTER_BEARER_TOKEN", "")

HEADERS = {"Authorization": f"Bearer {BEARER_TOKEN}"}
USER_URL = "https://api.twitter.com/2/users/by/username/{username}"
TWEETS_URL = "https://api.twitter.com/2/users/{user_id}/tweets"


async def get_user_id(handle: str) -> str:
    """Return Twitter user id for handle."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            USER_URL.format(username=handle.lstrip("@")),
            headers=HEADERS,
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json()["data"]["id"]


async def fetch_latest(handle: str, since_id: str | None = None) -> list[dict]:
    """Return latest tweets for handle since ``since_id``."""
    user_id = await get_user_id(handle)
    params: dict[str, str] = {
        "max_results": "5",
        "exclude": "replies",
        "tweet.fields": "id,text",
    }
    if since_id:
        params["since_id"] = since_id
    async with httpx.AsyncClient() as client:
        resp = await client.get(
            TWEETS_URL.format(user_id=user_id),
            params=params,
            headers=HEADERS,
            timeout=20,
        )
        resp.raise_for_status()
        return resp.json().get("data", [])


def _ensure_feed(session: Session, handle: str) -> Feed:
    feed = session.exec(select(Feed).where(Feed.handle == handle)).first()
    if not feed:
        feed = Feed(handle=handle)
        session.add(feed)
        session.commit()
        session.refresh(feed)
    return feed


def ingest_handles(handles: list[str]) -> None:
    """Pull tweets, summarise, and persist new posts."""

    with Session(engine) as session:
        for handle in handles:
            feed = _ensure_feed(session, handle)
            tweets = anyio.run(fetch_latest, handle, feed.last_post_id)  # noqa: WPS420
            for tweet in tweets:
                if session.exec(select(Post).where(Post.tweet_id == str(tweet["id"]))).first():
                    continue
                post = Post(feed_id=feed.id, tweet_id=str(tweet["id"]), text=tweet["text"])
                session.add(post)
                session.commit()
                session.refresh(post)

                summary = anyio.run(summarise, TextIn(text=post.text))  # noqa: WPS420
                cards = anyio.run(generate_flashcards, TextIn(text=summary.summary))  # noqa: WPS420
                for c in cards.flashcards:
                    card = Flashcard(post_id=post.id, owner_id=1, question=c.question, answer=c.answer)
                    session.add(card)
                feed.last_post_id = str(tweet["id"])
            session.commit()


async def scheduler(handles: list[str]) -> None:
    """Run ingestion periodically every 15 minutes."""
    while True:
        ingest_handles(handles)
        await anyio.sleep(60 * 15)


def main() -> None:
    """CLI entrypoint for running the ingestor."""
    handles_env = os.environ.get(
        "FEED_HANDLES",
        "dr_cintas,GoogleLabs,kregenrek,GeminiApp,OpenAI,AnthropicAI,GoogleAI",
    )
    handles = [h.strip() for h in handles_env.split(",") if h.strip()]
    anyio.run(scheduler, handles)


if __name__ == "__main__":  # pragma: no cover - manual run
    main()
