# Day 090 — Practice Tasks: Data Cleaning and Handling Missing Values

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Missing value report

**Problem statement:** Create a small DataFrame with some `None` values (5 rows, columns `host`, `cpu`, `owner`), print missing counts and percentages per column, then drop rows where `cpu` is missing and fill `owner` with `unknown`.

**Input requirements:** No user input required.

**Expected behavior:** A report and the cleaned table.

**Expected output:**

```text
       missing  percent
host         0      0.0
cpu          2     40.0
owner        2     40.0
  host   cpu    owner
0    a  50.0    team1
2    c  70.0    team2
4    e  30.0  unknown
```

## Task 2 — Medium: Fix types

**Problem statement:** Given a column `["85", "90%", "n/a", "72.5", ""]`, convert it to floats: strip `%`, coerce invalid values to NaN with `pd.to_numeric(errors="coerce")`, then fill NaN with the median. Print each stage.

**Input requirements:** No user input required.

**Expected behavior:** Final values `[85.0, 90.0, 85.0, 72.5, 85.0]`.

**Expected output:**

```text
['85', '90', 'n/a', '72.5', '']
[85.0, 90.0, nan, 72.5, nan]
[85.0, 90.0, 85.0, 72.5, 85.0]
```

## Task 3 — Practical Challenge: Clean the house dataset

**Problem statement:** Copy `house_prices.csv` into a DataFrame and deliberately damage it: set 10 random `price` values to NaN (`default_rng(0)`), duplicate 5 rows and set 3 `bedrooms` to -1. Then write `clean_houses(df)` that fixes all three problems (drop rows with missing price — it's the ML label!, drop duplicates, replace invalid bedrooms with the median) and validates the result. Print what was changed and the final shape.

**Input requirements:** No user input required.

**Expected behavior:** Final shape (190, 5) after dropping 10 label-missing rows and 5 duplicates.

**Expected output:**

```text
damaged shape: (205, 5)
dropped 11 rows with missing price (label)
dropped 4 duplicates
fixed 3 invalid bedroom values
final shape: (190, 5)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
