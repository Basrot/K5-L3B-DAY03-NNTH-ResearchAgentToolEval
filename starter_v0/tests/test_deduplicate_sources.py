from __future__ import annotations

from tools import TOOL_FUNCTIONS


deduplicate_sources = TOOL_FUNCTIONS["deduplicate_sources"]


def test_deduplicate_sources_removes_fragments_and_trailing_slashes() -> None:
    result = deduplicate_sources(urls=[
        "https://Example.com/paper/#abstract",
        "https://example.com/paper",
        "https://example.com/paper?download=1",
    ])

    assert result["urls"] == [
        "https://Example.com/paper/#abstract",
        "https://example.com/paper?download=1",
    ]
    assert result["duplicate_count"] == 1
    assert result["invalid_count"] == 0


def test_deduplicate_sources_rejects_non_list_input() -> None:
    result = deduplicate_sources(urls="https://example.com")

    assert result["error"] == "invalid_input"
    assert "urls" not in result


def test_deduplicate_sources_skips_invalid_urls_and_items() -> None:
    result = deduplicate_sources(urls=[
        "https://example.com/article",
        "ftp://example.com/file",
        None,
        "not a URL",
    ])

    assert result["urls"] == ["https://example.com/article"]
    assert result["duplicate_count"] == 0
    assert result["invalid_count"] == 3
