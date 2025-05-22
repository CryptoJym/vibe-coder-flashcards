import pytest
from sqlmodel import select

from packages.core.models import User, Feed, Post, Flashcard
from packages.db import async_session_maker, init_db


@pytest.mark.asyncio
async def test_model_crud_round_trip() -> None:
    await init_db()
    async with async_session_maker() as session:
        user = User(email="me@example.com")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        feed = Feed(handle="test")
        session.add(feed)
        await session.commit()
        await session.refresh(feed)

        post = Post(feed_id=feed.id, tweet_id="t1", text="hello")
        session.add(post)
        await session.commit()
        await session.refresh(post)

        card = Flashcard(owner_id=user.id, post_id=post.id, question="Q", answer="A")
        session.add(card)
        await session.commit()

        result = await session.exec(select(Flashcard).where(Flashcard.id == card.id))
        fetched = result.one()
        assert fetched.question == "Q"
        assert fetched.owner_id == user.id

