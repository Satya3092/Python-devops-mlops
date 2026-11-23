# Day 089 — Data Filtering, Sorting, and Grouping

[⬅ Day 088](../../09-data-analysis/day-088/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 090 ➡](../../09-data-analysis/day-090/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Filter rows with boolean conditions, `isin`, `between`, string methods and `query`
- Sort by one or more columns
- Aggregate with `groupby`/`agg`, `pivot_table` and `crosstab`

## 2. Topic Explanation

These three operations answer most business and operations questions.

**Filtering** (like SQL `WHERE`):
- `df[df["cpu"] > 80]`
- `df[(df["env"] == "prod") & (df["cpu"] > 80)]` — use `&`, `|`, `~` with parentheses
- `df[df["region"].isin(["us-east-1", "eu-west-1"])]`
- `df[df["cpu"].between(50, 80)]`
- `df[df["host"].str.startswith("web")]` — `.str` gives string methods on a column
- `df.query("env == 'prod' and cpu > 80")` — readable alternative

**Sorting** (`ORDER BY`): `df.sort_values(["env", "cpu"], ascending=[True, False])`, `nlargest`, `nsmallest`.

**Grouping** (`GROUP BY`) — *split → apply → combine*:
```python
df.groupby("env")["cpu"].mean()
df.groupby("env").agg(servers=("host", "count"), avg_cpu=("cpu", "mean"), max_disk=("disk", "max"))
```
- `pivot_table(index=..., columns=..., values=..., aggfunc=...)` — Excel pivot tables.
- `pd.crosstab(a, b)` — counts of combinations.
- Group by time with `df.set_index("timestamp").resample("1h").mean()` or `df.groupby(df["timestamp"].dt.hour)`.

> Examples read the sample datasets in [`datasets/`](../../datasets/) using the relative path `../../datasets/...`, so run them from inside this day's folder. Install the libraries with `pip install numpy pandas matplotlib openpyxl`.

## 3. Syntax

```python
df[(df["a"] > 1) & (df["b"] == "x")]
df[df["col"].isin([...])]; df.query("a > 1 and b == 'x'")
df.sort_values(["a", "b"], ascending=[True, False])
df.groupby("key").agg(new_name=("col", "mean"))
df.pivot_table(index="r", columns="c", values="v", aggfunc="sum", fill_value=0)
```

| Part | Meaning |
|---|---|
| `boolean filter` | Keep rows where the condition is True. |
| `isin / between / .str` | Membership, ranges and string tests on columns. |
| `sort_values` | Sort by one or more columns. |
| `groupby + agg` | Named aggregations per group. |
| `pivot_table` | Rows × columns summary table. |

## 4. Example 1 — Basic Example: Filtering and sorting servers

```python
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")
cols = ["hostname", "environment", "region", "cpu_usage", "disk_usage", "status"]

print("Prod servers with CPU > 60:")
print(df[(df["environment"] == "prod") & (df["cpu_usage"] > 60)][cols])

print("\nIn Mumbai or Ireland regions, disk between 60 and 90:")
print(df[df["region"].isin(["ap-south-1", "eu-west-1"]) & df["disk_usage"].between(60, 90)][cols])

print("\nUnhealthy servers whose hostname contains '-web-1' (query + str):")
unhealthy = df.query("status != 'healthy'")
print(unhealthy[unhealthy["hostname"].str.contains("-web-1")][["hostname", "status"]])

print("\nTop 5 by CPU, ties broken by disk:")
print(df.sort_values(["cpu_usage", "disk_usage"], ascending=[False, False]).head(5)[cols])
```

## 5. Example 2 — Practical Example: Grouping: per-environment stats, pivots and time windows

```python
import pandas as pd

pd.set_option("display.width", 120)
servers = pd.read_csv("../../datasets/servers.csv")

summary = servers.groupby("environment").agg(
    servers=("hostname", "count"),
    avg_cpu=("cpu_usage", "mean"),
    max_disk=("disk_usage", "max"),
    total_memory_gb=("memory_gb", "sum"),
).round(1).sort_values("avg_cpu", ascending=False)
print(summary)

print("\nStatus by environment (crosstab):")
print(pd.crosstab(servers["environment"], servers["status"]))

sales = pd.read_csv("../../datasets/sales.csv", parse_dates=["date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
pivot = sales.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum", fill_value=0)
print("\nRevenue pivot (region x product):")
print(pivot)
print("Best region:", pivot.sum(axis=1).idxmax(), "| best product:", pivot.sum(axis=0).idxmax())

metrics = pd.read_csv("../../datasets/server_metrics.csv", parse_dates=["timestamp"])
hourly = metrics.set_index("timestamp").resample("1h")["cpu"].mean().round(1)
print("\nFleet average CPU per hour:")
print(hourly)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Each condition is wrapped in parentheses and combined with `&`.
- `isin` matches a list of regions; `between` is inclusive on both ends.
- `.str.contains` applies a string test to every hostname; `query()` filters with a readable expression.
- `sort_values` with two columns and two directions breaks ties.

**Example 2**
- `groupby(...).agg(name=(column, function))` produces clearly named result columns — like `SELECT env, COUNT(*), AVG(cpu) ... GROUP BY env`.
- `crosstab` counts combinations of two categorical columns.
- `pivot_table` builds an Excel-style region × product revenue table; summing rows/columns finds the best region and product.
- `resample("1h")` groups a time-indexed DataFrame into hourly buckets — the basis of every metrics dashboard.

## 7. Expected Output

**Example 1:**

```text
Prod servers with CPU > 60:
       hostname environment      region  cpu_usage  disk_usage   status
5   prod-web-06        prod  ap-south-1         64          82  warning
14  prod-web-15        prod   eu-west-1         78          52  warning
17  prod-web-18        prod  ap-south-1         70          40  healthy

In Mumbai or Ireland regions, disk between 60 and 90:
          hostname environment      region  cpu_usage  disk_usage    status
1       dev-web-02         dev  ap-south-1         84          72   warning
2      prod-web-03        prod   eu-west-1         53          75  critical
5      prod-web-06        prod  ap-south-1         64          82   warning
9   staging-web-10     staging  ap-south-1         95          88  critical
18  staging-web-19     staging   eu-west-1         45          84   warning

Unhealthy servers whose hostname contains '-web-1' (query + str):
          hostname    status
9   staging-web-10  critical
10      dev-web-11   warning
12  staging-web-13  critical
13      dev-web-14   warning
14     prod-web-15   warning
16      dev-web-17  critical
18  staging-web-19   warning

Top 5 by CPU, ties broken by disk:
          hostname environment      region  cpu_usage  disk_usage    status
9   staging-web-10     staging  ap-south-1         95          88  critical
16      dev-web-17         dev   us-west-2         92          28  critical
12  staging-web-13     staging   us-west-2         90          45  critical
1       dev-web-02         dev  ap-south-1         84          72   warning
14     prod-web-15        prod   eu-west-1         78          52   warning
```

**Example 2:**

```text
             servers  avg_cpu  max_disk  total_memory_gb
environment                                             
staging            7     59.4        88              136
dev                7     54.0        82               88
prod               6     49.0        82               92

Status by environment (crosstab):
status       critical  healthy  warning
environment                            
dev                 1        2        4
prod                1        2        3
staging             2        2        3

Revenue pivot (region x product):
product  Keyboard  Laptop  Monitor  Mouse
region                                   
East         3330   35100     6820   1225
North        2070   51300    17160    150
South          90   39600    14740   1400
West         3870   27000     5280   1400
Best region: North | best product: Laptop

Fleet average CPU per hour:
timestamp
2026-11-20 09:00:00    48.6
2026-11-20 10:00:00    55.2
2026-11-20 11:00:00    59.2
2026-11-20 12:00:00    57.6
2026-11-20 13:00:00    54.3
Freq: h, Name: cpu, dtype: float64
```

> ℹ️ Output was produced with pandas 3.x. With pandas 2.x, text columns show the dtype `object` instead of `str`; everything else is the same.

## 8. Common Mistakes

**1. Using `and`/`or` in filters**

`df[df.a > 1 and df.b < 2]` raises `ValueError`. Use `&`/`|` with parentheses.

**2. Forgetting `as_index=False` / `reset_index()`**

After `groupby`, the group keys become the index. Reset it before exporting or merging.

**3. Grouping text-typed numbers**

If `cpu` is a string column, `mean()` fails or concatenates. Fix dtypes first.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Filter houses:** From `house_prices.csv`, show houses with 3+ bedrooms, less than 10 km from the centre and priced below 400,000, sorted by price. Print how many there are and the 5 cheapest.
- **Task 2 (Medium) — Sales analysis:** Using `sales.csv`, compute revenue, then print total revenue per region (sorted desc), average units per product, and the month (from `date`) with the highest revenue.
- **Task 3 (Practical Challenge) — Server failure insights:** Load `server_failures.csv`. Group by `error_count` bins (`0-2`, `3-5`, `6+` using `pd.cut`) and print the failure rate (%) and count per bin. Then print a pivot of failure rate by CPU band (`<50`, `50-80`, `80+`) × memory band (same bands). What do you notice?

## 10. DevOps/MLOps Connection

- **DevOps / SRE:** "which services break most?", "error rate per hour?", "MTTR per team?" are groupby questions; DORA metrics come from grouping deployment data.
- **Cloud:** cost per service/team/month is a pivot table over billing data.
- **ML / MLOps:** grouping reveals which features relate to the label (like the failure pivot) — exactly the intuition a model will learn; it also powers drift monitoring per segment.

## 11. Interview Questions

**Q1. How do you filter a DataFrame with multiple conditions?**

<details><summary>Show answer</summary>

Combine boolean Series with `&`, `|`, `~`, wrapping each condition in parentheses, or use `df.query()`.

</details>

**Q2. What does `groupby` do conceptually?**

<details><summary>Show answer</summary>

Split the data into groups by key, apply an aggregation/transformation to each group, and combine the results.

</details>

**Q3. What is the difference between `pivot_table` and `pivot`?**

<details><summary>Show answer</summary>

`pivot` only reshapes and fails on duplicate entries; `pivot_table` aggregates duplicates with a function (mean by default) and supports fill values/margins.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 89 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 088](../../09-data-analysis/day-088/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 090 ➡](../../09-data-analysis/day-090/README.md)
