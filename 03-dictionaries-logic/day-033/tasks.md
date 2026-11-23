# Day 033 — Practice Tasks: Nested Loops

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Number pyramid

**Problem statement:** Print a pyramid where row n contains the numbers 1..n separated by spaces, for 5 rows.

**Input requirements:** No user input required.

**Expected behavior:** `1`, `1 2`, … `1 2 3 4 5`.

**Expected output:**

```text
1
1 2
1 2 3
1 2 3 4
1 2 3 4 5
```

## Task 2 — Medium: Inventory per environment

**Problem statement:** Given `inventory = {"dev": ["web-01"], "staging": ["web-01", "web-02"], "prod": ["web-01", "web-02", "web-03", "db-01"]}`, print every host as `<env>/<host>` and the host count per environment.

**Input requirements:** No user input required.

**Expected behavior:** All hosts and counts 1, 2, 4.

**Expected output:**

```text
dev/web-01
staging/web-01
staging/web-02
prod/web-01
prod/web-02
prod/web-03
prod/db-01
dev: 1 hosts
staging: 2 hosts
prod: 4 hosts
```

## Task 3 — Practical Challenge: Port scan matrix (simulated)

**Problem statement:** Given hosts `["10.0.0.1", "10.0.0.2", "10.0.0.3"]`, ports `[22, 80, 443, 3306]` and a simulated set of open `(host, port)` pairs `{("10.0.0.1", 22), ("10.0.0.1", 80), ("10.0.0.2", 443), ("10.0.0.3", 3306), ("10.0.0.3", 22)}`, print a table with OPEN/closed per host and port, then list hosts exposing MySQL.

**Input requirements:** No user input required.

**Expected behavior:** A 3 × 4 status table and `MySQL exposed on: ['10.0.0.3']`.

**Expected output:**

```text
HOST           22     80    443   3306
10.0.0.1     OPEN   OPEN closed closed
10.0.0.2   closed closed   OPEN closed
10.0.0.3     OPEN closed closed   OPEN
MySQL exposed on: ['10.0.0.3']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
