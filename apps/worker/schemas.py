"""Pydantic models shared across the worker module."""
from typing import List
from pydantic import BaseModel, Field


class TextIn(BaseModel):
    """Input payload containing raw text to summarise."""

    text: str = Field(..., min_length=1, description="Raw text to be summarised")


class SummaryOut(BaseModel):
    """Response containing the summary text."""

    summary: str


class Flashcard(BaseModel):
    """A simple flashcard data model."""

    question: str
    answer: str


class FlashcardsOut(BaseModel):
    """Response containing a list of flashcards."""

    flashcards: List[Flashcard]
