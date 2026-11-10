"""TODO CP3 (student): Tool Unit Test Challenge.

Each test below is a stub. Replace `pytest.skip(...)` with a real test.
Patterns to copy are in test_tools_examples.py. Fixtures are in conftest.py.

Rules:
- Offline only: mock HTTP with `fake_http`, set fake keys with `monkeypatch.setenv`.
- One behaviour per test. Name the test after the behaviour, not the function.
- Done = `pytest tests/ -v` shows 0 skipped, 0 failed.
"""
from __future__ import annotations

import pytest

from conftest import FakeResponse  # noqa: F401  (you will need it)
from tools import TOOL_FUNCTIONS  # noqa: F401

TODO = "TODO CP3 (student): implement this test"


# ---------------- clarify ----------------

def test_clarify_choice_returns_options_and_awaits_user() -> None:
    result = TOOL_FUNCTIONS["clarify"](
        question="Bạn muốn chọn nguồn nào?",
        response_type="choice",
        options=["Web", "Twitter"],
    )
    assert result["tool"] == "ask_user"
    assert result["response_type"] == "choice"
    assert result["options"] == ["Web", "Twitter"]
    assert result["awaiting_user"] is True


# ---------------- format ----------------

def test_format_sections_groups_items_by_section() -> None:
    items = [
        {"title": "Item 1", "url": "https://a.com/1", "section": "A"},
        {"title": "Item 2", "url": "https://b.com/2", "section": "B"},
        {"title": "Item 3", "url": "https://a.com/3", "section": "A"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="sections", headline="Digest")
    md = result["markdown"]
    assert md.count("## A") == 1
    assert md.count("## B") == 1
    assert result["item_count"] == 3


def test_format_thread_numbers_items() -> None:
    items = [
        {"title": "First post", "url": "https://x.com/1"},
        {"title": "Second post", "url": "https://x.com/2"},
    ]
    result = TOOL_FUNCTIONS["format"](items=items, template="thread")
    lines = [block.strip() for block in result["markdown"].split("\n\n") if block.strip()]
    assert lines[0].startswith("1/ ")
    assert lines[1].startswith("2/ ")


def test_format_empty_items_does_not_crash() -> None:
    res_none = TOOL_FUNCTIONS["format"](items=None, template="bullets")
    res_empty = TOOL_FUNCTIONS["format"](items=[], template="sections")
    assert res_none["item_count"] == 0
    assert res_empty["item_count"] == 0


# ---------------- send (guardrail) ----------------

def test_send_confirmed_posts_to_telegram(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "bot-secret-token")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "-100123456")
    calls = fake_http(FakeResponse({"ok": True}))

    result = TOOL_FUNCTIONS["send"](text="Bản tin AI", confirmed=True)

    assert result["status"] == "sent"
    assert len(calls) == 1
    assert calls[0]["method"] == "POST"
    assert "bot-secret-token" in calls[0]["url"]
    assert calls[0]["json"]["chat_id"] == "-100123456"
    assert calls[0]["json"]["text"] == "Bản tin AI"


