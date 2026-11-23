# Day 087 — Pandas Series and DataFrames

[⬅ Day 086](../../09-data-analysis/day-086/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 088 ➡](../../09-data-analysis/day-088/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create Series and DataFrames from lists and dictionaries
- Select data with `loc` (labels) and `iloc` (positions)
- Add, modify and drop columns; apply vectorised and conditional transformations

## 2. Topic Explanation

**Series** = one labelled column (values + index).
**DataFrame** = a table of Series sharing the same index.

```python
s = pd.Series([45, 72, 91], index=["web-01", "web-02", "db-01"], name="cpu")
df = pd.DataFrame({"host": ["web-01", "db-01"], "cpu": [45, 91]})
```

**Selecting data**

| Syntax | Selects |
|---|---|
| `df["cpu"]` | a column |
| `df.loc[row_label, col_label]` | by **labels** (slices include the end!) |
| `df.iloc[row_pos, col_pos]` | by **positions** (like lists) |
| `df.loc[df["cpu"] > 80, ["host", "cpu"]]` | rows by condition + chosen columns |
| `df.set_index("host")` | use a column as the row labels |

**Changing data**
- New column: `df["cpu_ratio"] = df["cpu"] / 100` (vectorised)
- Conditional column: `np.where(...)` or `pd.cut(...)` for bins
- `df.assign(...)` adds columns and returns a new DataFrame (chain-friendly)
- `df.rename(columns={...})`, `df.drop(columns=[...])`
- `.map(dict)` translates values; `.apply(func)` runs a function per value/row (slower — use vectorised operations when possible)

> Examples read the sample datasets in [`datasets/`](../../datasets/) using the relative path `../../datasets/...`, so run them from inside this day's folder. Install the libraries with `pip install numpy pandas matplotlib openpyxl`.

## 3. Syntax

```python
pd.Series(values, index=labels, name="x")
pd.DataFrame({"col": [..], "col2": [..]})
df.loc[label, "col"]      df.iloc[0, 1]
df.loc[df["cpu"] > 80, ["host", "cpu"]]
df["new"] = df["a"] * 2
df.drop(columns=["tmp"]); df.rename(columns={"a": "b"})
```

| Part | Meaning |
|---|---|
| `Series` | 1-D labelled array. |
| `DataFrame` | 2-D table of Series. |
| `loc` | Label-based selection (end of slice included). |
| `iloc` | Position-based selection (end excluded). |
| `vectorised column ops` | Operate on whole columns at once. |

## 4. Example 1 — Basic Example: Series and DataFrame basics

```python
import pandas as pd

cpu = pd.Series([45, 72, 91, 38], index=["web-01", "web-02", "db-01", "cache-01"], name="cpu")
print(cpu)
print("db-01:", cpu["db-01"], "| over 70:", cpu[cpu > 70].to_dict())
print("mean:", cpu.mean())

df = pd.DataFrame({
    "host": ["web-01", "web-02", "db-01", "cache-01"],
    "env": ["prod", "prod", "prod", "dev"],
    "cpu": [45, 72, 91, 38],
    "memory_gb": [8, 8, 64, 4],
})
print(df)
print("iloc[0, 0]:", df.iloc[0, 0], "| first two rows:\n", df.iloc[:2])

indexed = df.set_index("host")
print("loc['db-01', 'cpu']:", indexed.loc["db-01", "cpu"])
print(indexed.loc["web-02":"db-01", ["env", "cpu"]])     # label slice includes db-01
```

## 5. Example 2 — Practical Example: Enriching a server table with new columns

```python
import numpy as np
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")

df["memory_per_core"] = df["memory_gb"] / df["cpu_cores"]
df["max_usage"] = df[["cpu_usage", "memory_usage", "disk_usage"]].max(axis=1)
df["needs_attention"] = np.where(df["max_usage"] >= 75, "yes", "no")
df["load_band"] = pd.cut(df["cpu_usage"], bins=[0, 40, 75, 100], labels=["low", "medium", "high"])
df["tier"] = df["environment"].map({"prod": 1, "staging": 2, "dev": 3})
df = df.rename(columns={"hostname": "host"}).drop(columns=["region"])

print(df.loc[df["needs_attention"] == "yes", ["host", "environment", "max_usage", "load_band", "tier"]].head(6))
print()
print("Load bands:", df["load_band"].value_counts().sort_index().to_dict())
print("Columns now:", list(df.columns))

summary = df.assign(cost_per_month=df["cpu_cores"] * 15 + df["memory_gb"] * 4)
print("Estimated monthly cost (top 3):")
print(summary.nlargest(3, "cost_per_month")[["host", "cpu_cores", "memory_gb", "cost_per_month"]])
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- A `Series` has values and an index of labels; boolean filtering works like NumPy.
- `iloc` uses positions; after `set_index("host")`, `loc` uses hostnames.
- `loc["web-02":"db-01"]` **includes** both ends — unlike Python slices.

**Example 2**
- Arithmetic between columns creates new columns for every row at once.
- `.max(axis=1)` takes the row-wise maximum of three columns.
- `np.where` creates a yes/no flag; `pd.cut` puts numbers into labelled bins (low/medium/high).
- `.map(dict)` translates categories into numbers — very common when preparing data for ML.
- `rename` / `drop` tidy the table; `assign` adds a column in a chain; `nlargest` picks the top rows.

## 7. Expected Output

**Example 1:**

```text
web-01      45
web-02      72
db-01       91
cache-01    38
Name: cpu, dtype: int64
db-01: 91 | over 70: {'web-02': 72, 'db-01': 91}
mean: 61.5
       host   env  cpu  memory_gb
0    web-01  prod   45          8
1    web-02  prod   72          8
2     db-01  prod   91         64
3  cache-01   dev   38          4
iloc[0, 0]: web-01 | first two rows:
      host   env  cpu  memory_gb
0  web-01  prod   45          8
1  web-02  prod   72          8
loc['db-01', 'cpu']: 91
         env  cpu
host             
web-02  prod   72
db-01   prod   91
```

**Example 2:**

```text
             host environment  max_usage load_band  tier
0  staging-web-01     staging         78       low     2
1      dev-web-02         dev         84      high     3
2     prod-web-03        prod         93    medium     1
3  staging-web-04     staging         78      high     2
5     prod-web-06        prod         82    medium     1
7      dev-web-08         dev         84       low     3

Load bands: {'low': 6, 'medium': 8, 'high': 6}
Columns now: ['host', 'environment', 'cpu_cores', 'memory_gb', 'cpu_usage', 'memory_usage', 'disk_usage', 'status', 'memory_per_core', 'max_usage', 'needs_attention', 'load_band', 'tier']
Estimated monthly cost (top 3):
           host  cpu_cores  memory_gb  cost_per_month
4    dev-web-05         16         32             368
17  prod-web-18         16         32             368
2   prod-web-03         16         16             304
```

> ℹ️ Output was produced with pandas 3.x. With pandas 2.x, text columns show the dtype `object` instead of `str`; everything else is the same.

## 8. Common Mistakes

**1. Chained assignment**

`df[df.cpu > 80]["flag"] = 1` may modify a temporary copy (SettingWithCopyWarning). Use `df.loc[df.cpu > 80, "flag"] = 1`.

**2. Confusing loc and iloc**

`df.loc[0]` uses the label 0, `df.iloc[0]` the first position. After sorting or filtering they differ!

**3. Using `apply` for simple maths**

`df["a"].apply(lambda x: x * 2)` works but is much slower than `df["a"] * 2`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Build a DataFrame:** Create a DataFrame of 4 employees (name, team, salary) from a dict, print it, then print only the names of the `devops` team using `loc`.
- **Task 2 (Medium) — Derived columns:** Load `house_prices.csv`, add `price_per_sqft` (rounded to 2) and `age_group` (`new` < 10 years, `mid` < 25, `old`), then print the first 5 rows and the average price per sqft per age group.
- **Task 3 (Practical Challenge) — Fleet scorecard:** Load `servers.csv`, add `risk_score = 0.5*cpu + 0.3*memory + 0.2*disk`, rank servers by it (`rank(ascending=False)`), and print the top 5 with host, environment, risk_score (1 decimal) and rank. Then print the mean risk per environment.

## 10. DevOps/MLOps Connection

- **DevOps:** enrich inventory data (cost estimates, risk scores, owners) for capacity and cost reviews.
- **Cloud:** add derived columns to billing data (cost per team = tag mapping with `.map`).
- **ML / MLOps:** **feature engineering** — creating new informative columns (ratios, bins, encodings) is often the biggest accuracy win.

## 11. Interview Questions

**Q1. What is the difference between `loc` and `iloc`?**

<details><summary>Show answer</summary>

`loc` selects by labels (inclusive slices); `iloc` selects by integer positions (exclusive end).

</details>

**Q2. How do you add a column based on a condition?**

<details><summary>Show answer</summary>

`df["flag"] = np.where(df["x"] > 10, "high", "low")` or `df.loc[cond, "flag"] = value`.

</details>

**Q3. What is a Series?**

<details><summary>Show answer</summary>

A one-dimensional labelled array — a single column of a DataFrame with its index.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 87 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 086](../../09-data-analysis/day-086/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 088 ➡](../../09-data-analysis/day-088/README.md)
