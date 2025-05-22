import pytest
from sqlmodel import Session, select, create_engine

from apps import worker
from apps.worker.ingestors import twitter
from apps.worker import init_db
from packages.core.models import Post, Flashcard
from apps.worker.main import SummaryOut, FlashcardsOut, Flashcard as CardSchema


@pytest.fixture(autouse=True)
def setup_db(monkeypatch):
    test_engine = create_engine("sqlite:///:memory:")
    monkeypatch.setattr(twitter, "engine", test_engine)
    monkeypatch.setattr(worker, "engine", test_engine)
    init_db()
    yield


@pytest.fixture(autouse=True)
def mock_network(monkeypatch):
    class Resp:
        def __init__(self, data):
            self._data = data
            self.status_code = 200

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    async def fake_get(self, url, params=None, headers=None, timeout=20):
        if "users/by/username" in url:
            return Resp({"data": {"id": "1"}})
        return Resp({"data": [{"id": "10", "text": "hello world"}]})

    monkeypatch.setattr(twitter.httpx.AsyncClient, "get", fake_get, raising=False)
    
    async def fake_summarise(payload):
        return SummaryOut(summary=payload.text)

    async def fake_flashcards(payload):
        return FlashcardsOut(flashcards=[CardSchema(question="q", answer="a")])

    monkeypatch.setattr(twitter, "summarise", fake_summarise)
    monkeypatch.setattr(twitter, "generate_flashcards", fake_flashcards)
    yield


def test_ingest_handles():
    twitter.ingest_handles(["testuser"])

    with Session(twitter.engine) as ses:
        posts = ses.exec(select(Post)).all()
        cards = ses.exec(select(Flashcard)).all()

    assert len(posts) == 1
    assert len(cards) == 1