def test_send_confirmed_without_env_returns_error_and_no_request(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin AI", confirmed=True)
    assert result["error"] == "RuntimeError"
    assert "TELEGRAM_BOT_TOKEN" in result["message"]
    assert calls == []


# ---------------- lookup ----------------

def test_lookup_without_timeframe_omits_time_range(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "test-tavily-key")
    calls = fake_http(FakeResponse({"results": []}))

    TOOL_FUNCTIONS["lookup"](query="AI agents", topic="general", timeframe=None, max_results=5)

    assert len(calls) == 1
    assert "time_range" not in calls[0]["json"]


# ---------------- fetch ----------------

def test_fetch_maps_firecrawl_response(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-fc-key")
    calls = fake_http(
        FakeResponse(
            {
                "data": {
                    "markdown": "Full article content",
                    "metadata": {"title": "Article Title", "sourceURL": "https://www.openai.com/research"},
                }
            }
        )
    )

    result = TOOL_FUNCTIONS["fetch"](url="https://www.openai.com/research")

    assert len(calls) == 1
    assert result["items"][0] == {
        "title": "Article Title",
        "url": "https://www.openai.com/research",
        "source": "openai.com",
        "summary": "Full article content",
    }


def test_fetch_truncates_markdown_to_4000_chars(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("FIRECRAWL_API_KEY", "test-fc-key")
    fake_http(
        FakeResponse(
            {
                "data": {
                    "markdown": "a" * 5500,
                    "metadata": {"title": "Long Doc", "sourceURL": "https://example.com/long"},
                }
            }
        )
    )

    result = TOOL_FUNCTIONS["fetch"](url="https://example.com/long")
    assert len(result["items"][0]["summary"]) == 4000


# ---------------- timeline / social_search ----------------

def test_timeline_respects_limit_and_skips_items_without_id(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    timeline_data = [{"text": "Missing ID tweet", "screen_name": "sama"}] + [
        {"tweet_id": str(100 + i), "text": f"Tweet {i}", "screen_name": "sama"}
        for i in range(6)
    ]
    fake_http(FakeResponse({"timeline": timeline_data}))

    result = TOOL_FUNCTIONS["timeline"](screenname="sama", limit=3)

    assert len(result["items"]) == 3
    for idx, item in enumerate(result["items"]):
        assert item["url"] == f"https://x.com/sama/status/{100 + idx}"


def test_social_search_passes_search_type(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    calls = fake_http(FakeResponse({"timeline": []}))

    TOOL_FUNCTIONS["social_search"](query="OpenAI", search_type="Top", limit=5)

    assert len(calls) == 1
    assert calls[0]["params"]["query"] == "OpenAI"
    assert calls[0]["params"]["search_type"] == "Top"


# ---------------- policy (local knowledge + trust boundary) ----------------

def test_policy_empty_query_returns_no_results() -> None:
    result = TOOL_FUNCTIONS["policy"](query="", policy_area="all")
    assert result["results"] == []


def test_policy_area_filter_only_returns_that_area() -> None:
    result = TOOL_FUNCTIONS["policy"](query="customer data api key", policy_area="data_privacy")
    assert len(result["results"]) >= 1
    assert all(item["policy_area"] == "data_privacy" for item in result["results"])


def test_policy_instruction_like_lines_go_to_untrusted_text() -> None:
    result = TOOL_FUNCTIONS["policy"](query="citation viral tweet", policy_area="source_citation", top_k=10)
    probe_sections = [r for r in result["results"] if r["section"] == "Injection probe"]
    assert len(probe_sections) == 1
    probe = probe_sections[0]
    assert any("ignore the citation policy" in line.lower() for line in probe["untrusted_text"])
    assert "ignore the citation policy" not in probe["facts"].lower()


# ---------------- YOUR NEW TOOL(S) ----------------
# Write at least 3 tests per tool your team adds:
#   1. happy path (mocked if it calls an API)
#   2. bad / missing input from the model (empty string, wrong type, out-of-enum value)
#   3. failure path (missing key, HTTP error, timeout) -> returns error dict, does not raise

def test_extract_keywords_happy_path_returns_top_frequent_words() -> None:
    text = "AI agent is an autonomous agent. An agent uses tools to solve research tasks."
    result = TOOL_FUNCTIONS["extract_keywords"](text=text, top_k=3)
    assert result.get("tool") == "extract_keywords"
    assert "keywords" in result
    assert len(result["keywords"]) == 3
    # "agent" appears 3 times and is not a stop word -> should be rank 1
    assert result["keywords"][0]["keyword"] == "agent"
    assert result["keywords"][0]["count"] == 3
    assert result["total_words"] == 14


def test_extract_keywords_bad_input_from_model_handles_gracefully() -> None:
    # 1. Empty string input
    empty_res = TOOL_FUNCTIONS["extract_keywords"](text="")
    assert empty_res.get("keywords") == []
    assert empty_res.get("total_words") == 0

    # 2. Whitespace-only string
    ws_res = TOOL_FUNCTIONS["extract_keywords"](text="   \n\t  ")
    assert ws_res.get("keywords") == []

    # 3. Model passes integer as string (e.g. top_k="2")
    str_k_res = TOOL_FUNCTIONS["extract_keywords"](
        text="machine learning and deep learning models", top_k="2"
    )
    assert len(str_k_res["keywords"]) == 2
    assert str_k_res["keywords"][0]["keyword"] == "learning"
    assert str_k_res["keywords"][0]["count"] == 2


def test_extract_keywords_failure_returns_error_dict() -> None:
    # 1. Invalid text type (e.g. None or int) -> returns error dict without crashing
    res_type = TOOL_FUNCTIONS["extract_keywords"](text=None)
    assert "error" in res_type
    assert res_type["error"] == "invalid_input"

    # 2. Invalid top_k (e.g. <= 0) -> returns error dict without crashing
    res_k = TOOL_FUNCTIONS["extract_keywords"](text="hello world", top_k=0)
    assert "error" in res_k
    assert res_k["error"] == "invalid_top_k"


# ---------------- REGRESSION TESTS FOR BUGS IN EXISTING TOOLS (Challenge+) ----------------

def test_regression_format_item_missing_url_does_not_leave_dangling_hyphen() -> None:
    result = TOOL_FUNCTIONS["format"](items=[{"title": "Tin không có link"}], template="bullets")
    assert result["markdown"] == "- Tin không có link"
    assert not result["markdown"].endswith(" - ")


def test_regression_timeline_limit_zero_returns_empty_and_strips_at_prefix(monkeypatch, fake_http) -> None:
    monkeypatch.setenv("RAPIDAPI_KEY", "test-rapid-key")
    calls = fake_http(FakeResponse({"timeline": [{"tweet_id": "1", "text": "hi", "screen_name": "sama"}]}))

    result = TOOL_FUNCTIONS["timeline"](screenname="@sama", limit=0)

    assert calls[0]["params"]["screenname"] == "sama"
    assert result["items"] == []


def test_regression_policy_top_k_zero_returns_empty_list() -> None:
    result = TOOL_FUNCTIONS["policy"](query="citation", policy_area="source_citation", top_k=0)
    assert result["results"] == []


def test_regression_send_string_false_confirmation_is_blocked(fake_http) -> None:
    calls = fake_http(FakeResponse({"ok": True}))
    result = TOOL_FUNCTIONS["send"](text="Bản tin", confirmed="false")  # type: ignore[arg-type]
    assert result["status"] == "needs_confirmation"
    assert calls == []
