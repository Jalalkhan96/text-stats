"""Command-line interface for text-stats.

Usage:
    text-stats [FILE] [--top N] [--wpm N] [--json]
    cat file.txt | text-stats

With no FILE argument, text is read from standard input.
"""

import argparse
import json
import sys

from .stats import DEFAULT_WPM, analyse


def build_parser():
    parser = argparse.ArgumentParser(
        prog="text-stats",
        description="Text statistics: lines, words, characters, "
        "most frequent words and estimated reading time.",
    )
    parser.add_argument(
        "file",
        nargs="?",
        type=argparse.FileType("r", encoding="utf-8"),
        default=sys.stdin,
        help="text file to analyse (default: standard input)",
    )
    parser.add_argument(
        "--top",
        type=int,
        default=10,
        metavar="N",
        help="show the N most frequent words (default: 10)",
    )
    parser.add_argument(
        "--wpm",
        type=int,
        default=DEFAULT_WPM,
        metavar="N",
        help="words per minute for the reading-time estimate (default: 200)",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="print the result as JSON instead of a human-readable report",
    )
    return parser


def _print_report(result):
    print(f"Lines:                {result['lines']}")
    print(f"Words:                {result['words']}")
    print(f"Characters:           {result['chars']}")
    print(f"Characters (no spaces): {result['chars_no_spaces']}")
    print(f"Reading time:         {result['reading_time_minutes']} min")
    print("Top words:")
    if not result["top_words"]:
        print("  (none)")
    for entry in result["top_words"]:
        print(f"  {entry['word']:<20} {entry['count']}")


def main(argv=None):
    args = build_parser().parse_args(argv)
    if args.top < 0:
        print("error: --top must be 0 or more", file=sys.stderr)
        return 2
    if args.wpm <= 0:
        print("error: --wpm must be greater than 0", file=sys.stderr)
        return 2
    with args.file as source:
        text = source.read()
    result = analyse(text, top_n=args.top, wpm=args.wpm)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        _print_report(result)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
