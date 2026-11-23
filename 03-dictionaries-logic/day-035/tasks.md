# Day 035 — Practice Tasks: Programming Logic Practice and Mini Project

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Prime numbers

**Problem statement:** Print all prime numbers between 2 and 50 using nested loops and `for...else`.

**Input requirements:** No user input required.

**Expected behavior:** `[2, 3, 5, 7, 11, ..., 47]`.

**Expected output:**

```text
[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47]
```

## Task 2 — Medium: Second largest

**Problem statement:** Find the second-largest unique value in `[45, 91, 23, 91, 78, 60]` without using `sort()`/`sorted()`.

**Input requirements:** No user input required.

**Expected behavior:** Prints `78`.

**Expected output:**

```text
78
```

## Task 3 — Practical Challenge: Extend the inventory report

**Problem statement:** Using the mini-project inventory (copy it), add: (a) the busiest server per environment, (b) a list of owners with the number of servers each owns (empty owner shown as `UNASSIGNED`), and (c) a recommendation line: scale up any env where average CPU util > 50%.

**Input requirements:** No user input required.

**Expected behavior:** Busiest server per env, owner counts and a prod scale-up recommendation.

**Expected output:**

```text
Busiest in prod: web-02 (91%)
Busiest in staging: web-01 (12%)
Busiest in dev: batch-01 (5%)
Servers per owner: {'team-web': 2, 'team-data': 1, 'UNASSIGNED': 1, 'team-ml': 1}
Recommendation: scale up prod (average CPU 66.0%)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
