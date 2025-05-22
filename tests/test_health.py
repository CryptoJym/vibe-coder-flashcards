import httpx
import os
import anyio

os.environ["DATABASE_URL"] = "sqlite://"
from apps.worker.main import app


def test_health_check():
    async def run() -> None:
        async with httpx.AsyncClient(transport=httpx.ASGITransport(app=app), base_url="http://test") as client:
            response = await client.get("/health")
            assert response.status_code == 200
            assert response.json() == {"status": "ok"}

    anyio.run(run)
