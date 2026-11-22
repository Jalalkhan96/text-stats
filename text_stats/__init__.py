"""text-stats package: line/word/character counts, top words, reading time."""

from .stats import (
    DEFAULT_WPM,
    analyse,
    count_stats,
    reading_time_minutes,
    top_words,
)

__version__ = "0.1.0"

__all__ = [
    "DEFAULT_WPM",
    "analyse",
    "count_stats",
    "reading_time_minutes",
    "top_words",
]
