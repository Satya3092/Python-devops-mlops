# Day 039 — Practice Tasks: Default Arguments

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Power function

**Problem statement:** Write `power(base, exponent=2)` and print `power(5)`, `power(2, 10)`.

**Input requirements:** No user input required.

**Expected behavior:** 25 and 1024.

**Expected output:**

```text
25
1024
```

## Task 2 — Medium: Backup filename

**Problem statement:** Write `backup_name(db, date="2026-11-20", ext="sql.gz")` that returns `<db>-<date>.<ext>`. Call it with only the db, with a custom date, and with a custom extension.

**Input requirements:** No user input required.

**Expected behavior:** Three filenames.

**Expected output:**

```text
orders-2026-11-20.sql.gz
orders-2026-12-01.sql.gz
users-2026-11-20.dump
```

## Task 3 — Practical Challenge: HTTP request description

**Problem statement:** Write `describe_request(url, method="GET", headers=None, timeout=5, retries=3)` that returns a multi-line description. Merge any given headers with a default `User-Agent: devops-script/1.0` header without modifying the caller's dict. Show the caller's dict is unchanged.

**Input requirements:** No user input required.

**Expected behavior:** Two descriptions and proof that the original headers dict was not modified.

**Expected output:**

```text
GET https://api.example.com/health
  headers: {'User-Agent': 'devops-script/1.0'}
  timeout: 5s, retries: 3
POST https://api.example.com/orders
  headers: {'User-Agent': 'devops-script/1.0', 'Accept': 'application/json'}
  timeout: 10s, retries: 3
Caller's headers unchanged: {'Accept': 'application/json'}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
