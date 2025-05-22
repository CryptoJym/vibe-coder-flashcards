"""Utility functions for ingesting social feeds via RSS."""

from __future__ import annotations

import xml.etree.ElementTree as ET
from typing import List, Dict

import httpx


async def fetch_rss(url: str) -> str:
    """Fetch raw RSS feed text from the given URL."""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


def parse_rss(xml_text: str) -> List[Dict[str, str]]:
    """Parse RSS XML into a list of posts with title and link."""
    root = ET.fromstring(xml_text)
    posts: List[Dict[str, str]] = []
    for item in root.findall(".//item"):
        title = item.findtext("title")
        link = item.findtext("link")
        if title and link:
            posts.append({"title": title, "link": link})
    return posts


async def ingest_twitter(handle: str) -> List[Dict[str, str]]:
    """Return recent tweets for the handle via nitter RSS."""
    url = f"https://nitter.net/{handle}/rss"
    xml = await fetch_rss(url)
    return parse_rss(xml)


async def ingest_youtube(channel_id: str) -> List[Dict[str, str]]:
    """Return recent YouTube uploads for the channel via RSS."""
    url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    xml = await fetch_rss(url)
    return parse_rss(xml)

