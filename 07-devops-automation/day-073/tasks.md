# Day 073 — Practice Tasks: Python Automation for Log Analysis

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Count by level

**Problem statement:** Using `../../datasets/app.log`, print how many INFO, WARNING and ERROR lines exist using `Counter`.

**Input requirements:** No user input required.

**Expected behavior:** Three counts that sum to 60.

**Expected output:**

```text
Counter({'INFO': 30, 'WARNING': 17, 'ERROR': 13})
```

## Task 2 — Medium: Errors per IP

**Problem statement:** For each IP, print the number of ERROR lines and the error percentage of that IP's traffic, sorted by error count.

**Input requirements:** No user input required.

**Expected behavior:** A table of 4 IPs.

**Expected output:**

```text
10.0.0.5       errors=5   of 15  (33%)
10.0.0.7       errors=3   of 15  (20%)
192.168.1.20   errors=3   of 15  (20%)
10.0.1.12      errors=2   of 15  (13%)
```

## Task 3 — Practical Challenge: Brute-force and deployment timeline

**Problem statement:** From the same log, (a) list every user with failed logins and how many, (b) list every `Deployment v1.x started` event with its time, and (c) for each deployment, count ERROR lines in the 2 minutes after it (compare `HH:MM` strings). Print a small incident timeline.

**Input requirements:** No user input required.

**Expected behavior:** Users with failed logins and deployments with following-error counts.

**Expected output:**

```text
Failed logins per user: {'dave': 1}
10:01:14  Deployment v1.2 started  errors in next 2 min: 1
10:02:35  Deployment v1.5 started  errors in next 2 min: 1
10:13:09  Deployment v1.0 started  errors in next 2 min: 0
10:16:51  Deployment v1.6 started  errors in next 2 min: 0
10:22:08  Deployment v1.8 started  errors in next 2 min: 2
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
