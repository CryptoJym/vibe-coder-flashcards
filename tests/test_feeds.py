import asyncio
import pytest
from apps.worker import feeds

SAMPLE_RSS = """
<rss><channel>
  <item><title>First post</title><link>https://example.com/1</link></item>
  <item><title>Second post</title><link>https://example.com/2</link></item>
</channel></rss>
"""


def test_parse_rss():
    posts = feeds.parse_rss(SAMPLE_RSS)
    assert posts == [
        {"title": "First post", "link": "https://example.com/1"},
        {"title": "Second post", "link": "https://example.com/2"},
    ]


def test_ingest_twitter(monkeypatch):
    async def fake_fetch(url: str) -> str:
        return SAMPLE_RSS

    monkeypatch.setattr(feeds, "fetch_rss", fake_fetch)
    posts = asyncio.run(feeds.ingest_twitter("user"))
    assert len(posts) == 2
    assert posts[0]["title"] == "First post"

