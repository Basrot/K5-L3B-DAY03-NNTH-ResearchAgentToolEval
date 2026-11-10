from __future__ import annotations

from tools import TOOL_FUNCTIONS

calculate_text_stats = TOOL_FUNCTIONS["text_stats"]


def test_text_stats_happy_path_calculates_metrics() -> None:
    text = (
        "Artificial intelligence is transforming scientific discovery. "
        "Researchers can now analyze vast literature in seconds.\n\n"
        "This is the second paragraph with more insights."
    )
    result = calculate_text_stats(text=text, wpm=200)

    assert result["tool"] == "text_stats"
    assert "error" not in result
    assert result["word_count"] == 22
    assert result["sentence_count"] == 3
    assert result["paragraph_count"] == 2
    assert result["char_count"] == len(text)
    assert result["reading_time_minutes"] == round(22 / 200, 1)


def test_text_stats_bad_input_handles_gracefully() -> None:
    # 1. Empty string -> returns 0 counts without error
    empty_res = calculate_text_stats(text="")
    assert empty_res["word_count"] == 0
    assert empty_res["char_count"] == 0
    assert empty_res["sentence_count"] == 0
    assert empty_res["paragraph_count"] == 0
    assert empty_res["reading_time_minutes"] == 0.0

    # 2. Whitespace-only string
    ws_res = calculate_text_stats(text="   \n\t  ")
    assert ws_res["word_count"] == 0

    # 3. Model sends wpm as string digit (e.g. wpm="100")
    str_wpm_res = calculate_text_stats(text="One two three four five.", wpm="100")
    assert str_wpm_res["word_count"] == 5
    assert str_wpm_res["reading_time_minutes"] == round(5 / 100, 1)


def test_text_stats_failure_returns_error_dict() -> None:
    # 1. Invalid text type (e.g. None or int) -> returns error dict, does not raise
    res_none = calculate_text_stats(text=None)
    assert "error" in res_none
    assert res_none["error"] == "invalid_input"

    # 2. Invalid wpm (e.g. <= 0) -> returns error dict, does not raise
    res_wpm = calculate_text_stats(text="Hello world", wpm=0)
    assert "error" in res_wpm
    assert res_wpm["error"] == "invalid_wpm"
