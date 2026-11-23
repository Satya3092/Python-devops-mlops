# Day 085 — NumPy Arrays and Operations

[⬅ Day 084](../../09-data-analysis/day-084/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 086 ➡](../../09-data-analysis/day-086/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Index, slice and filter arrays with boolean masks
- Use vectorised arithmetic, aggregations along axes and broadcasting
- Reshape arrays and apply conditional logic with `np.where`

## 2. Topic Explanation

**Indexing & slicing** work like lists, plus multi-dimensional forms:
- `a[0]`, `a[-1]`, `a[1:4]`
- 2-D: `m[row, col]`, `m[0, :]` (first row), `m[:, 1]` (second column)

**Boolean masks** — the superpower for filtering:
```python
cpu = np.array([45, 92, 71, 98])
cpu > 90            # array([False,  True, False,  True])
cpu[cpu > 90]       # array([92, 98])
```
Combine masks with `&` (and), `|` (or), `~` (not) and **parentheses**: `cpu[(cpu > 50) & (cpu < 95)]`.

**Aggregations:** `sum`, `mean`, `min`, `max`, `std`, `argmax`, `percentile`. On 2-D arrays choose an **axis**: `axis=0` → down the rows (per column), `axis=1` → across columns (per row).

**Broadcasting:** NumPy stretches smaller arrays to match larger ones: `matrix - matrix.mean(axis=0)` subtracts each column's mean from every row. This is how feature scaling works in ML.

**Reshape:** `a.reshape(4, 6)` changes the shape without changing data (sizes must match; `-1` means "work it out").

**`np.where(condition, a, b)`** — vectorised if/else.

> Install NumPy with `pip install numpy`.

## 3. Syntax

```python
m[row, col]   m[:, col]   m[row, :]
a[a > 90]     a[(a > 50) & (a < 95)]
m.mean(axis=0)    m.max(axis=1)
m - m.mean(axis=0)            # broadcasting
a.reshape(rows, -1)
np.where(a > 90, "ALERT", "ok")
```

| Part | Meaning |
|---|---|
| `m[:, c]` | All rows, column c. |
| `boolean mask` | Array of True/False selecting elements. |
| `& \| ~` | Element-wise and/or/not (use parentheses!). |
| `axis=0 / axis=1` | Aggregate per column / per row. |
| `np.where` | Vectorised conditional choice. |

## 4. Example 1 — Basic Example: Indexing, masks and aggregations

```python
import numpy as np

cpu = np.array([45, 92, 71, 98, 33, 87])
print("first, last:", cpu[0], cpu[-1], "| slice 1:4:", cpu[1:4])
print("mask cpu > 85:", cpu > 85)
print("values > 85:", cpu[cpu > 85])
print("between 40 and 90:", cpu[(cpu >= 40) & (cpu <= 90)])
print("count > 85:", (cpu > 85).sum(), "| any > 95?", (cpu > 95).any(), "| all > 30?", (cpu > 30).all())
print("labels:", np.where(cpu > 85, "ALERT", "ok"))
print("sum/mean/std:", cpu.sum(), round(cpu.mean(), 2), round(cpu.std(), 2))
print("index of max:", cpu.argmax())
print("reshape to 2x3:\n", cpu.reshape(2, 3))
```

## 5. Example 2 — Practical Example: A metrics matrix: servers × hours

```python
import numpy as np

servers = np.array(["web-01", "web-02", "db-01", "cache-01"])
hours = np.array(["09:00", "10:00", "11:00", "12:00", "13:00"])
# rows = servers, columns = hours (CPU %)
cpu = np.array([
    [35, 42, 55, 61, 48],
    [70, 88, 93, 97, 85],
    [50, 52, 58, 60, 57],
    [20, 22, 19, 25, 21],
])
print("shape:", cpu.shape)
print("db-01 at 11:00:", cpu[2, 2])
print("all servers at 12:00:", dict(zip(servers, cpu[:, 3])))

print("average per server:", dict(zip(servers, cpu.mean(axis=1).round(1))))
print("peak per hour     :", dict(zip(hours, cpu.max(axis=0))))
busiest_hour = hours[cpu.sum(axis=0).argmax()]
print("busiest hour across the fleet:", busiest_hour)

hot = cpu > 90
print("readings over 90%:", hot.sum(), "on", servers[hot.any(axis=1)])

# Broadcasting: how far is each reading from that server's own average?
deviation = cpu - cpu.mean(axis=1, keepdims=True)
print("deviation from own average (web-02):", deviation[1].round(1))

# Min-max scaling to 0..1 per server (a common ML preprocessing step)
mins = cpu.min(axis=1, keepdims=True)
maxs = cpu.max(axis=1, keepdims=True)
print("scaled cache-01:", ((cpu - mins) / (maxs - mins))[3].round(2))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `cpu > 85` produces a boolean mask; `cpu[mask]` keeps matching values.
- Combine conditions with `&` and wrap each in parentheses.
- Booleans sum as 1/0, so `(cpu > 85).sum()` counts matches. `any`/`all` answer yes/no questions.
- `np.where` labels every element at once.

**Example 2**
- The 2-D array has servers as rows and hours as columns; `cpu[2, 2]` and `cpu[:, 3]` pick a cell and a column.
- `mean(axis=1)` = average per **row** (server); `max(axis=0)` = peak per **column** (hour).
- `hot.any(axis=1)` finds servers with at least one reading over 90 %, then indexes the `servers` array with that mask.
- Broadcasting: `cpu - cpu.mean(axis=1, keepdims=True)` subtracts each row's mean from that row. `keepdims=True` keeps the shape `(4, 1)` so it lines up.
- Min-max scaling uses the same idea — this exact maths appears again in ML preprocessing.

## 7. Expected Output

**Example 1:**

```text
first, last: 45 87 | slice 1:4: [92 71 98]
mask cpu > 85: [False  True False  True False  True]
values > 85: [92 98 87]
between 40 and 90: [45 71 87]
count > 85: 3 | any > 95? True | all > 30? True
labels: ['ok' 'ALERT' 'ok' 'ALERT' 'ok' 'ALERT']
sum/mean/std: 426 71.0 24.31
index of max: 3
reshape to 2x3:
 [[45 92 71]
 [98 33 87]]
```

**Example 2:**

```text
shape: (4, 5)
db-01 at 11:00: 58
all servers at 12:00: {np.str_('web-01'): np.int64(61), np.str_('web-02'): np.int64(97), np.str_('db-01'): np.int64(60), np.str_('cache-01'): np.int64(25)}
average per server: {np.str_('web-01'): np.float64(48.2), np.str_('web-02'): np.float64(86.6), np.str_('db-01'): np.float64(55.4), np.str_('cache-01'): np.float64(21.4)}
peak per hour     : {np.str_('09:00'): np.int64(70), np.str_('10:00'): np.int64(88), np.str_('11:00'): np.int64(93), np.str_('12:00'): np.int64(97), np.str_('13:00'): np.int64(85)}
busiest hour across the fleet: 12:00
readings over 90%: 2 on ['web-02']
deviation from own average (web-02): [-16.6   1.4   6.4  10.4  -1.6]
scaled cache-01: [0.17 0.5  0.   1.   0.33]
```

## 8. Common Mistakes

**1. Using `and`/`or` with arrays**

`(a > 1) and (a < 5)` raises `ValueError: truth value of an array is ambiguous`. Use `&`, `|` with parentheses.

**2. Mixing up axes**

`axis=0` collapses rows (result per column); `axis=1` collapses columns (result per row). Check the result's shape.

**3. Views vs copies**

Slices are **views**: modifying `b = a[0:3]` changes `a`. Use `.copy()` when you need independent data.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Filter temperatures:** Given temperatures `[22.5, 35.1, 28.4, 40.2, 18.9, 31.0]`, print values above 30, their count, and the array with values above 35 replaced by 35 (`np.where` or `np.clip`).
- **Task 2 (Medium) — Matrix statistics:** Create a 3×4 array of request counts (rows = services api/web/worker, columns = 4 quarters). Print totals per service, totals per quarter, and the service with the highest total.
- **Task 3 (Practical Challenge) — Anomaly detection with z-scores:** Using `default_rng(3)`, generate 50 response times from a normal distribution (mean 200, std 20) and inject spikes of 450 at positions 10 and 37. Compute z-scores `(x - mean) / std` and print the indexes and values where |z| > 3.

## 10. DevOps/MLOps Connection

- **DevOps / SRE:** detect anomalies (z-scores), compute per-host and per-hour aggregates from metric matrices, find the worst offenders quickly.
- **Data engineering:** vectorised transformations on large numeric data.
- **ML / MLOps:** boolean masks split data, broadcasting implements feature scaling, `reshape` prepares input shapes for models (`model.predict(x.reshape(1, -1))`).

## 11. Interview Questions

**Q1. What is broadcasting in NumPy?**

<details><summary>Show answer</summary>

Automatic expansion of arrays with compatible shapes so element-wise operations work without copying data, e.g. subtracting a per-column mean from a matrix.

</details>

**Q2. How do you select elements of an array that satisfy two conditions?**

<details><summary>Show answer</summary>

Use a boolean mask with `&`/`|` and parentheses: `a[(a > 10) & (a < 20)]`.

</details>

**Q3. What does `axis=0` mean in `m.sum(axis=0)`?**

<details><summary>Show answer</summary>

Sum along the first axis (down the rows), producing one result per column.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 85 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 084](../../09-data-analysis/day-084/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 086 ➡](../../09-data-analysis/day-086/README.md)
