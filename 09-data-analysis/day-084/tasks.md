# Day 084 — Practice Tasks: NumPy Introduction

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Create arrays

**Problem statement:** Create an array of the numbers 1–10, a 3×3 array of zeros, and 5 evenly spaced values from 0 to 100. Print each with its shape and dtype.

**Input requirements:** No user input required.

**Expected behavior:** Three arrays with shapes (10,), (3, 3), (5,).

**Expected output:**

```text
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10] (10,) int64
[[0.0, 0.0, 0.0], [0.0, 0.0, 0.0], [0.0, 0.0, 0.0]] (3, 3) float64
[0.0, 25.0, 50.0, 75.0, 100.0] (5,) float64
```

## Task 2 — Medium: Convert units

**Problem statement:** Given disk sizes in bytes `[1073741824, 536870912, 2147483648, 268435456]`, convert them to GB with one vectorised operation and print the total.

**Input requirements:** No user input required.

**Expected behavior:** `[1.0, 0.5, 2.0, 0.25]` and total 3.75 GB.

**Expected output:**

```text
[1.0, 0.5, 2.0, 0.25] total: 3.75 GB
```

## Task 3 — Practical Challenge: Simulated traffic

**Problem statement:** With `default_rng(1)`, simulate 24 hourly request counts as integers between 1000 and 5000. Print the array, the busiest hour (index with `argmax`), the quietest hour and how many hours exceeded 4000 requests.

**Input requirements:** No user input required.

**Expected behavior:** 24 numbers and three summary lines.

**Expected output:**

```text
[2893 3047 4021 4802 1139 1576 4292 4795 1997 2247 4476 2693 2092 4311
 2028 2637 3575 3198 1343 1110 4463 4014 4352 3153]
Busiest hour: 3 with 4802
Quietest hour: 19 with 1110
Hours over 4000: 9
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
