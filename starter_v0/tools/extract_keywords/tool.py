from __future__ import annotations

import re
from collections import Counter
from typing import Any

# Basic stop words in English and Vietnamese to filter out noise
STOP_WORDS = {
    # English
    "a", "an", "the", "and", "or", "but", "if", "because", "as", "what",
    "which", "this", "that", "these", "those", "then", "just", "so", "than",
    "such", "both", "through", "about", "for", "is", "of", "while", "during",
    "to", "from", "in", "out", "on", "off", "again", "further", "then", "once",
    "here", "there", "when", "where", "why", "how", "all", "any", "both", "each",
    "few", "more", "most", "other", "some", "such", "no", "nor", "not", "only",
    "own", "same", "so", "than", "too", "very", "s", "t", "can", "will", "don",
    "should", "now", "are", "was", "were", "be", "been", "being", "have", "has",
    "had", "having", "do", "does", "did", "doing", "with", "at", "by", "into",
    # Vietnamese
    "và", "của", "là", "có", "được", "trong", "cho", "với", "các", "những",
    "đã", "đang", "sẽ", "đó", "này", "về", "như", "khi", "tại", "đến",
    "từ", "ra", "vào", "lại", "nhiều", "một", "hai", "ba", "người", "ngày",
}


def extract_keywords(text: str = "", top_k: int = 5) -> dict[str, Any]:
    """Extract top keywords and their frequency from a given text.
    
    Returns a dict with 'keywords', 'total_words', and 'unique_words'.
    Never raises exceptions; returns an error dict on invalid input.
    """
    if not isinstance(text, str):
        return {
            "error": "invalid_input",
            "message": f"Expected text to be str, got {type(text).__name__}",
            "keywords": [],
            "total_words": 0,
            "unique_words": 0,
        }

    # Handle string-formatted integers if model sends "5" instead of 5
    if isinstance(top_k, str) and top_k.isdigit():
        top_k = int(top_k)
    elif not isinstance(top_k, int) or top_k <= 0:
        return {
            "error": "invalid_top_k",
            "message": f"top_k must be a positive integer, got {top_k!r}",
            "keywords": [],
            "total_words": 0,
            "unique_words": 0,
        }

    stripped = text.strip()
    if not stripped:
        return {
            "tool": "extract_keywords",
            "keywords": [],
            "total_words": 0,
            "unique_words": 0,
        }

    # Extract alphanumeric words (supporting unicode/Vietnamese characters)
    words = re.findall(r"\b[a-zA-Z0-9_\u00C0-\u024F\u1EA0-\u1EF9]{2,}\b", stripped.lower())
    total_words = len(words)
    filtered = [w for w in words if w not in STOP_WORDS and not w.isdigit()]

    counts = Counter(filtered)
    # Sort by count desc, then alphabetically
    sorted_keywords = sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:top_k]

    return {
        "tool": "extract_keywords",
        "keywords": [{"keyword": k, "count": c} for k, c in sorted_keywords],
        "total_words": total_words,
        "unique_words": len(counts),
    }

