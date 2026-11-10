from __future__ import annotations

import re
from typing import Any


def calculate_text_stats(text: str = "", wpm: int = 200) -> dict[str, Any]:
    """Calculate descriptive statistics and estimated reading time for a text.

    Returns word_count, char_count, sentence_count, paragraph_count, and reading_time_minutes.
    Never raises exceptions; returns an error dict on invalid inputs.
    """
    if not isinstance(text, str):
        return {
            "tool": "text_stats",
            "error": "invalid_input",
            "message": f"Expected text to be str, got {type(text).__name__}",
            "word_count": 0,
            "char_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "reading_time_minutes": 0.0,
        }

    # Handle string-formatted integer for wpm if sent by LLM (e.g. "200")
    if isinstance(wpm, str) and wpm.isdigit():
        wpm = int(wpm)
    elif not isinstance(wpm, int) or wpm <= 0:
        return {
            "tool": "text_stats",
            "error": "invalid_wpm",
            "message": f"wpm must be a positive integer, got {wpm!r}",
            "word_count": 0,
            "char_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "reading_time_minutes": 0.0,
        }

    stripped = text.strip()
    if not stripped:
        return {
            "tool": "text_stats",
            "word_count": 0,
            "char_count": 0,
            "sentence_count": 0,
            "paragraph_count": 0,
            "reading_time_minutes": 0.0,
        }

    words = re.findall(r"\b\w+\b", stripped)
    word_count = len(words)
    char_count = len(stripped)

    # Count sentences based on punctuation (. ! ?)
    sentences = re.split(r"[.!?]+", stripped)
    sentences = [s.strip() for s in sentences if s.strip()]
    sentence_count = max(len(sentences), 1 if word_count > 0 else 0)

    # Count paragraphs based on double newlines
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", stripped) if p.strip()]
    paragraph_count = max(len(paragraphs), 1 if word_count > 0 else 0)

    reading_time = round(word_count / wpm, 1)

    return {
        "tool": "text_stats",
        "word_count": word_count,
        "char_count": char_count,
        "sentence_count": sentence_count,
        "paragraph_count": paragraph_count,
        "reading_time_minutes": reading_time,
    }
