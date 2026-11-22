# text-stats

Text statistics from the command line: line, word and character counts,
the most frequent words, and an estimated reading time. Reads a file or
standard input. Zero dependencies, Python 3.9+.

## Install

```bash
pip install .
```

This installs the `text-stats` command.

## Usage

```bash
text-stats README.md
cat essay.txt | text-stats
text-stats --top 5 --wpm 250 notes.txt
text-stats --json report.txt
```

Example output:

```text
Lines:                42
Words:                318
Characters:           2140
Characters (no spaces): 1822
Reading time:         1.59 min
Top words:
  the                  21
  and                  14
  python               9
```

## Options

| Option | Description |
| --- | --- |
| `FILE` | Text file to analyse (default: standard input) |
| `--top N` | Show the N most frequent words (default: 10) |
| `--wpm N` | Words per minute for the reading-time estimate (default: 200) |
| `--json` | Print the result as JSON |

## Library use

```python
from text_stats import analyse

result = analyse("hello world hello\n")
# {'lines': 1, 'words': 3, 'chars': 18, 'chars_no_spaces': 15,
#  'top_words': [{'word': 'hello', 'count': 2}, {'word': 'world', 'count': 1}],
#  'reading_time_minutes': 0.01}
```

## Tests

```bash
python -m pytest
```

## License

MIT — see [LICENSE](LICENSE).
