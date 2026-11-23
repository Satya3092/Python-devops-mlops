# Day 086 — Practice Tasks: Pandas Introduction

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Inspect house prices

**Problem statement:** Load `../../datasets/house_prices.csv` and print its shape, column names, the first 3 rows and the data types.

**Input requirements:** No user input required.

**Expected behavior:** Shape (200, 5) and dtypes.

**Expected output:**

```text
(200, 5)
['size_sqft', 'bedrooms', 'age_years', 'distance_km', 'price']
   size_sqft  bedrooms  age_years  distance_km   price
0       3241         6          4         17.5  566400
1       1922         4         22         18.1  324000
2        888         1          7         25.6  125000
size_sqft        int64
bedrooms         int64
age_years        int64
distance_km    float64
price            int64
dtype: object
```

## Task 2 — Medium: Quick statistics

**Problem statement:** For the house dataset print the mean, median and max `price`, and the number of houses per bedroom count (sorted by bedrooms).

**Input requirements:** No user input required.

**Expected behavior:** Price statistics and bedroom counts.

**Expected output:**

```text
mean: 323750 median: 319950.0 max: 628200
bedrooms
1    31
2    51
3    47
4    36
5    24
6    11
Name: count, dtype: int64
```

## Task 3 — Practical Challenge: Server report

**Problem statement:** From `servers.csv`, print: number of critical servers, the hostname with the highest CPU usage, the average disk usage per environment (use `df[df['environment'] == env]` in a loop) and the percentage of servers that are healthy.

**Input requirements:** No user input required.

**Expected behavior:** Four answers.

**Expected output:**

```text
Critical servers: 4
Highest CPU: staging-web-10
  avg disk dev: 52.9%
  avg disk prod: 58.0%
  avg disk staging: 52.1%
Healthy: 30%
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
