"""Pydantic models shared across the worker module."""
from typing import List
from pydantic import BaseModel, Field


class TextIn(BaseModel):
    """Input payload containing raw text to summarise."""

    text: str = Field(
        ...,
        min_length=1,
        description="Raw text to be summarised",
        example="Python is a popular programming language.",
    )


class SummaryOut(BaseModel):
    """Response containing the summary text."""

    summary: str


class Flashcard(BaseModel):
    """A simple flashcard data model."""

    question: str
    answer: str


class FlashcardDB(Flashcard):
    """Flashcard persisted in the database."""

    id: int = Field(..., example=1)


class FlashcardsOut(BaseModel):
    """Response containing a list of flashcards."""

    flashcards: List[Flashcard]


class FlashcardsDBOut(BaseModel):
    """List of flashcards including DB ids."""

    flashcards: List[FlashcardDB]


class ReviewIn(BaseModel):
    """Payload for reviewing a flashcard."""

    flashcard_id: int = Field(..., example=1)
    quality: int = Field(..., ge=0, le=5, example=5)


class ReviewOut(BaseModel):
    """Result of a review action."""

    id: int
    next_review: str
    interval: int
