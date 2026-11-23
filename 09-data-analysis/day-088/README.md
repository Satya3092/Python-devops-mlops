# Day 088 — Reading CSV and Excel Data

[⬅ Day 087](../../09-data-analysis/day-087/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 089 ➡](../../09-data-analysis/day-089/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use `read_csv` options: separators, columns, dtypes, dates, missing values, chunks
- Read and write Excel files with multiple sheets
- Export results to CSV, Excel and JSON

## 2. Topic Explanation

Real files are messy: semicolons instead of commas, extra header lines, `N/A` markers, dates as text, huge sizes. `pd.read_csv` has options for all of them:

| Option | Purpose |
|---|---|
| `sep=";"` | different delimiter (`"\t"` for TSV) |
| `usecols=[...]` | read only some columns (faster, less memory) |
| `dtype={"id": "string"}` | force column types (keep leading zeros!) |
| `parse_dates=["timestamp"]` | convert text to datetime |
| `na_values=["N/A", "-"]` | extra markers for missing values |
| `skiprows=n` / `nrows=n` | skip junk lines / read a sample |
| `chunksize=10_000` | process huge files piece by piece |
| `index_col="host"` | use a column as the index |

**Excel** (needs `openpyxl`):
- `pd.read_excel("file.xlsx", sheet_name="sales")` — one sheet; `sheet_name=None` → dict of all sheets.
- `df.to_excel("out.xlsx", index=False)`; several sheets with `pd.ExcelWriter`.

**Exporting**: `to_csv`, `to_excel`, `to_json(orient="records")`, `to_markdown()` (for reports), `to_parquet` (fast columnar format used in data lakes).

Always pass `index=False` when exporting unless the index carries real information.

> Examples read the sample datasets in [`datasets/`](../../datasets/) using the relative path `../../datasets/...`, so run them from inside this day's folder. Install the libraries with `pip install numpy pandas matplotlib openpyxl`.

## 3. Syntax

```python
pd.read_csv(path, sep=",", usecols=[...], dtype={...}, parse_dates=[...], na_values=[...])
for chunk in pd.read_csv(path, chunksize=10000): ...
pd.read_excel("file.xlsx", sheet_name="sheet1")
with pd.ExcelWriter("out.xlsx") as writer:
    df.to_excel(writer, sheet_name="summary", index=False)
df.to_csv("out.csv", index=False); df.to_json("out.json", orient="records")
```

| Part | Meaning |
|---|---|
| `usecols / dtype` | Choose columns and types while reading. |
| `parse_dates` | Convert to datetime64. |
| `na_values` | Treat custom markers as missing. |
| `chunksize` | Iterate over a large file in pieces. |
| `ExcelWriter` | Write several sheets to one workbook. |

## 4. Example 1 — Basic Example: read_csv options on a messy export

```python
from pathlib import Path

import pandas as pd

pd.set_option("display.width", 120)

messy = """# exported from CMDB on 2026-11-20
asset_id;hostname;owner;purchase_date;cost_usd;status
00123;web-01;team-web;2024-03-15;1200;active
00124;web-02;team-web;2024-03-15;N/A;active
00987;db-01;-;2023-11-02;5400;active
01001;old-ftp;team-legacy;2019-07-30;800;retired
"""
Path("cmdb_export.csv").write_text(messy)

df = pd.read_csv(
    "cmdb_export.csv",
    sep=";",
    skiprows=1,                       # skip the comment line
    dtype={"asset_id": "string"},     # keep leading zeros
    parse_dates=["purchase_date"],
    na_values=["N/A", "-"],
)
print(df)
print(df.dtypes)
print("Missing values per column:", df.isna().sum().to_dict())
print("Age in years:", ((pd.Timestamp("2026-11-20") - df["purchase_date"]).dt.days / 365).round(1).tolist())

subset = pd.read_csv("../../datasets/servers.csv", usecols=["hostname", "cpu_usage"], nrows=3)
print(subset)
```

## 5. Example 2 — Practical Example: Excel in, multi-sheet Excel/CSV/JSON out, chunked processing

```python
import json

import pandas as pd

pd.set_option("display.width", 120)

sales = pd.read_excel("../../datasets/sales.xlsx", sheet_name="sales")
print("Excel rows:", len(sales), "| columns:", list(sales.columns))
sales["revenue"] = sales["units"] * sales["unit_price"]

by_region = sales.groupby("region", as_index=False)["revenue"].sum()     # Day 89 explains groupby
by_product = sales.groupby("product", as_index=False)["revenue"].sum()

with pd.ExcelWriter("sales_report.xlsx") as writer:
    sales.to_excel(writer, sheet_name="raw", index=False)
    by_region.to_excel(writer, sheet_name="by_region", index=False)
    by_product.to_excel(writer, sheet_name="by_product", index=False)

sheets = pd.read_excel("sales_report.xlsx", sheet_name=None)       # dict of all sheets
print("Workbook sheets:", {name: frame.shape for name, frame in sheets.items()})

by_region.to_csv("by_region.csv", index=False)
by_region.to_json("by_region.json", orient="records")
print("CSV :", open("by_region.csv").read().strip().splitlines()[:2])
print("JSON:", json.load(open("by_region.json"))[:2])

# Processing a 'big' file in chunks keeps memory low
total_units = 0
for chunk in pd.read_csv("../../datasets/sales.csv", chunksize=10):
    total_units += chunk["units"].sum()
print("Units counted chunk by chunk:", total_units, "| check:", pd.read_csv("../../datasets/sales.csv")["units"].sum())
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The export uses `;`, has a comment line, leading-zero IDs, `N/A`/`-` markers and dates.
- `sep`, `skiprows`, `dtype`, `parse_dates` and `na_values` fix all of it at read time: IDs stay `00123`, missing costs/owners become `NaN`/`<NA>`, dates become real `datetime64` so we can compute asset age.
- `usecols` + `nrows` read just a sample of a file — handy for huge datasets.

**Example 2**
- `read_excel` loads a sheet; a computed `revenue` column is added.
- `ExcelWriter` writes three sheets into one workbook; `sheet_name=None` reads them all back as a dict.
- The same summary is exported as CSV and JSON (`orient="records"` = list of row dicts, ideal for APIs).
- `chunksize` returns an iterator of smaller DataFrames — the pattern for files larger than memory.

## 7. Expected Output

**Example 1:**

```text
  asset_id hostname        owner purchase_date  cost_usd   status
0    00123   web-01     team-web    2024-03-15    1200.0   active
1    00124   web-02     team-web    2024-03-15       NaN   active
2    00987    db-01          NaN    2023-11-02    5400.0   active
3    01001  old-ftp  team-legacy    2019-07-30     800.0  retired
asset_id                 string
hostname                    str
owner                       str
purchase_date    datetime64[us]
cost_usd                float64
status                      str
dtype: object
Missing values per column: {'asset_id': 0, 'hostname': 0, 'owner': 1, 'purchase_date': 0, 'cost_usd': 1, 'status': 0}
Age in years: [2.7, 2.7, 3.1, 7.3]
         hostname  cpu_usage
0  staging-web-01         13
1      dev-web-02         84
2     prod-web-03         53
```

**Example 2:**

```text
Excel rows: 48 | columns: ['date', 'region', 'product', 'units', 'unit_price']
Workbook sheets: {'raw': (48, 6), 'by_region': (4, 2), 'by_product': (4, 2)}
CSV : ['region,revenue', 'East,46475']
JSON: [{'region': 'East', 'revenue': 46475}, {'region': 'North', 'revenue': 70680}]
Units counted chunk by chunk: 745 | check: 745
```

> ℹ️ Output was produced with pandas 3.x. With pandas 2.x, text columns show the dtype `object` instead of `str`; everything else is the same. Reading/writing `.xlsx` needs `pip install openpyxl`.

## 8. Common Mistakes

**1. Losing leading zeros**

IDs like `00123` become the number 123. Use `dtype={"id": "string"}`.

**2. Dates left as text**

Sorting text dates like `11/2/2026` gives wrong orders. Use `parse_dates` or `pd.to_datetime`.

**3. Writing the index by accident**

`to_csv` adds an unnamed index column unless you pass `index=False`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Semicolon file:** Write a small semicolon-separated CSV with a comment line and 3 rows (service;port;protocol), read it correctly with pandas and print it.
- **Task 2 (Medium) — Excel round trip:** Read `../../datasets/sales.xlsx`, keep only `Laptop` rows, write them to `laptops.xlsx` (sheet `laptops`), read it back and print the number of rows and the total units.
- **Task 3 (Practical Challenge) — Metrics export pipeline:** Read `../../datasets/server_metrics.csv` with `parse_dates=["timestamp"]`, compute per-server mean CPU and max response time, and export the result to `metrics_summary.csv`, `metrics_summary.json` (records) and an Excel file with two sheets (`raw`, `summary`). Print the summary and the sheet names of the Excel file.

## 10. DevOps/MLOps Connection

- **DevOps:** turn CMDB/monitoring exports into clean data; produce Excel reports for managers and JSON for automation from one script.
- **Cloud:** read cost exports; process huge CloudTrail/ALB logs in chunks.
- **Data engineering / MLOps:** correct dtypes and dates at ingestion avoid silent data bugs; Parquet/JSON exports feed training pipelines.

## 11. Interview Questions

**Q1. How do you read a CSV file that is too large for memory?**

<details><summary>Show answer</summary>

Use `chunksize` to iterate over pieces, `usecols` to read fewer columns, appropriate `dtype`s, or tools like Parquet/Dask/Polars.

</details>

**Q2. How do you keep leading zeros in an ID column?**

<details><summary>Show answer</summary>

Read it as a string: `dtype={"id": "string"}` (or `str`).

</details>

**Q3. How do you write multiple DataFrames to one Excel file?**

<details><summary>Show answer</summary>

Use `pd.ExcelWriter` and call `df.to_excel(writer, sheet_name=...)` for each.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 88 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 087](../../09-data-analysis/day-087/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 089 ➡](../../09-data-analysis/day-089/README.md)
