"""Tests for text-stats."""

import io
import json

import pytest

from text_stats import analyse, count_stats, reading_time_minutes, top_words
from text_stats.cli import main


def test_count_stats_basic():
    stats = count_stats("hello world\nfrom C\n")
    assert stats == {
        "lines": 2,
        "words": 4,
        "chars": 19,
        "chars_no_spaces": 15,
    }


def test_count_stats_empty():
    assert count_stats("") == {
        "lines": 0,
        "words": 0,
        "chars": 0,
        "chars_no_spaces": 0,
    }


def test_count_stats_apostrophe_is_one_word():
    assert count_stats("don't stop")[ "words"] == 2
    assert count_stats("don't stop")["chars_no_spaces"] == 9


def test_top_words_case_insensitive():
    assert top_words("Hello hello HELLO world", 2) == [
        ("hello", 3),
        ("world", 1),
    ]


def test_top_words_tie_keeps_first_appearance():
    assert top_words("b a b a c", 3) == [("b", 2), ("a", 2), ("c", 1)]


def test_top_words_zero():
    assert top_words("hello world", 0) == []


def test_reading_time_default_wpm():
    assert reading_time_minutes(200) == 1.0
    assert reading_time_minutes(100) == 0.5
    assert reading_time_minutes(0) == 0.0
    assert reading_time_minutes(1) == 0.01  # rounded to 2 decimals: 0.005 -> 0.01


def test_reading_time_custom_wpm():
    assert reading_time_minutes(100, wpm=100) == 1.0


def test_analyse_combines_everything():
    result = analyse("cat dog cat\nbird cat", top_n=2)
    assert result["lines"] == 2
    assert result["words"] == 5
    assert result["top_words"] == [
        {"word": "cat", "count": 3},
        {"word": "dog", "count": 1},
    ]
    assert result["reading_time_minutes"] == 0.03  # 5 / 200 = 0.025 -> 0.03


def test_cli_report(capsys, monkeypatch):
    monkeypatch.setattr("sys.stdin", io.StringIO("hello world hello\n"))
    assert main([]) == 0
    out = capsys.readouterr().out
    assert "Lines:                1" in out
    assert "Words:                3" in out
    assert "hello" in out and "2" in out


def test_cli_json(capsys, tmp_path):
    sample = tmp_path / "sample.txt"
    sample.write_text("one two three\n", encoding="utf-8")
    assert main(["--json", "--top", "1", str(sample)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["lines"] == 1
    assert result["words"] == 3
    assert result["top_words"] == [{"word": "one", "count": 1}]


def test_cli_rejects_bad_top(capsys):
    assert main(["--top", "-1"]) == 2
    assert "--top must be 0 or more" in capsys.readouterr().err


def test_cli_rejects_bad_wpm(capsys):
    assert main(["--wpm", "0"]) == 2
    assert "--wpm must be greater than 0" in capsys.readouterr().err
