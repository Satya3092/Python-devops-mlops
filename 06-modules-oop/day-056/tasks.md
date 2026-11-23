# Day 056 — Practice Tasks: Modules and Imports

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Math helpers

**Problem statement:** Use `math` to print the square root of 2 (4 decimals), `math.floor(9.99)`, and `math.factorial(5)`.

**Input requirements:** No user input required.

**Expected behavior:** 1.4142, 9, 120.

**Expected output:**

```text
1.4142
9
120
```

## Task 2 — Medium: Your first module

**Problem statement:** Create `string_tools.py` (in the solution this file is written for you) with `slugify(text)` and `shorten(text, n)`. Import it and use both functions.

**Input requirements:** No user input required.

**Expected behavior:** `payment-service-api` and `Deploy...`.

**Expected output:**

```text
payment-service-api
Deploy...
```

## Task 3 — Practical Challenge: Unit converter module with self-test

**Problem statement:** Create `units.py` with `bytes_to_human(n)` that returns strings like `1.5 GB`, plus a `__main__` self-test. Import it and print sizes for 512, 2048, 5_000_000 and 7_500_000_000 bytes. Then run the module directly with `subprocess` (preview of Day 61) to show the self-test output.

**Input requirements:** No user input required.

**Expected behavior:** Human-readable sizes and the self-test line.

**Expected output:**

```text
512 -> 512.0 B
2048 -> 2.0 KB
5000000 -> 4.8 MB
7500000000 -> 7.0 GB
self-test: 1.5 KB
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
