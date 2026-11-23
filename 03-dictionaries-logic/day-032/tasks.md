# Day 032 — Practice Tasks: Break, Continue, and Pass

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Stop at negative

**Problem statement:** Loop over `[4, 7, 2, -1, 9]` and print numbers until a negative number appears, then print `Stopped at -1`.

**Input requirements:** No user input required.

**Expected behavior:** Prints 4, 7, 2 then the stop message.

**Expected output:**

```text
4
7
2
Stopped at -1
```

## Task 2 — Medium: Skip maintenance hosts

**Problem statement:** Given hosts `["web-01", "web-02 (maintenance)", "web-03", "db-01 (maintenance)"]`, print `Deploying to <host>` only for hosts not in maintenance and count skipped hosts.

**Input requirements:** No user input required.

**Expected behavior:** Deploys to web-01, web-03; 2 skipped.

**Expected output:**

```text
Deploying to web-01
Deploying to web-03
Skipped: 2
```

## Task 3 — Practical Challenge: Find a healthy replica

**Problem statement:** Replicas are checked in order: `[("replica-1", 503), ("replica-2", 500), ("replica-3", 200), ("replica-4", 200)]`. Route traffic to the first replica that returns 200. If none is healthy, print `All replicas down - failing over to DR region`. Test with the given list and with a list where all return 500.

**Input requirements:** No user input required.

**Expected behavior:** Routes to replica-3 for the first list; prints the failover message for the second.

**Expected output:**

```text
Routing traffic to replica-3
All replicas down - failing over to DR region
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
