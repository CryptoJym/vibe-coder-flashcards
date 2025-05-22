"""Pipeline: convert new posts to flashcards via OpenAI."""
from __future__ import annotations

import json
from loguru import logger
from openai import AsyncOpenAI
from sqlmodel import Session, select

from packages.core.models import Post, Flashcard
from apps.worker import engine

client = AsyncOpenAI()


async def posts_to_flashcards(batch_size: int = 10) -> int:  # noqa: D401
    """Generate flashcards for latest posts without cards.

    Returns number of cards created.
    """
    created = 0
    with Session(engine) as ses:
        posts = ses.exec(
            select(Post).where(~Post.id.in_(select(Flashcard.post_id))).limit(batch_size)
        ).all()
        for p in posts:
            prompt = (
                "Convert the following text to <=5 study flashcards in JSON array of objects "
                'with "question" & "answer" keys only. No extra keys. Text:\n' + p.text
            )
            chat = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=256,
                response_format={"type": "json_object"},
            )
            cards_data = chat.choices[0].message.content
            for raw in json.loads(cards_data):
                card = Flashcard(post_id=p.id, owner_id=1, question=raw["question"], answer=raw["answer"])
                ses.add(card)
                created += 1
        ses.commit()
    logger.info(f"Created {created} flashcards")
    return created
