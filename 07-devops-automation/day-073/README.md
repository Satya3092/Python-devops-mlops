# Day 073 — Python Automation for Log Analysis

[⬅ Day 072](../../07-devops-automation/day-072/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 074 ➡](../../07-devops-automation/day-074/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Parse a real-looking application log with regex into structured records
- Aggregate by level, IP, endpoint and time window
- Detect anomalies (error spikes, failed logins) and produce a report

## 2. Topic Explanation

Today you combine files (Days 46–51), regex (Day 72), dictionaries and functions into a reusable **log analyser** — the core of [Project 3](../../projects/03-log-file-analyzer/).

The repository's `datasets/app.log` looks like:
```
2026-11-20 10:00:00 ERROR [10.0.0.5] Database connection timeout after 2418ms
```

Pipeline:
1. **Parse** each line into a dict (`timestamp`, `level`, `ip`, `message`) with a compiled regex.
2. **Aggregate** with dictionaries or `collections.Counter` (a dict subclass built for counting: `Counter(items).most_common(3)`).
3. **Window** by minute: `timestamp[:16]` gives `2026-11-20 10:05`, perfect for "errors per minute".
4. **Detect** issues: error rate above a threshold, repeated failed logins from the same user/IP (possible brute force), slow responses.
5. **Report**: print a summary and save JSON for other tools.

`collections.defaultdict(list)` creates missing keys automatically — a cleaner alternative to `setdefault`.

## 3. Syntax

```python
from collections import Counter, defaultdict
counts = Counter(level for level in levels)
counts.most_common(3)
groups = defaultdict(list)
groups[key].append(item)
```

| Part | Meaning |
|---|---|
| `Counter` | Counts hashable items; `most_common(n)` returns the top n. |
| `defaultdict(list)` | Dict that creates an empty list for new keys. |
| `timestamp[:16]` | Truncate to the minute for time windows. |
| `compiled regex` | One pattern reused for every line. |

## 4. Example 1 — Basic Example: Parse and count with Counter

```python
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("../../datasets/app.log")
LINE = re.compile(r"^(?P<ts>\S+ \S+) (?P<level>INFO|WARNING|ERROR) \[(?P<ip>[\d.]+)\] (?P<msg>.+)$")

records = []
with LOG_PATH.open(encoding="utf-8") as f:
    for line in f:
        m = LINE.match(line.strip())
        if m:
            records.append(m.groupdict())

print("Parsed records:", len(records))
levels = Counter(r["level"] for r in records)
print("By level:", dict(levels))
print("Top IPs:", Counter(r["ip"] for r in records).most_common(2))
print("First record:", records[0])
```

## 5. Example 2 — Practical Example: Full analysis: windows, anomalies and a JSON report

```python
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

LOG_PATH = Path("../../datasets/app.log")
LINE = re.compile(r"^(?P<ts>\S+ \S+) (?P<level>INFO|WARNING|ERROR) \[(?P<ip>[\d.]+)\] (?P<msg>.+)$")
MS = re.compile(r"(\d+)ms")
USER = re.compile(r"user=(\w+)")
ERROR_RATE_LIMIT = 15.0          # percent
SLOW_MS = 2000


def parse(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LINE.match(line)
        if m:
            yield m.groupdict()


def analyse(records):
    levels = Counter()
    per_minute = defaultdict(Counter)
    error_messages = Counter()
    failed_logins = Counter()
    slow = []
    for r in records:
        levels[r["level"]] += 1
        per_minute[r["ts"][:16]][r["level"]] += 1
        if r["level"] == "ERROR":
            error_messages[MS.sub("<N>ms", r["msg"])] += 1     # normalise numbers
        if "Failed login" in r["msg"]:
            failed_logins[USER.search(r["msg"]).group(1)] += 1
        ms = MS.search(r["msg"])
        if ms and int(ms.group(1)) >= SLOW_MS:
            slow.append((r["ts"], int(ms.group(1)), r["msg"]))
    total = sum(levels.values())
    error_rate = levels["ERROR"] / total * 100
    busiest_minute = max(per_minute, key=lambda m: per_minute[m]["ERROR"])
    return {
        "total": total,
        "levels": dict(levels),
        "error_rate_percent": round(error_rate, 1),
        "alert": error_rate > ERROR_RATE_LIMIT,
        "top_errors": error_messages.most_common(3),
        "failed_logins": dict(failed_logins),
        "worst_minute": {"minute": busiest_minute, "errors": per_minute[busiest_minute]["ERROR"]},
        "slow_requests": len(slow),
        "slowest": max(slow, key=lambda s: s[1])[:2] if slow else None,
    }


report = analyse(parse(LOG_PATH))
print(f"Lines analysed : {report['total']}")
print(f"Levels         : {report['levels']}")
print(f"Error rate     : {report['error_rate_percent']}%  ALERT={report['alert']}")
print("Top errors     :")
for message, count in report["top_errors"]:
    print(f"   {count} x {message}")
print(f"Failed logins  : {report['failed_logins']}")
print(f"Worst minute   : {report['worst_minute']}")
print(f"Slow requests  : {report['slow_requests']} (slowest {report['slowest']})")

Path("log_report.json").write_text(json.dumps(report, indent=2))
print("Saved log_report.json with keys:", list(json.loads(Path("log_report.json").read_text())))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The compiled regex extracts four named fields from each line; lines that don't match are ignored.
- `Counter(...)` counts levels and IPs in one line; `most_common(2)` returns the two busiest IPs.

**Example 2**
- `parse` is a generator: it yields records one by one, so it would also work on huge files.
- `defaultdict(Counter)` builds "per minute → per level" counts without any `if key in dict` checks.
- Error messages are **normalised** (`2418ms` → `<N>ms`) so similar errors group together — a technique used by log-aggregation tools.
- Failed logins are counted per user — the basis for brute-force detection.
- The report is a plain dict, printed for humans and saved as JSON for machines (dashboards, alerting, Slack bots).

## 7. Expected Output

**Example 1:**

```text
Parsed records: 60
By level: {'ERROR': 13, 'WARNING': 17, 'INFO': 30}
Top IPs: [('10.0.0.5', 15), ('10.0.0.7', 15)]
First record: {'ts': '2026-11-20 10:00:00', 'level': 'ERROR', 'ip': '10.0.0.5', 'msg': 'Database connection timeout after 2418ms'}
```

**Example 2:**

```text
Lines analysed : 60
Levels         : {'ERROR': 13, 'WARNING': 17, 'INFO': 30}
Error rate     : 21.7%  ALERT=True
Top errors     :
   8 x Database connection timeout after <N>ms
   4 x GET /api/payments 500 <N>ms
   1 x Failed login user=dave
Failed logins  : {'dave': 1}
Worst minute   : {'minute': '2026-11-20 10:05', 'errors': 2}
Slow requests  : 6 (slowest ('2026-11-20 10:11:41', 2879))
Saved log_report.json with keys: ['total', 'levels', 'error_rate_percent', 'alert', 'top_errors', 'failed_logins', 'worst_minute', 'slow_requests', 'slowest']
```

## 8. Common Mistakes

**1. Grouping un-normalised messages**

`timeout after 2418ms` and `timeout after 2002ms` count as different errors unless you normalise variable parts.

**2. Loading huge logs into memory**

Use generators / line-by-line iteration for multi-GB logs.

**3. Assuming every line matches**

Real logs contain stack traces and multi-line messages. Handle non-matching lines explicitly.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Count by level:** Using `../../datasets/app.log`, print how many INFO, WARNING and ERROR lines exist using `Counter`.
- **Task 2 (Medium) — Errors per IP:** For each IP, print the number of ERROR lines and the error percentage of that IP's traffic, sorted by error count.
- **Task 3 (Practical Challenge) — Brute-force and deployment timeline:** From the same log, (a) list every user with failed logins and how many, (b) list every `Deployment v1.x started` event with its time, and (c) for each deployment, count ERROR lines in the 2 minutes after it (compare `HH:MM` strings). Print a small incident timeline.

## 10. DevOps/MLOps Connection

- **DevOps / SRE:** incident triage ("what broke after the deploy?"), error budgets, brute-force detection, daily log summaries in Slack.
- **Cloud:** the same analysis applies to CloudWatch Logs exports, ALB logs in S3 or Kubernetes pod logs.
- **ML/MLOps:** parsed logs become structured datasets for anomaly detection; inference-service logs are analysed for latency and error trends.

## 11. Interview Questions

**Q1. Why normalise log messages before counting?**

<details><summary>Show answer</summary>

Variable parts (IDs, durations) make every message unique; replacing them groups identical error types.

</details>

**Q2. What is `collections.Counter` useful for?**

<details><summary>Show answer</summary>

Counting hashable items, finding most common elements, and arithmetic between counts.

</details>

**Q3. How would you correlate errors with deployments?**

<details><summary>Show answer</summary>

Parse deployment events and error timestamps, then count errors in a time window after each deployment (or compare error rates before/after).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 73 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 072](../../07-devops-automation/day-072/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 074 ➡](../../07-devops-automation/day-074/README.md)
