"""Text statistics: line/word/character counts, word frequencies, reading time."""

import re
from collections import Counter

__version__ = "0.1.0"

# A word is a run of letters, digits or apostrophes (so "don't" is one word).
_WORD_RE = re.compile(r"[A-Za-z0-9']+")

DEFAULT_WPM = 200


def count_stats(text):
    """Return line, word and character counts for ``text``.

    ``lines`` counts newline-separated lines (an empty string has 0 lines),
    ``chars`` counts every character including whitespace, and
    ``chars_no_spaces`` counts every non-whitespace character.
    """
    words = _WORD_RE.findall(text)
    return {
        "lines": len(text.splitlines()),
        "words": len(words),
        "chars": len(text),
        "chars_no_spaces": len(re.sub(r"\s", "", text)),
    }


def top_words(text, n=10):
    """Return the ``n`` most frequent words as a list of ``(word, count)``.

    Matching is case-insensitive; ties are broken by first appearance.
    """
    words = [word.lower() for word in _WORD_RE.findall(text)]
    return Counter(words).most_common(n)


def reading_time_minutes(word_count, wpm=DEFAULT_WPM):
    """Estimated reading time in minutes at ``wpm`` words per minute."""
    if word_count <= 0:
        return 0.0
    return round(word_count / wpm, 2)


def analyse(text, top_n=10, wpm=DEFAULT_WPM):
    """Full analysis of ``text``: counts, top words and reading time."""
    stats = count_stats(text)
    stats["top_words"] = [
        {"word": word, "count": count} for word, count in top_words(text, top_n)
    ]
    stats["reading_time_minutes"] = reading_time_minutes(stats["words"], wpm)
    return stats
