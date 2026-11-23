# Day 010 — Practice Tasks: Assignment Operators

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Countdown

**Problem statement:** Start with `seconds = 10`. Subtract 3 three times with `-=` and print the value after each step.

**Input requirements:** No user input required.

**Expected behavior:** Prints 7, 4, 1.

**Expected output:**

```text
7
4
1
```

## Task 2 — Medium: Exponential backoff

**Problem statement:** Starting from 1 second, double the delay with `*=` five times and print the delay for each retry attempt. Also keep a running total of waiting time with `+=`.

**Input requirements:** No user input required.

**Expected behavior:** Delays 2, 4, 8, 16, 32 and total 62.

**Expected output:**

```text
Attempt 1 -> wait 2 s
Attempt 2 -> wait 4 s
Attempt 3 -> wait 8 s
Attempt 4 -> wait 16 s
Attempt 5 -> wait 32 s
Total waiting time: 62 s
```

## Task 3 — Practical Challenge: Daily bandwidth meter

**Problem statement:** A server transferred 1.2 GB, 3.4 GB, 0.8 GB and 2.6 GB in four time slots. Use `+=` to total the GB, convert to MB with `*=` (1024), then compute what is left of a 10 GB daily quota with `-=`.

**Input requirements:** No user input required.

**Expected behavior:** Prints total GB, total MB and the remaining quota.

**Expected output:**

```text
Total transferred: 8.0 GB
Total transferred: 8192.0 MB
Remaining quota: 2.0 GB
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
