# Day 068 — Practice Tasks: Command-Line Arguments using argparse

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Greeter CLI

**Problem statement:** Create a parser with a positional `name` and an optional `--times` (int, default 1). Parse `["Asha", "--times", "3"]` and print the greeting that many times.

**Input requirements:** No user input required.

**Expected behavior:** Three greetings.

**Expected output:**

```text
Hello, Asha!
Hello, Asha!
Hello, Asha!
```

## Task 2 — Medium: Port scanner arguments

**Problem statement:** Create a parser for `scan.py` with positional `host`, `--ports` (one or more ints, default `[22, 80, 443]`), `--timeout` (float, default 1.0) and `-v/--verbose` flag. Parse two different command lines and print the resulting namespaces as dicts.

**Input requirements:** No user input required.

**Expected behavior:** Two dicts with converted types.

**Expected output:**

```text
{'host': '10.0.0.5', 'ports': [22, 80, 443], 'timeout': 1.0, 'verbose': False}
{'host': 'db.internal', 'ports': [5432, 6379], 'timeout': 0.5, 'verbose': True}
```

## Task 3 — Practical Challenge: log-tool with sub-commands

**Problem statement:** Build `logtool` with sub-commands `count` (positional file, `--level` choice INFO/WARNING/ERROR), `tail` (file, `-n` int default 5) and `search` (file, pattern, `--ignore-case` flag). Each handler should actually operate on `../../datasets/app.log`. Run all three sub-commands.

**Input requirements:** No user input required.

**Expected behavior:** Count of a level, last N lines, and matching lines.

**Expected output:**

```text
$ logtool count ...
ERROR: 13 lines
$ logtool tail ...
2026-11-20 10:28:39 INFO [10.0.0.7] Health check passed
2026-11-20 10:29:46 INFO [10.0.1.12] Cache refreshed in 1390ms
2026-11-20 10:29:53 ERROR [192.168.1.20] Database connection timeout after 624ms
$ logtool search ...
2026-11-20 10:00:00 ERROR [10.0.0.5] Database connection timeout after 2418ms
2026-11-20 10:05:10 ERROR [10.0.1.12] Database connection timeout after 844ms
2026-11-20 10:06:24 ERROR [10.0.0.5] Database connection timeout after 2569ms
2026-11-20 10:06:31 ERROR [10.0.0.7] Database connection timeout after 1314ms
2026-11-20 10:10:20 ERROR [10.0.0.5] Database connection timeout after 1502ms
2026-11-20 10:24:36 ERROR [10.0.0.5] Database connection timeout after 1644ms
2026-11-20 10:28:32 ERROR [10.0.0.5] Database connection timeout after 724ms
2026-11-20 10:29:53 ERROR [192.168.1.20] Database connection timeout after 624ms
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
