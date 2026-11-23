# Day 045 — Practice Tasks: Functions Revision and Mini Project

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Temperature converter module

**Problem statement:** Write `c_to_f`, `f_to_c`, `c_to_k` functions and a dispatch dict keyed by `"c->f"`, `"f->c"`, `"c->k"`. Convert 100 using each.

**Input requirements:** No user input required.

**Expected behavior:** 212.0, 37.78, 373.15.

**Expected output:**

```text
100 c->f: 212.0
100 f->c: 37.78
100 c->k: 373.15
```

## Task 2 — Medium: Statistics helper

**Problem statement:** Write `stats(*values, precision=2)` returning a dict with count, min, max, mean and median. Use it on response times `[120, 87, 450, 134, 98, 101]`.

**Input requirements:** No user input required.

**Expected behavior:** count 6, min 87, max 450, mean 165.0, median 110.5.

**Expected output:**

```text
{'count': 6, 'min': 87, 'max': 450, 'mean': 165.0, 'median': 110.5}
```

## Task 3 — Practical Challenge: Extend the calculator

**Problem statement:** Add `%` (modulo) and `//` (floor division) to the mini project, make both safe for zero, and add a `history` list (passed in as a parameter, not global) that stores every successful calculation as a string. Print the history at the end.

**Input requirements:** No user input required.

**Expected behavior:** New operators work; errors are not stored in history.

**Expected output:**

```text
17 % 5 -> 2.0
17 // 5 -> 3.0
8 // 0 -> division by zero
3 * 4 -> 12.0
History:
  17 % 5 = 2.0
  17 // 5 = 3.0
  3 * 4 = 12.0
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
