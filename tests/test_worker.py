import json

from fastapi.testclient import TestClient

from apps.worker.main import app, client as openai_client
import types
import pytest


@pytest.fixture(autouse=True)
def mock_openai(monkeypatch):
    """Patch OpenAI chat completion to avoid real API calls."""

    async def fake_create(*args, **kwargs):
        dummy = types.SimpleNamespace()
        dummy.choices = [
            types.SimpleNamespace(
                message=types.SimpleNamespace(content='[{"question":"Q","answer":"A"}]')
            )
        ]
        return dummy

    monkeypatch.setattr(openai_client.chat.completions, "create", fake_create)
    yield


test_client = TestClient(app, raise_server_exceptions=False)


def test_summarise_route():
    resp = test_client.post("/summarise", json={"text": "OpenAI builds AI systems."})
    assert resp.status_code == 200
    # summarise returns dummy summary string
    assert resp.json()["summary"] == '[{"question":"Q","answer":"A"}]'


def test_flashcards_route_schema():
    """Ensure response model keys are correct when mocked."""
    payload = {"text": "Python is a popular programming language."}
    resp = test_client.post("/flashcards", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert "flashcards" in data
    # mock returns list with dummy-response; structure check only
    for card in data["flashcards"]:
        assert set(card) == {"question", "answer"}
