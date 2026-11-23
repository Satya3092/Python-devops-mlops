# Day 075 — Practice Tasks: DevOps Automation Project

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Run and inspect

**Problem statement:** Run `server_monitor.py` with `--output-dir task_reports` via subprocess, then count the JSON and TXT reports created and print the overall status from the JSON.

**Input requirements:** No user input required.

**Expected behavior:** 1 JSON, 1 TXT and the overall status.

**Expected output:**

```text
Reports in folder: 1 JSON, 1 TXT
Overall status: OK
```

## Task 2 — Medium: Exit-code experiment

**Problem statement:** Run the tool twice: once with absurdly low CPU thresholds (`--cpu-warn 1 --cpu-crit 2`, which will almost always be CRITICAL) and once with thresholds of 100/101 for every metric. Print both exit codes.

**Input requirements:** No user input required.

**Expected behavior:** A non-zero exit code first, 0 second.

**Expected output:**

```text
Run with --cpu-warn 1 --cpu-crit 2: exit code 2 (CRITICAL expected on a busy CPU)
Run with very high thresholds: exit code 0
```

## Task 3 — Practical Challenge: Add a CSV history

**Problem statement:** Import `server_monitor`, run `collect` once, and append one row per check (`timestamp, hostname, metric, value, status`) to `history.csv` (header only when the file is new). Print the rows and the row count. (Bonus: add this as a `--history-csv` option in the tool.)

**Input requirements:** No user input required.

**Expected behavior:** Three rows (cpu, memory, disk).

**Expected output:**

```text
ip-10-0-1-25 cpu       8.2% OK
ip-10-0-1-25 memory   41.7% OK
ip-10-0-1-25 disk     83.4% WARNING
history.csv rows: 3
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
