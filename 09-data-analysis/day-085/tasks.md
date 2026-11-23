# Day 085 — Practice Tasks: NumPy Arrays and Operations

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Filter temperatures

**Problem statement:** Given temperatures `[22.5, 35.1, 28.4, 40.2, 18.9, 31.0]`, print values above 30, their count, and the array with values above 35 replaced by 35 (`np.where` or `np.clip`).

**Input requirements:** No user input required.

**Expected behavior:** `[35.1, 40.2, 31.0]`, count 3, capped array.

**Expected output:**

```text
[35.1 40.2 31. ] 3
[22.5 35.  28.4 35.  18.9 31. ]
```

## Task 2 — Medium: Matrix statistics

**Problem statement:** Create a 3×4 array of request counts (rows = services api/web/worker, columns = 4 quarters). Print totals per service, totals per quarter, and the service with the highest total.

**Input requirements:** No user input required.

**Expected behavior:** Per-row and per-column totals and the top service.

**Expected output:**

```text
per service: {np.str_('api'): 5850, np.str_('web'): 3950, np.str_('worker'): 1700}
per quarter: [2500, 2720, 2980, 3300]
top service: api
```

## Task 3 — Practical Challenge: Anomaly detection with z-scores

**Problem statement:** Using `default_rng(3)`, generate 50 response times from a normal distribution (mean 200, std 20) and inject spikes of 450 at positions 10 and 37. Compute z-scores `(x - mean) / std` and print the indexes and values where |z| > 3.

**Input requirements:** No user input required.

**Expected behavior:** Indexes 10 and 37 detected.

**Expected output:**

```text
index 10: 450.0 ms (z=4.5)
index 37: 450.0 ms (z=4.5)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
