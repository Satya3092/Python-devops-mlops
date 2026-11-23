# Day 009 — Practice Tasks: Logical Operators

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Access check

**Problem statement:** A user can deploy if `is_admin` is True **or** (`is_developer` is True **and** `environment` is not `prod`). Test with is_admin=False, is_developer=True, environment='staging'.

**Input requirements:** No user input required.

**Expected behavior:** Prints `Can deploy: True`.

**Expected output:**

```text
Can deploy: True
```

## Task 2 — Medium: Business hours

**Problem statement:** Given `hour = 14` and `is_weekday = True`, decide if this is a safe deployment window (weekday, between 10 and 16 inclusive) and print the result. Also print the opposite using `not`.

**Input requirements:** No user input required.

**Expected behavior:** `Safe window: True` and `Freeze period: False`.

**Expected output:**

```text
Safe window: True
Freeze period: False
```

## Task 3 — Practical Challenge: Backup decision

**Problem statement:** Run a backup if the disk has more than 20 GB free AND (it is after 01:00 and before 05:00 OR a `force_backup` flag is set) AND no other backup is running. Evaluate for free_gb=35, hour=14, force_backup=True, backup_running=False and explain each part.

**Input requirements:** No user input required.

**Expected behavior:** Prints each partial condition and `Run backup: True`.

**Expected output:**

```text
Enough space: True
Night time: False | Forced: True | Allowed time: True
No other backup running: True
Run backup: True
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
