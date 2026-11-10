from __future__ import annotations

from typing import Any
from urllib.parse import urlsplit, urlunsplit


def _normalized_url(url: str) -> str | None:
    value = url.strip()
    try:
        parsed = urlsplit(value)
        if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
            return None
        return urlunsplit((
            parsed.scheme.lower(),
            parsed.netloc.lower(),
            parsed.path.rstrip("/") or "/",
            parsed.query,
            "",
        ))
    except ValueError:
        return None


def deduplicate_sources(urls: list[str] | None = None) -> dict[str, Any]:
    if not isinstance(urls, list):
        return {
            "tool": "deduplicate_sources",
            "error": "invalid_input",
            "message": "urls must be a list of HTTP(S) URL strings",
        }

    unique_urls: list[str] = []
    seen: set[str] = set()
    duplicate_count = 0
    invalid_count = 0

    for url in urls:
        if not isinstance(url, str):
            invalid_count += 1
            continue
        normalized = _normalized_url(url)
        if normalized is None:
            invalid_count += 1
            continue
        if normalized in seen:
            duplicate_count += 1
            continue
        seen.add(normalized)
        unique_urls.append(url.strip())

    return {
        "tool": "deduplicate_sources",
        "urls": unique_urls,
        "duplicate_count": duplicate_count,
        "invalid_count": invalid_count,
    }
