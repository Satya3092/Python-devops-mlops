# Day 086 — Pandas Introduction

[⬅ Day 085](../../09-data-analysis/day-085/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 087 ➡](../../09-data-analysis/day-087/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain what pandas is and how it relates to NumPy, Excel and SQL
- Load a CSV into a DataFrame and inspect it (`head`, `info`, `describe`, `shape`)
- Select columns and compute quick summaries

## 2. Topic Explanation

**pandas** is Python's spreadsheet + SQL engine. It gives you the **DataFrame**: a table with labelled rows and columns, where each column has its own type.

```python
import pandas as pd                  # universal alias
df = pd.read_csv("servers.csv")
df.head()
```

Why pandas?
- Read/write CSV, Excel, JSON, SQL, Parquet in one line.
- Filter, sort, group, join and aggregate millions of rows quickly (it uses NumPy underneath).
- Handle missing values and dates properly.

First things to do with any dataset (**exploratory data analysis**, EDA):

| Command | Shows |
|---|---|
| `df.shape` | (rows, columns) |
| `df.head(n)` / `df.tail(n)` | first / last rows |
| `df.columns` | column names |
| `df.dtypes` / `df.info()` | column types and non-null counts |
| `df.describe()` | statistics for numeric columns |
| `df["col"].value_counts()` | frequency of categories |
| `df["col"].unique()` / `.nunique()` | distinct values |

Analogy: if NumPy is a calculator for numbers, pandas is Excel you can script and version-control.

> Examples read the sample datasets in [`datasets/`](../../datasets/) using the relative path `../../datasets/...`, so run them from inside this day's folder. Install the libraries with `pip install numpy pandas matplotlib openpyxl`.

## 3. Syntax

```python
import pandas as pd
df = pd.read_csv("file.csv")
df.shape; df.head(); df.info(); df.describe()
df["column"]                # one column (Series)
df[["col1", "col2"]]        # several columns (DataFrame)
df["column"].value_counts()
```

| Part | Meaning |
|---|---|
| `pd.read_csv` | Load a CSV file into a DataFrame. |
| `head / tail` | Preview rows. |
| `info / dtypes` | Column types and missing values. |
| `describe` | count, mean, std, min, quartiles, max. |
| `df["col"]` | Select a column → Series. |

## 4. Example 1 — Basic Example: Load and inspect a dataset

```python
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")

print("shape:", df.shape)
print("columns:", list(df.columns))
print(df.head())
print()
df.info()
```

## 5. Example 2 — Practical Example: First questions answered with pandas

```python
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")

print(df.describe().round(1))
print()
print("Servers per environment:")
print(df["environment"].value_counts())
print()
print("Status counts:", df["status"].value_counts().to_dict())
print("Regions used:", sorted(df["region"].unique()), "| distinct:", df["region"].nunique())
print("Average CPU usage:", round(df["cpu_usage"].mean(), 1))
print("Total memory (GB):", df["memory_gb"].sum())
print()
print(df[["hostname", "cpu_usage", "status"]].head(3))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `pd.read_csv` reads the file, detects the header and infers types (ints for numbers, text for strings).
- `head()` shows the first 5 rows with an index (0, 1, 2...).
- `info()` lists each column's type and non-null count — the fastest way to spot missing data.

**Example 2**
- `describe()` gives count/mean/std/min/quartiles/max for every numeric column in one call.
- `value_counts()` counts categories (like `sort | uniq -c`).
- `unique()` / `nunique()` show distinct values.
- `df[["hostname", "cpu_usage", "status"]]` (double brackets) selects several columns.

## 7. Expected Output

**Example 1:**

```text
shape: (20, 9)
columns: ['hostname', 'environment', 'region', 'cpu_cores', 'memory_gb', 'cpu_usage', 'memory_usage', 'disk_usage', 'status']
         hostname environment      region  ...  memory_usage  disk_usage    status
0  staging-web-01     staging   us-west-2  ...            78          68   warning
1      dev-web-02         dev  ap-south-1  ...            26          72   warning
2     prod-web-03        prod   eu-west-1  ...            93          75  critical
3  staging-web-04     staging   us-east-1  ...            58          25   warning
4      dev-web-05         dev   us-west-2  ...            47          29   healthy

[5 rows x 9 columns]

<class 'pandas.DataFrame'>
RangeIndex: 20 entries, 0 to 19
Data columns (total 9 columns):
 #   Column        Non-Null Count  Dtype
---  ------        --------------  -----
 0   hostname      20 non-null     str  
 1   environment   20 non-null     str  
 2   region        20 non-null     str  
 3   cpu_cores     20 non-null     int64
 4   memory_gb     20 non-null     int64
 5   cpu_usage     20 non-null     int64
 6   memory_usage  20 non-null     int64
 7   disk_usage    20 non-null     int64
 8   status        20 non-null     str  
dtypes: int64(5), str(4)
memory usage: 1.5 KB
```

**Example 2:**

```text
       cpu_cores  memory_gb  cpu_usage  memory_usage  disk_usage
count       20.0       20.0       20.0          20.0        20.0
mean         8.5       15.8       54.4          56.6        54.2
std          5.5       10.5       28.2          21.4        22.9
min          2.0        4.0        9.0          26.0        22.0
25%          4.0        8.0       34.0          37.0        32.0
50%          8.0       16.0       52.0          52.5        48.5
75%         16.0       20.0       78.0          76.5        72.8
max         16.0       32.0       95.0          93.0        88.0

Servers per environment:
environment
staging    7
dev        7
prod       6
Name: count, dtype: int64

Status counts: {'warning': 10, 'healthy': 6, 'critical': 4}
Regions used: ['ap-south-1', 'eu-west-1', 'us-east-1', 'us-west-2'] | distinct: 4
Average CPU usage: 54.4
Total memory (GB): 316

         hostname  cpu_usage    status
0  staging-web-01         13   warning
1      dev-web-02         84   warning
2     prod-web-03         53  critical
```

> ℹ️ Output was produced with pandas 3.x. With pandas 2.x, text columns show the dtype `object` instead of `str`; everything else is the same.

## 8. Common Mistakes

**1. Single vs double brackets**

`df["a", "b"]` raises `KeyError`. Use `df[["a", "b"]]` for multiple columns.

**2. Wrong path**

`FileNotFoundError` usually means you're running from a different folder. Check `Path.cwd()`.

**3. Skipping `info()`**

Columns you think are numbers may be text (e.g. `"85%"`). Always check dtypes first.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Inspect house prices:** Load `../../datasets/house_prices.csv` and print its shape, column names, the first 3 rows and the data types.
- **Task 2 (Medium) — Quick statistics:** For the house dataset print the mean, median and max `price`, and the number of houses per bedroom count (sorted by bedrooms).
- **Task 3 (Practical Challenge) — Server report:** From `servers.csv`, print: number of critical servers, the hostname with the highest CPU usage, the average disk usage per environment (use `df[df['environment'] == env]` in a loop) and the percentage of servers that are healthy.

## 10. DevOps/MLOps Connection

- **DevOps:** analyse inventory exports, incident timelines, deployment frequency (DORA metrics) and on-call load.
- **Cloud:** AWS Cost & Usage Reports are huge CSV/Parquet files — pandas summarises them in seconds.
- **Data engineering:** pandas is the go-to tool for small/medium ETL jobs and data validation.
- **ML / MLOps:** almost every ML project starts with `pd.read_csv` and EDA before training.

## 11. Interview Questions

**Q1. What is a DataFrame?**

<details><summary>Show answer</summary>

A 2-D labelled table in pandas: rows with an index and named columns, each column a typed Series.

</details>

**Q2. What are the first commands you run on a new dataset?**

<details><summary>Show answer</summary>

`shape`, `head()`, `info()`/`dtypes`, `describe()`, `isna().sum()`, and `value_counts()` on key categorical columns.

</details>

**Q3. How is pandas related to NumPy?**

<details><summary>Show answer</summary>

pandas is built on NumPy; columns store data in NumPy (or Arrow) arrays and use vectorised operations.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 86 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 085](../../09-data-analysis/day-085/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 087 ➡](../../09-data-analysis/day-087/README.md)
