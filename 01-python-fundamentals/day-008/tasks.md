# Day 008 — Practice Tasks: Comparison Operators

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Port checks

**Problem statement:** Given `port = 22`, print whether it equals 22, is a privileged port (< 1024), and is not 80.

**Input requirements:** No user input required.

**Expected behavior:** Three True/False lines.

**Expected output:**

```text
Is SSH port: True
Privileged port: True
Not HTTP: True
```

## Task 2 — Medium: Version comparison trap

**Problem statement:** Compare `"10"` and `"9"` as strings and as integers. Print both results and a sentence explaining the difference.

**Input requirements:** No user input required.

**Expected behavior:** String comparison gives False; integer comparison gives True.

**Expected output:**

```text
'10' > '9' as strings: False
10 > 9 as integers: True
Strings compare character by character, so '1' < '9' makes '10' smaller.
```

## Task 3 — Practical Challenge: SLA checker

**Problem statement:** An SLA requires uptime >= 99.9 %, average latency < 200 ms and error rate <= 1 %. Given `uptime = 99.95`, `latency_ms = 215`, `error_rate = 0.4`, store each check in a boolean variable and print them plus an overall result using `and` (preview of Day 9).

**Input requirements:** No user input required.

**Expected behavior:** Uptime True, latency False, errors True, SLA met False.

**Expected output:**

```text
Uptime OK: True
Latency OK: False
Error rate OK: True
SLA met: False
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
