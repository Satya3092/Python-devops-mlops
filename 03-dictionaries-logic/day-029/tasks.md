# Day 029 — Practice Tasks: For Loops

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Multiplication table

**Problem statement:** Print the multiplication table of 7 from 7 × 1 to 7 × 10.

**Input requirements:** No user input required.

**Expected behavior:** Ten lines like `7 x 3 = 21`.

**Expected output:**

```text
7 x 1 = 7
7 x 2 = 14
7 x 3 = 21
7 x 4 = 28
7 x 5 = 35
7 x 6 = 42
7 x 7 = 49
7 x 8 = 56
7 x 9 = 63
7 x 10 = 70
```

## Task 2 — Medium: Service URLs

**Problem statement:** Given `services = ["auth", "orders", "search"]` and `ports = [8001, 8002, 8003]`, print `http://<service>.internal:<port>/health` for each with a number prefix using `enumerate` and `zip`.

**Input requirements:** No user input required.

**Expected behavior:** Three numbered URLs.

**Expected output:**

```text
1. http://auth.internal:8001/health
2. http://orders.internal:8002/health
3. http://search.internal:8003/health
```

## Task 3 — Practical Challenge: Disk cleanup candidates

**Problem statement:** Given files as tuples `(name, size_mb, days_old)`: `[("app.log", 120, 2), ("app.log.1", 300, 10), ("backup.tar", 4096, 40), ("core.dump", 2048, 15), ("notes.txt", 1, 100)]`, find files older than 7 days and bigger than 100 MB. Print each candidate and the total space you would free in GB.

**Input requirements:** No user input required.

**Expected behavior:** Three candidates; total ≈ 6.15 GB.

**Expected output:**

```text
Candidate: app.log.1 (300 MB, 10 days old)
Candidate: backup.tar (4096 MB, 40 days old)
Candidate: core.dump (2048 MB, 15 days old)
Space to free: 6.29 GB
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
