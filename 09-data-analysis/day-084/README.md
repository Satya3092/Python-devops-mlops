# Day 084 — NumPy Introduction

[⬅ Day 083](../../09-data-analysis/day-083/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 085 ➡](../../09-data-analysis/day-085/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain why NumPy arrays are faster and more convenient than lists for numbers
- Create arrays from lists, ranges and helper functions
- Inspect `shape`, `ndim`, `dtype` and `size`

## 2. Topic Explanation

**NumPy** (Numerical Python) provides the `ndarray`: a fast, fixed-type, multi-dimensional array. Pandas, scikit-learn, TensorFlow and PyTorch are all built on it.

Why not just lists?
- **Speed:** NumPy loops run in optimised C, often 10–100× faster.
- **Vectorisation:** `cpu * 1.1` multiplies **every** element — no Python loop.
- **Memory:** values are stored compactly with one type (`int64`, `float64`...).
- **Maths:** statistics, linear algebra, random numbers built in.

```python
import numpy as np            # the universal alias
cpu = np.array([45, 72, 91, 38])
```

Array attributes:

| Attribute | Example | Meaning |
|---|---|---|
| `shape` | `(3, 4)` | rows, columns |
| `ndim` | `2` | number of dimensions |
| `dtype` | `float64` | element type |
| `size` | `12` | total elements |

Creation helpers: `np.zeros`, `np.ones`, `np.full`, `np.arange` (like range), `np.linspace` (evenly spaced), `np.random.default_rng(seed)` for reproducible random data.

Analogy: a Python list is a shopping bag that can hold anything; a NumPy array is an egg carton — every slot holds the same kind of thing, so it's compact and fast to process.

> Install NumPy with `pip install numpy`.

## 3. Syntax

```python
import numpy as np
a = np.array([1, 2, 3])
m = np.array([[1, 2], [3, 4]])
np.zeros((2, 3)); np.ones(5); np.arange(0, 10, 2); np.linspace(0, 1, 5)
rng = np.random.default_rng(42); rng.integers(0, 100, size=5)
a.shape, a.ndim, a.dtype, a.size
```

| Part | Meaning |
|---|---|
| `np.array(list)` | Create an array from a list (nested list → 2-D). |
| `np.arange / linspace` | Ranges by step / by number of points. |
| `default_rng(seed)` | Reproducible random number generator. |
| `shape / dtype` | Dimensions and element type. |

## 4. Example 1 — Basic Example: Creating and inspecting arrays

```python
import numpy as np

cpu = np.array([45, 72, 91, 38])
print("array:", cpu, "| type:", type(cpu).__name__)
print("shape:", cpu.shape, "ndim:", cpu.ndim, "dtype:", cpu.dtype, "size:", cpu.size)

matrix = np.array([[45, 60, 70], [80, 85, 90]])
print("2-D shape:", matrix.shape)

print("zeros :", np.zeros(3))
print("ones  :", np.ones((2, 2), dtype=int).tolist())
print("full  :", np.full(3, 99))
print("arange:", np.arange(0, 60, 15))
print("linspace:", np.linspace(0, 1, 5))

rng = np.random.default_rng(42)
print("random ints:", rng.integers(0, 100, size=5))

print("list  * 2:", [1, 2, 3] * 2)
print("array * 2:", np.array([1, 2, 3]) * 2)
```

## 5. Example 2 — Practical Example: Why NumPy: speed and vectorised maths on metrics

```python
import time

import numpy as np

rng = np.random.default_rng(7)
latencies = rng.normal(loc=120, scale=25, size=1_000_000).clip(5)   # one million fake latencies (ms)
latency_list = latencies.tolist()

start = time.perf_counter()
slow_list = sum(1 for v in latency_list if v > 200)
list_seconds = time.perf_counter() - start

start = time.perf_counter()
slow_numpy = int((latencies > 200).sum())
numpy_seconds = time.perf_counter() - start

print("Slow requests (list) :", slow_list)
print("Slow requests (numpy):", slow_numpy)
print(f"NumPy was about {list_seconds / numpy_seconds:.0f}x faster")

seconds = latencies / 1000                       # vectorised unit conversion
print("first 3 in seconds:", np.round(seconds[:3], 4))
print(f"mean={latencies.mean():.1f} ms  p95={np.percentile(latencies, 95):.1f} ms  max={latencies.max():.1f} ms")
print("memory: list ~", len(latency_list) * 32 // 1024 // 1024, "MB vs array", latencies.nbytes // 1024 // 1024, "MB")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `np.array` infers `int64` for whole numbers; a nested list becomes a 2-D array with shape `(2, 3)`.
- Helper functions create common arrays quickly; `default_rng(42)` makes "random" numbers repeatable.
- The last two lines show the key difference: `list * 2` **repeats** the list, `array * 2` **multiplies every element**.

**Example 2**
- One million latencies are generated from a normal distribution (mean 120, std 25).
- Counting slow requests with a Python generator vs a NumPy boolean mask: same answer, NumPy is dramatically faster.
- `latencies / 1000` converts all values at once (vectorisation).
- `nbytes` shows the compact memory layout (8 bytes per float64 vs ~32 bytes per Python float object in a list).

## 7. Expected Output

**Example 1:**

```text
array: [45 72 91 38] | type: ndarray
shape: (4,) ndim: 1 dtype: int64 size: 4
2-D shape: (2, 3)
zeros : [0. 0. 0.]
ones  : [[1, 1], [1, 1]]
full  : [99 99 99]
arange: [ 0 15 30 45]
linspace: [0.   0.25 0.5  0.75 1.  ]
random ints: [ 8 77 65 43 43]
list  * 2: [1, 2, 3, 1, 2, 3]
array * 2: [2 4 6]
```

**Example 2:**

```text
Slow requests (list) : 665
Slow requests (numpy): 665
NumPy was about 16x faster
first 3 in seconds: [0.12   0.1275 0.1131]
mean=120.0 ms  p95=161.1 ms  max=243.7 ms
memory: list ~ 30 MB vs array 7 MB
```

> ℹ️ The speed-up factor in Example 2 depends on your computer.

## 8. Common Mistakes

**1. Mixed types**

`np.array([1, "2", 3])` becomes an array of **strings**. Clean/convert data first.

**2. Expecting list behaviour**

`array + array` adds element-wise; `list + list` concatenates. Know which one you have.

**3. Using Python loops over arrays**

Looping element by element throws away NumPy's speed. Use vectorised operations.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Create arrays:** Create an array of the numbers 1–10, a 3×3 array of zeros, and 5 evenly spaced values from 0 to 100. Print each with its shape and dtype.
- **Task 2 (Medium) — Convert units:** Given disk sizes in bytes `[1073741824, 536870912, 2147483648, 268435456]`, convert them to GB with one vectorised operation and print the total.
- **Task 3 (Practical Challenge) — Simulated traffic:** With `default_rng(1)`, simulate 24 hourly request counts as integers between 1000 and 5000. Print the array, the busiest hour (index with `argmax`), the quietest hour and how many hours exceeded 4000 requests.

## 10. DevOps/MLOps Connection

- **DevOps / Monitoring:** fast statistics over millions of metric points or log latencies; percentiles for SLO reports.
- **Data engineering:** NumPy is the engine under pandas.
- **ML / MLOps:** every model input is a NumPy array (`X` with shape `(samples, features)`); predictions come back as arrays.

## 11. Interview Questions

**Q1. Why are NumPy arrays faster than Python lists?**

<details><summary>Show answer</summary>

Homogeneous typed data stored contiguously, operations implemented in C, and vectorisation avoids Python-level loops.

</details>

**Q2. What does `shape` tell you?**

<details><summary>Show answer</summary>

The size of each dimension, e.g. `(rows, columns)` for a 2-D array.

</details>

**Q3. How do you create reproducible random numbers in NumPy?**

<details><summary>Show answer</summary>

Use a seeded generator: `rng = np.random.default_rng(42)`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 84 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 083](../../09-data-analysis/day-083/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 085 ➡](../../09-data-analysis/day-085/README.md)
