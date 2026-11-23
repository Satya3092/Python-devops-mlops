# Day 089 — Practice Tasks: Data Filtering, Sorting, and Grouping

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Filter houses

**Problem statement:** From `house_prices.csv`, show houses with 3+ bedrooms, less than 10 km from the centre and priced below 400,000, sorted by price. Print how many there are and the 5 cheapest.

**Input requirements:** No user input required.

**Expected behavior:** A count and 5 rows.

**Expected output:**

```text
matches: 14
     size_sqft  bedrooms  age_years  distance_km   price
181       1231         3          6          8.1  217400
126       1500         3         31          6.9  237700
171       1376         3         13          6.2  272100
117       1432         3         20          5.7  286000
51        1794         4         29          9.5  290900
```

## Task 2 — Medium: Sales analysis

**Problem statement:** Using `sales.csv`, compute revenue, then print total revenue per region (sorted desc), average units per product, and the month (from `date`) with the highest revenue.

**Input requirements:** No user input required.

**Expected behavior:** Region totals, product averages and the best month.

**Expected output:**

```text
region
North    70680
South    55830
East     46475
West     37550
Name: revenue, dtype: int64
product
Keyboard    17.3
Laptop      13.1
Monitor     14.3
Mouse       18.6
Name: units, dtype: float64
Best month: 2026-06 with 32805
```

## Task 3 — Practical Challenge: Server failure insights

**Problem statement:** Load `server_failures.csv`. Group by `error_count` bins (`0-2`, `3-5`, `6+` using `pd.cut`) and print the failure rate (%) and count per bin. Then print a pivot of failure rate by CPU band (`<50`, `50-80`, `80+`) × memory band (same bands). What do you notice?

**Input requirements:** No user input required.

**Expected behavior:** Failure rate increases with errors and with high CPU+memory.

**Expected output:**

```text
            failure_rate  servers
error_band                       
0-2                 12.2      181
3-5                 20.0      180
6+                  41.0       39
mem_band   <50  50-80   80+
cpu_band                   
<50        1.2    1.5  20.4
50-80      2.0   23.5  59.4
80+       20.5   42.4  75.0
Insight: failures concentrate where errors are frequent and CPU and memory are both high.
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
