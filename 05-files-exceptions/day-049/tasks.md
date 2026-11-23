# Day 049 — Practice Tasks: Append Mode

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Shopping list

**Problem statement:** Append three items to `shopping.txt` in two separate `with` blocks (2 items then 1). Print the file.

**Input requirements:** No user input required.

**Expected behavior:** Three items listed.

**Expected output:**

```text
milk
bread
coffee
```

## Task 2 — Medium: Audit trail

**Problem statement:** Write a function `audit(user, action)` that appends `user|action` to `audit.log`. Call it 4 times, then read the file and print how many actions each user performed.

**Input requirements:** No user input required.

**Expected behavior:** Counts per user.

**Expected output:**

```text
{'asha': 3, 'ravi': 1}
```

## Task 3 — Practical Challenge: Uptime history

**Problem statement:** Simulate 6 health checks with statuses `[200, 200, 503, 200, 500, 200]`. For each, append `check_number,status,UP/DOWN` to `uptime.csv` (header only once). Then read the file and compute the availability percentage.

**Input requirements:** No user input required.

**Expected behavior:** Availability 66.7%.

**Expected output:**

```text
Availability: 66.7%
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
