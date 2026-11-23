# Day 049 — Append Mode

[⬅ Day 048](../../05-files-exceptions/day-048/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 050 ➡](../../05-files-exceptions/day-050/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Add data to the end of a file with mode `"a"`
- Build simple log files and audit trails
- Combine append mode with timestamps

## 2. Topic Explanation

Mode `"a"` (**append**) opens a file for writing **at the end**, keeping existing content. If the file does not exist, it is created.

```python
with open("app.log", "a", encoding="utf-8") as log:
    log.write("Service started\n")
```

Typical uses:
- **Log files** — each run adds new lines.
- **Audit trails** — "who did what, when".
- **CSV history** — one new row per measurement.

Like `>>` in Bash (`echo "msg" >> app.log`), while `"w"` is like `>`.

Add **timestamps** with the `datetime` module so you know when each line was written:
```python
from datetime import datetime
datetime.now().strftime("%Y-%m-%d %H:%M:%S")
```

`"a+"` lets you append and also read (rarely needed).

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work.

## 3. Syntax

```python
with open("file.log", "a", encoding="utf-8") as f:
    f.write("new line\n")
```

| Part | Meaning |
|---|---|
| `"a"` | Append: write at the end, create if missing. |
| `"w" vs "a"` | `w` = overwrite (like `>`), `a` = append (like `>>`). |
| `datetime.now()` | Current timestamp for log lines. |

## 4. Example 1 — Basic Example: Appending vs overwriting

```python
with open("visits.txt", "w", encoding="utf-8") as f:
    f.write("visit 1\n")

with open("visits.txt", "a", encoding="utf-8") as f:
    f.write("visit 2\n")
    f.write("visit 3\n")

with open("visits.txt", encoding="utf-8") as f:
    print(f.read(), end="")

with open("visits.txt", "a", encoding="utf-8") as f:
    f.write("visit 4\n")

with open("visits.txt", encoding="utf-8") as f:
    print("Total visits recorded:", len(f.readlines()))
```

## 5. Example 2 — Practical Example: A tiny logger and a metrics history CSV

```python
from datetime import datetime, timedelta

LOG_FILE = "deploy.log"
start = datetime(2026, 11, 20, 10, 0, 0)        # fixed time so output is reproducible


def log(level, message, when):
    """Append one timestamped line to the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{when:%Y-%m-%d %H:%M:%S} [{level}] {message}\n")


steps = ["Pulling image", "Stopping old container", "Starting new container", "Health check passed"]
for i, step in enumerate(steps):
    log("INFO", step, start + timedelta(seconds=i * 5))
log("INFO", "Deployment finished", start + timedelta(seconds=20))

with open(LOG_FILE, encoding="utf-8") as f:
    print(f.read(), end="")

# Append metrics rows; write the header only if the file is new
import os
METRICS = "cpu_history.csv"
for minute, cpu in enumerate([35.2, 41.8, 77.5]):
    new_file = not os.path.exists(METRICS)
    with open(METRICS, "a", encoding="utf-8") as f:
        if new_file:
            f.write("timestamp,cpu_percent\n")
        f.write(f"{start + timedelta(minutes=minute):%H:%M},{cpu}\n")

with open(METRICS, encoding="utf-8") as f:
    print(f.read(), end="")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The first open uses `"w"` (start fresh); later opens use `"a"` so earlier lines are kept.

**Example 2**
- `log()` opens the file in append mode for every message — simple and safe even if the program crashes midway.
- `f"{when:%Y-%m-%d %H:%M:%S}"` formats a datetime inside an f-string.
- `timedelta` adds seconds/minutes to a datetime (we use a fixed start so the output is reproducible; real code uses `datetime.now()`).
- The CSV writer writes the header only when the file did not exist yet — the classic append-to-CSV pattern.

## 7. Expected Output

**Example 1:**

```text
visit 1
visit 2
visit 3
Total visits recorded: 4
```

**Example 2:**

```text
2026-11-20 10:00:00 [INFO] Pulling image
2026-11-20 10:00:05 [INFO] Stopping old container
2026-11-20 10:00:10 [INFO] Starting new container
2026-11-20 10:00:15 [INFO] Health check passed
2026-11-20 10:00:20 [INFO] Deployment finished
timestamp,cpu_percent
10:00,35.2
10:01,41.8
10:02,77.5
```

## 8. Common Mistakes

**1. Using `"w"` for logs**

Each run would erase the previous log. Use `"a"`.

**2. Header written every time**

Appending a CSV header on every run corrupts the data. Write it only when creating the file.

**3. Logs growing forever**

Append-only files need rotation (`logrotate` or Python's `RotatingFileHandler`, Day 62).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Shopping list:** Append three items to `shopping.txt` in two separate `with` blocks (2 items then 1). Print the file.
- **Task 2 (Medium) — Audit trail:** Write a function `audit(user, action)` that appends `user|action` to `audit.log`. Call it 4 times, then read the file and print how many actions each user performed.
- **Task 3 (Practical Challenge) — Uptime history:** Simulate 6 health checks with statuses `[200, 200, 503, 200, 500, 200]`. For each, append `check_number,status,UP/DOWN` to `uptime.csv` (header only once). Then read the file and compute the availability percentage.

## 10. DevOps/MLOps Connection

- **DevOps:** application and audit logs, deployment history, cron job output (`>> job.log`).
- **Monitoring:** appending metrics to CSV for quick trend analysis before using Prometheus.
- **MLOps:** appending one row per training run (date, parameters, accuracy) creates a simple experiment log — the idea behind MLflow tracking.

## 11. Interview Questions

**Q1. What is the difference between `w` and `a` modes?**

<details><summary>Show answer</summary>

`w` truncates the file; `a` keeps existing content and writes at the end.

</details>

**Q2. What happens when you open a non-existent file in append mode?**

<details><summary>Show answer</summary>

It is created.

</details>

**Q3. How do you prevent log files from filling the disk?**

<details><summary>Show answer</summary>

Use log rotation (logrotate, RotatingFileHandler/TimedRotatingFileHandler) and retention policies, or ship logs to a central system.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 49 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 048](../../05-files-exceptions/day-048/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 050 ➡](../../05-files-exceptions/day-050/README.md)
