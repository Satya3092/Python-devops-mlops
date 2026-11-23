# Day 055 — Practice Tasks: File Processing Automation Project

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: List log files

**Problem statement:** Print the names and sizes (bytes) of all `.log` files in the `logs/` folder, sorted by size descending.

**Input requirements:** No user input required.

**Expected behavior:** Three files with sizes.

**Expected output:**

```text
web-01.log     320 bytes
web-02.log     273 bytes
db-01.log      103 bytes
```

## Task 2 — Medium: Error extractor

**Problem statement:** Write every ERROR line from all logs in `logs/` into `errors_only.log`, prefixed with the source file name (`web-02.log: ...`). Print the output file.

**Input requirements:** No user input required.

**Expected behavior:** Three ERROR lines with file prefixes.

**Expected output:**

```text
web-01.log: 2026-11-20 10:00:09 ERROR Database timeout path=/api/orders ms=5000
web-02.log: 2026-11-20 10:00:06 ERROR Upstream 502 path=/api/payments ms=30
web-02.log: 2026-11-20 10:00:11 ERROR Upstream 502 path=/api/payments ms=28
```

## Task 3 — Practical Challenge: Daily summary JSON

**Problem statement:** Extend the project: produce `summary.json` with total counts per level, the error rate (% of valid lines), the number of corrupted lines, and the top error message (most frequent message among ERROR lines). Print the JSON.

**Input requirements:** No user input required.

**Expected behavior:** JSON with totals, error rate, bad lines and top error `Upstream 502`.

**Expected output:**

```text
{
  "totals": {
    "INFO": 6,
    "WARNING": 2,
    "ERROR": 3
  },
  "error_rate_percent": 27.3,
  "bad_lines": 1,
  "top_error": "Upstream 502"
}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
