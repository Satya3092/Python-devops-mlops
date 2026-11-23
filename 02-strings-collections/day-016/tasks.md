# Day 016 — Practice Tasks: Strings Introduction

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Full hostname

**Problem statement:** Given `service = "auth"`, `env = "prod"`, `number = "03"`, build the hostname `auth-prod-03` with `+` and print it with its length.

**Input requirements:** No user input required.

**Expected behavior:** Prints `auth-prod-03` and `Length: 12`.

**Expected output:**

```text
auth-prod-03
Length: 12
```

## Task 2 — Medium: Keyword scanner

**Problem statement:** Given the log line `"2026-11-20 10:21:01 WARNING Disk usage 91% on /var"`, print which of the words ERROR, WARNING, Disk, disk are present.

**Input requirements:** No user input required.

**Expected behavior:** Four lines with True/False.

**Expected output:**

```text
ERROR present: False
WARNING present: True
Disk present: True
disk present: False
```

## Task 3 — Practical Challenge: Banner generator

**Problem statement:** Given a message `"Deployment v2.3.0 complete"`, print it framed in a box of `#` characters whose width automatically matches the message length + 4.

**Input requirements:** No user input required.

**Expected behavior:** A three-line box that fits the message exactly.

**Expected output:**

```text
##############################
# Deployment v2.3.0 complete #
##############################
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
