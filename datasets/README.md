# Datasets

[🏠 Home](../README.md)

Small, synthetic, privacy-free datasets used by the lessons and projects. All are generated reproducibly by
[`generate_datasets.py`](generate_datasets.py) (seed 42), so you never need to download anything.

| File | Rows | Columns | Used in |
|---|---|---|---|
| `servers.csv` | 20 | hostname, environment, region, cpu_cores, memory_gb, cpu_usage, memory_usage, disk_usage, status | Days 50, 83, 86–89, 92 |
| `app.log` | 60 | `date time LEVEL [ip] message` application log | Days 68, 73, Project 3 |
| `server_metrics.csv` | 61 | timestamp, server, cpu, memory, disk, response_ms (with missing values, a duplicate and a messy label on purpose) | Days 88–90, 92, Project 6 |
| `sales.csv` / `sales.xlsx` | 48 | date, region, product, units, unit_price | Days 88–89, Project 6 |
| `house_prices.csv` | 200 | size_sqft, bedrooms, age_years, distance_km, **price** (regression label) | Days 86–87, 93, 95, 97, Project 7 |
| `server_failures.csv` | 400 | cpu_usage, memory_usage, disk_usage, error_count, response_time_ms, **failure** (0/1 classification label, ~18 % positive) | Days 89, 92–100, Project 8 |

Regenerate them with:
```bash
pip install numpy pandas openpyxl
python generate_datasets.py
```
