# Day 090 — Data Cleaning and Handling Missing Values

[⬅ Day 089](../../09-data-analysis/day-089/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 091 ➡](../../10-machine-learning/day-091/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Detect missing values, duplicates, wrong types and inconsistent text
- Choose between dropping and filling (`dropna`, `fillna`, interpolation, group-wise fill)
- Build a reusable, logged cleaning function and validate the result

## 2. Topic Explanation

"Garbage in, garbage out." Data scientists famously spend most of their time **cleaning** data. Typical problems:

| Problem | Detect | Fix |
|---|---|---|
| Missing values | `df.isna().sum()` | `dropna()`, `fillna(value)`, `interpolate()`, group mean |
| Duplicates | `df.duplicated().sum()` | `drop_duplicates()` |
| Wrong types | `df.dtypes` | `pd.to_numeric(errors="coerce")`, `pd.to_datetime` |
| Inconsistent text | `value_counts()` | `.str.strip().str.lower()` |
| Impossible values / outliers | `describe()`, rules | `clip()`, filter, investigate |

**Drop or fill?**
- Drop rows when few are affected and they're not systematically different.
- Fill numeric gaps with the **median** (robust) or a **group** median (per server); fill time series with **interpolation** or forward-fill.
- Fill categories with `"unknown"` — a missing value can itself be information.
- Never silently fill the **target/label** column for ML.

Always **log what you changed** and **validate** the result (assertions) — cleaning steps are part of your pipeline and must be reproducible. In MLOps, the *exact same* cleaning must run at training time and at prediction time.

> Examples read the sample datasets in [`datasets/`](../../datasets/) using the relative path `../../datasets/...`, so run them from inside this day's folder. Install the libraries with `pip install numpy pandas matplotlib openpyxl`.

## 3. Syntax

```python
df.isna().sum(); df.duplicated().sum()
df.drop_duplicates(); df.dropna(subset=["col"])
df["col"] = df["col"].fillna(df["col"].median())
df["col"] = df.groupby("key")["col"].transform(lambda s: s.fillna(s.median()))
df["col"] = pd.to_numeric(df["col"], errors="coerce")
df["text"] = df["text"].str.strip().str.lower()
```

| Part | Meaning |
|---|---|
| `isna / duplicated` | Detect missing values and duplicate rows. |
| `dropna / drop_duplicates` | Remove problem rows. |
| `fillna / interpolate` | Replace missing values. |
| `groupby().transform` | Group-wise fill that keeps the original shape. |
| `to_numeric(errors="coerce")` | Bad values become NaN instead of crashing. |

## 4. Example 1 — Basic Example: Finding the dirt

```python
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/server_metrics.csv")

print("shape:", df.shape)
print("missing per column:", df.isna().sum().to_dict())
print("duplicate rows:", df.duplicated().sum())
print("server labels:", df["server"].value_counts().to_dict())
print()
print("Rows with any missing value:")
print(df[df.isna().any(axis=1)])
print()
print(df.describe().round(1))
```

## 5. Example 2 — Practical Example: A reusable cleaning pipeline with validation

```python
import pandas as pd

pd.set_option("display.width", 120)


def clean_metrics(raw):
    """Return (clean DataFrame, list of log messages). Never modifies the input."""
    df = raw.copy()
    log = []

    before = len(df)
    df = df.drop_duplicates()
    log.append(f"dropped {before - len(df)} duplicate row(s)")

    fixed = (df["server"] != df["server"].str.strip().str.lower()).sum()
    df["server"] = df["server"].str.strip().str.lower()
    log.append(f"normalised {fixed} server label(s)")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["server", "timestamp"])

    for col in ["cpu", "memory"]:
        missing = df[col].isna().sum()
        df[col] = df.groupby("server")[col].transform(lambda s: s.interpolate().bfill().ffill())
        log.append(f"interpolated {missing} missing {col} value(s) per server")

    missing = df["response_ms"].isna().sum()
    df["response_ms"] = df["response_ms"].fillna(df["response_ms"].median())
    log.append(f"filled {missing} missing response_ms with the median")

    df[["cpu", "memory", "disk"]] = df[["cpu", "memory", "disk"]].clip(0, 100)
    df["response_ms"] = df["response_ms"].astype(int)
    return df.reset_index(drop=True), log


def validate(df):
    assert df.isna().sum().sum() == 0, "still missing values"
    assert not df.duplicated().any(), "duplicates remain"
    assert set(df["server"]) == {"web-01", "web-02", "db-01"}, "unexpected server names"
    assert df[["cpu", "memory", "disk"]].le(100).all().all(), "percentages above 100"
    return True


raw = pd.read_csv("../../datasets/server_metrics.csv")
clean, steps = clean_metrics(raw)
for step in steps:
    print("-", step)
print("validation passed:", validate(clean))
print("shape before/after:", raw.shape, clean.shape)
print(clean.groupby("server")[["cpu", "memory", "response_ms"]].mean().round(1))
clean.to_csv("server_metrics_clean.csv", index=False)
print("saved server_metrics_clean.csv")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `isna().sum()` counts gaps per column; `duplicated()` finds the repeated row; `value_counts()` exposes the inconsistent label `" WEB-01 "`.
- `df[df.isna().any(axis=1)]` shows exactly which rows are incomplete.

**Example 2**
- `clean_metrics` works on a **copy** and returns a log of every change — reproducible and auditable.
- Steps: remove duplicates → normalise text → parse dates and sort → **interpolate per server** (a gap in web-01 is filled from web-01's neighbouring values, not db-01's) → fill remaining gaps with the median → clip impossible values → fix dtypes.
- `groupby(...).transform(...)` applies the fill within each server and returns a Series aligned with the original rows.
- `validate` uses `assert`s as data-quality checks; in a pipeline a failing check should stop the run.

## 7. Expected Output

**Example 1:**

```text
shape: (61, 6)
missing per column: {'timestamp': 0, 'server': 0, 'cpu': 3, 'memory': 2, 'disk': 0, 'response_ms': 2}
duplicate rows: 1
server labels: {'web-01': 20, 'web-02': 20, 'db-01': 20, ' WEB-01 ': 1}

Rows with any missing value:
           timestamp  server   cpu  memory  disk  response_ms
4   2026-11-20 09:20  web-02   NaN    70.1  82.3        266.0
8   2026-11-20 09:40   db-01  52.1     NaN  81.3        258.0
12  2026-11-20 10:00  web-01  73.0    71.5  80.7          NaN
17  2026-11-20 10:25   db-01   NaN    39.2  68.7        154.0
33  2026-11-20 11:45  web-01   NaN    85.7  57.7        327.0
41  2026-11-20 12:25   db-01  66.5     NaN  61.9        252.0
50  2026-11-20 13:10   db-01  40.2    67.4  76.8          NaN

        cpu  memory  disk  response_ms
count  58.0    59.0  61.0         59.0
mean   54.9    65.9  69.9        254.1
std    15.7    12.9   8.3         91.4
min    28.6    37.5  49.5         42.0
25%    43.0    58.7  65.9        188.0
50%    57.6    65.6  69.6        256.0
75%    63.2    71.8  75.8        329.5
max    96.9    99.9  86.7        476.0
```

**Example 2:**

```text
- dropped 1 duplicate row(s)
- normalised 1 server label(s)
- interpolated 3 missing cpu value(s) per server
- interpolated 2 missing memory value(s) per server
- filled 2 missing response_ms with the median
validation passed: True
shape before/after: (61, 6) (60, 6)
         cpu  memory  response_ms
server                           
db-01   53.2    67.4        261.7
web-01  59.2    65.9        241.4
web-02  53.5    65.0        256.2
saved server_metrics_clean.csv
```

> ℹ️ Output was produced with pandas 3.x. With pandas 2.x, text columns show the dtype `object` instead of `str`; everything else is the same.

## 8. Common Mistakes

**1. Filling before deduplicating/normalising**

Order matters: normalise labels first, otherwise group-wise fills use the wrong groups.

**2. Filling everything with 0**

A missing CPU value is not 0 % CPU. Zero-filling biases averages and models.

**3. Cleaning differently in training and serving**

Put cleaning in one function/module and reuse it in both places.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Missing value report:** Create a small DataFrame with some `None` values (5 rows, columns `host`, `cpu`, `owner`), print missing counts and percentages per column, then drop rows where `cpu` is missing and fill `owner` with `unknown`.
- **Task 2 (Medium) — Fix types:** Given a column `["85", "90%", "n/a", "72.5", ""]`, convert it to floats: strip `%`, coerce invalid values to NaN with `pd.to_numeric(errors="coerce")`, then fill NaN with the median. Print each stage.
- **Task 3 (Practical Challenge) — Clean the house dataset:** Copy `house_prices.csv` into a DataFrame and deliberately damage it: set 10 random `price` values to NaN (`default_rng(0)`), duplicate 5 rows and set 3 `bedrooms` to -1. Then write `clean_houses(df)` that fixes all three problems (drop rows with missing price — it's the ML label!, drop duplicates, replace invalid bedrooms with the median) and validates the result. Print what was changed and the final shape.

## 10. DevOps/MLOps Connection

- **DevOps / Monitoring:** metric gaps (scrape failures), duplicate log lines and inconsistent hostnames are everyday data-quality problems in observability data.
- **Data engineering:** cleaning + validation steps (often with tools like Great Expectations or pandera) protect downstream dashboards and models.
- **ML / MLOps:** most model failures in production are data problems. The cleaning function becomes part of the pipeline that runs identically in training and serving (Day 100).

## 11. Interview Questions

**Q1. How do you decide between dropping and imputing missing values?**

<details><summary>Show answer</summary>

Consider how much is missing, whether missingness is random or meaningful, whether it's the label, and the impact on analysis; impute with robust statistics or domain logic, otherwise drop.

</details>

**Q2. What does `pd.to_numeric(errors='coerce')` do?**

<details><summary>Show answer</summary>

Converts values to numbers and turns unparseable entries into NaN instead of raising an error.

</details>

**Q3. Why must data cleaning be identical in training and inference?**

<details><summary>Show answer</summary>

Otherwise the model sees differently processed inputs in production (training-serving skew), causing wrong predictions.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 90 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 089](../../09-data-analysis/day-089/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 091 ➡](../../10-machine-learning/day-091/README.md)
