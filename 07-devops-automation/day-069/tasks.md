# Day 069 — Practice Tasks: System Information and Resource Monitoring

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: One-line status

**Problem statement:** Print one line with CPU %, memory % and root disk % using psutil.

**Input requirements:** No user input required.

**Expected behavior:** Something like `CPU: 6.0% | Memory: 38.5% | Disk: 44.4%`.

**Expected output:**

```text
CPU: 6.0% | Memory: 38.5% | Disk: 44.4%
```

## Task 2 — Medium: Sampling loop

**Problem statement:** Take 3 samples (1 second apart) of CPU and memory %, print each, then print the average and peak CPU.

**Input requirements:** No user input required.

**Expected behavior:** Three samples plus average/peak.

**Expected output:**

```text
Sample 1: cpu=5.5% mem=38.4%
Sample 2: cpu=12.0% mem=38.5%
Sample 3: cpu=7.1% mem=38.4%
Average CPU: 8.2% | Peak CPU: 12.0%
```

## Task 3 — Practical Challenge: Process report

**Problem statement:** List processes using more than 1 % memory (name, pid, %), sorted descending, print their combined memory share and the total number of processes.

**Input requirements:** No user input required.

**Expected behavior:** A filtered process list and totals.

**Expected output:**

```text
Processes using > 1.0% memory:
  java (pid 1342): 12.6%
  dockerd (pid 2210): 3.1%
  containerd (pid 987): 1.8%
Total memory used by them: 17.5%
Process count: 213
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
