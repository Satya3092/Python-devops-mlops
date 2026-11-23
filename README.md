# Day 055 — File Processing Automation Project

[⬅ Day 054](../../05-files-exceptions/day-054/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 056 ➡](../../06-modules-oop/day-056/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 2–3 hours |

## 1. Learning Objectives

By the end of today you will be able to:

- Combine file handling, CSV/JSON and exceptions in one automation
- Process a directory of files robustly
- Build the project: **Log Folder Processor** (foundation of Project 3)

## 2. Topic Explanation

Time to build a real automation that you could run in production.

**Problem:** a folder (`logs/`) contains log files from several servers. Every morning someone opens them manually. Automate it:

1. Find every `*.log` file in the folder (ignore other files).
2. Parse each line: `date time LEVEL message key=value...`.
3. Skip and count corrupted lines instead of crashing.
4. Count INFO / WARNING / ERROR per server and overall.
5. Find the slowest requests (`ms=` field).
6. Write `report.json` (machine-readable) and `report.csv` (for spreadsheets).
7. Print a human-readable summary.

**Design:** small functions — `find_log_files`, `parse_line`, `analyse_file`, `write_reports`, `main` — and custom exceptions for unparsable lines.

`os.listdir(folder)` returns the file names in a folder; `os.path.join(folder, name)` builds paths that work on every OS. (Day 59 shows the more modern `pathlib`.)

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work. The sample `logs/` folder is included.

## 3. Syntax

```python
import os
for name in sorted(os.listdir("logs")):
    if name.endswith(".log"):
        path = os.path.join("logs", name)
        ...
```

| Part | Meaning |
|---|---|
| `os.listdir(folder)` | Names of entries in a folder. |
| `os.path.join(a, b)` | Joins path parts with the correct separator. |
| `endswith(".log")` | Filter by extension. |
| `json.dump / csv.writer` | Write machine-readable reports. |

## 4. Example 1 — Basic Example: Parsing one line with a custom exception

```python
class ParseError(Exception):
    """Raised when a log line does not match the expected format."""


LEVELS = {"INFO", "WARNING", "ERROR"}


def parse_line(line):
    """Return a dict for a log line or raise ParseError."""
    parts = line.split()
    if len(parts) < 4 or parts[2] not in LEVELS:
        raise ParseError(f"unexpected format: {line.strip()!r}")
    fields = {}
    message_words = []
    for word in parts[3:]:
        if "=" in word:
            key, value = word.split("=", 1)
            fields[key] = value
        else:
            message_words.append(word)
    return {
        "timestamp": f"{parts[0]} {parts[1]}",
        "level": parts[2],
        "message": " ".join(message_words),
        "fields": fields,
    }


print(parse_line("2026-11-20 10:00:09 ERROR Database timeout path=/api/orders ms=5000"))
try:
    parse_line("this line is corrupted")
except ParseError as error:
    print("ParseError:", error)
```

## 5. Example 2 — Practical Example: Project — Log Folder Processor

```python
import csv
import json
import os


class ParseError(Exception):
    """Raised when a log line does not match the expected format."""


LEVELS = ("INFO", "WARNING", "ERROR")


def find_log_files(folder):
    """Return sorted paths of *.log files in a folder."""
    try:
        names = sorted(os.listdir(folder))
    except FileNotFoundError:
        print(f"Folder not found: {folder}")
        return []
    return [os.path.join(folder, n) for n in names if n.endswith(".log")]


def parse_line(line):
    parts = line.split()
    if len(parts) < 4 or parts[2] not in LEVELS:
        raise ParseError(line.strip())
    fields = dict(w.split("=", 1) for w in parts[3:] if "=" in w)
    return {"level": parts[2], "time": parts[1], "fields": fields}


def analyse_file(path):
    """Count levels, collect timings and bad lines for one file."""
    stats = {"file": os.path.basename(path), "INFO": 0, "WARNING": 0, "ERROR": 0,
             "bad_lines": 0, "slow": []}
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            try:
                entry = parse_line(line)
            except ParseError:
                stats["bad_lines"] += 1
                continue
            stats[entry["level"]] += 1
            ms = int(entry["fields"].get("ms", 0))
            if ms >= 1000:
                stats["slow"].append({"time": entry["time"], "ms": ms,
                                      "path": entry["fields"].get("path", "-")})
    return stats


def write_reports(results, json_path, csv_path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", *LEVELS, "bad_lines"])
        for r in results:
            writer.writerow([r["file"], *(r[level] for level in LEVELS), r["bad_lines"]])


def main(folder="logs"):
    files = find_log_files(folder)
    print(f"Found {len(files)} log files in '{folder}'")
    results = [analyse_file(path) for path in files]
    write_reports(results, "report.json", "report.csv")

    totals = {level: sum(r[level] for r in results) for level in LEVELS}
    print(f"{'FILE':<12}{'INFO':>6}{'WARN':>6}{'ERROR':>7}{'BAD':>5}")
    for r in results:
        print(f"{r['file']:<12}{r['INFO']:>6}{r['WARNING']:>6}{r['ERROR']:>7}{r['bad_lines']:>5}")
    print(f"{'TOTAL':<12}{totals['INFO']:>6}{totals['WARNING']:>6}{totals['ERROR']:>7}")
    slow = [s | {"file": r["file"]} for r in results for s in r["slow"]]
    for s in sorted(slow, key=lambda s: s["ms"], reverse=True):
        print(f"SLOW: {s['file']} {s['time']} {s['path']} {s['ms']} ms")
    with open("report.csv", encoding="utf-8") as f:
        print("report.csv ->", f.read().splitlines())


main()
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `parse_line` validates the format and raises a custom `ParseError` for anything unexpected.
- Words containing `=` become structured fields (`path`, `ms`); other words form the message.

**Example 2 (project)**
- `find_log_files` lists the folder, keeps only `.log` files (the `readme.md` is ignored) and handles a missing folder gracefully.
- `analyse_file` streams each file line by line; a corrupted line increments `bad_lines` instead of stopping the job.
- Requests with `ms >= 1000` are recorded as slow.
- `write_reports` writes the same results as JSON (for other programs) and CSV (for people with spreadsheets). `*LEVELS` unpacks the tuple into the header row.
- `s | {"file": ...}` merges dicts (Python 3.9+).
- `main` wires everything together and prints a summary table.

## 7. Expected Output

**Example 1:**

```text
{'timestamp': '2026-11-20 10:00:09', 'level': 'ERROR', 'message': 'Database timeout', 'fields': {'path': '/api/orders', 'ms': '5000'}}
ParseError: unexpected format: 'this line is corrupted'
```

**Example 2:**

```text
Found 3 log files in 'logs'
FILE          INFO  WARN  ERROR  BAD
db-01.log        1     1      0    0
web-01.log       3     1      1    0
web-02.log       2     0      2    1
TOTAL            6     2      3
SLOW: web-01.log 10:00:09 /api/orders 5000 ms
SLOW: web-01.log 10:00:05 /api/search 1850 ms
report.csv -> ['file,INFO,WARNING,ERROR,bad_lines', 'db-01.log,1,1,0,0', 'web-01.log,3,1,1,0', 'web-02.log,2,0,2,1']
```

## 8. Common Mistakes

**1. Letting one bad file stop everything**

Wrap per-file work so a single unreadable file is reported, not fatal.

**2. Hard-coding separators**

Use `os.path.join` (or pathlib) — `"logs\\" + name` breaks on Linux.

**3. Processing every file in a folder**

Always filter by extension/pattern; folders often contain README files, archives or hidden files.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — List log files:** Print the names and sizes (bytes) of all `.log` files in the `logs/` folder, sorted by size descending.
- **Task 2 (Medium) — Error extractor:** Write every ERROR line from all logs in `logs/` into `errors_only.log`, prefixed with the source file name (`web-02.log: ...`). Print the output file.
- **Task 3 (Practical Challenge) — Daily summary JSON:** Extend the project: produce `summary.json` with total counts per level, the error rate (% of valid lines), the number of corrupted lines, and the top error message (most frequent message among ERROR lines). Print the JSON.

## 10. DevOps/MLOps Connection

- **DevOps:** this is a mini version of what Logstash/Fluentd parsers do. Scheduled with cron or a Kubernetes CronJob, it becomes a daily report.
- **Cloud:** replace the local folder with S3 objects (Day 82) and you have a serverless log processor.
- **Data engineering:** extract (read files) → transform (parse/aggregate) → load (write JSON/CSV) = **ETL**.
- **MLOps:** the same robust "skip and count bad records" approach is used for data validation before training.
- Continue with **[Project 3 — Log File Analyzer](../../projects/03-log-file-analyzer/)**.

## 11. Interview Questions

**Q1. How would you make a file-processing script robust?**

<details><summary>Show answer</summary>

Validate inputs, filter files by pattern, stream large files, handle per-line and per-file errors, log/count failures, and write outputs atomically.

</details>

**Q2. Why write both JSON and CSV reports?**

<details><summary>Show answer</summary>

JSON is ideal for other programs/APIs; CSV is easy for humans in spreadsheets and BI tools.

</details>

**Q3. How would you run this every day at 6 am?**

<details><summary>Show answer</summary>

A cron entry (`0 6 * * * /usr/bin/python3 /opt/tools/process_logs.py`), a systemd timer, a Jenkins scheduled job or a Kubernetes CronJob.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 55 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 054](../../05-files-exceptions/day-054/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 056 ➡](../../06-modules-oop/day-056/README.md)
