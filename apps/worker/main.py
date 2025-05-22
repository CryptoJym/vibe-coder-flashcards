"""FastAPI worker entrypoint for Vibe Coder Flashcards.

Provides a simple health-check route for now.
"""
from fastapi import FastAPI
from openai import AsyncOpenAI
import os
from .schemas import TextIn, SummaryOut, Flashcard, FlashcardsOut

app = FastAPI(title="Vibe Coder Flashcards Worker")

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY", "test"))


@app.get("/")
async def health_check() -> dict[str, str]:
    """Health-check endpoint used by tests & uptime monitors."""
    return {"status": "ok"}


@app.post("/summarise", response_model=SummaryOut)
async def summarise(payload: TextIn) -> SummaryOut:
    """Return a concise summary of the provided text."""
    chat = await client.chat.completions.create(
        model="gpt-3.5-turbo",  # small cheap model
        messages=[{"role": "user", "content": f"Summarise:\n{payload.text}"}],
        max_tokens=128,
    )
    return SummaryOut(summary=chat.choices[0].message.content.strip())


@app.post("/flashcards", response_model=FlashcardsOut)
async def generate_flashcards(payload: TextIn) -> FlashcardsOut:
    """Generate Q/A flashcards from input text."""
    prompt = (
        "Convert the following text to <=5 study flashcards in JSON array of objects "
        "with \"question\" & \"answer\" keys only. No extra keys. Text:\n" + payload.text
    )
    chat = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=256,
        response_format={"type": "json_object"},
    )
    cards_data = chat.choices[0].message.content
    # simple parse – assumes correct JSON
    import json

    decoded = json.loads(cards_data)
    cards = [Flashcard(**c) for c in decoded]
    return FlashcardsOut(flashcards=cards)
