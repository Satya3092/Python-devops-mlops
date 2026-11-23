# Day 044 — Practice Tasks: Lambda Functions

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Sort students by marks

**Problem statement:** Sort `[("Asha", 88), ("Ravi", 72), ("Meera", 95)]` by marks (highest first) using a lambda.

**Input requirements:** No user input required.

**Expected behavior:** Meera, Asha, Ravi.

**Expected output:**

```text
[('Meera', 95), ('Asha', 88), ('Ravi', 72)]
```

## Task 2 — Medium: Filter and transform files

**Problem statement:** From `["app.log", "data.csv", "error.log", "model.pkl", "access.log"]`, use `filter` with a lambda to keep `.log` files and `map` to upper-case them.

**Input requirements:** No user input required.

**Expected behavior:** `['APP.LOG', 'ERROR.LOG', 'ACCESS.LOG']`.

**Expected output:**

```text
['APP.LOG', 'ERROR.LOG', 'ACCESS.LOG']
```

## Task 3 — Practical Challenge: Cost optimisation report

**Problem statement:** Given instances `(id, type, hourly_cost, avg_cpu)`: `[("i-1", "m5.xlarge", 0.192, 8), ("i-2", "t3.micro", 0.0104, 55), ("i-3", "c5.2xlarge", 0.34, 12), ("i-4", "m5.large", 0.096, 71)]`, find idle instances (avg_cpu < 15) with `filter`, sort them by monthly cost (730 h) descending with a lambda, and print the potential monthly savings.

**Input requirements:** No user input required.

**Expected behavior:** i-3 then i-1, savings ≈ $388.36.

**Expected output:**

```text
i-3 c5.2xlarge  cpu=12% monthly=$248.20
i-1 m5.xlarge   cpu=8% monthly=$140.16
Potential monthly savings: $388.36
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
