# Project 6 — CSV Data Analysis

**Phase:** after Day 90 · **Difficulty:** 🟠 Intermediate+ · **Concepts:** NumPy, pandas, data cleaning, grouping, matplotlib, report generation

`analyze.py` turns two raw CSV exports into a **clean dataset, summary tables, charts and a Markdown report** — the kind of weekly report an SRE or FinOps team sends to stakeholders.

## Inputs (from [`datasets/`](../../datasets/))
- `sales.csv` — date, region, product, units, unit_price
- `server_metrics.csv` — timestamp, server, cpu, memory, disk, response_ms (contains missing values, a duplicate and a messy label on purpose)

## What it does
1. **Load** with correct dtypes and parsed dates.
2. **Clean** server metrics: dedupe, normalise labels, interpolate gaps per server, clip impossible values.
3. **Analyse sales:** revenue by region/product/month, best sellers, month-over-month growth (pandas `groupby`, `pivot_table`, `pct_change`).
4. **Analyse servers:** per-server averages, p95 response time (NumPy `percentile`), hourly CPU trend, z-score anomalies.
5. **Visualise:** 3 PNG charts in `output/`.
6. **Report:** `output/report.md` with tables (`to_markdown`) and chart links; cleaned data saved as CSV.

## Run
```bash
pip install numpy pandas matplotlib tabulate
python analyze.py                     # uses ../../datasets by default
python analyze.py --data-dir /path/to/exports --out-dir weekly-report
```

Output:
```text
[load] sales: 48 rows | metrics: 61 rows
[clean] metrics: removed 1 duplicate, fixed 1 label, filled 7 missing values
[sales] total revenue 210,535 | best region North | best product Laptop
[servers] highest p95 latency: db-01 408.6 ms | anomalies: 2
[report] output/report.md, 3 charts, 2 CSV files
```

## Ideas to extend
- Schedule weekly with cron/GitHub Actions and email/Slack the Markdown report.
- Add a cost dataset (AWS CUR export) and compute cost per server.
- Swap matplotlib for an interactive Plotly HTML report.
