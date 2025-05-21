from fastapi.testclient import TestClient

from apps.worker.main import app


def test_health_check():
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
