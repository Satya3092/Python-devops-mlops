# Day 088 — Practice Tasks: Reading CSV and Excel Data

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Semicolon file

**Problem statement:** Write a small semicolon-separated CSV with a comment line and 3 rows (service;port;protocol), read it correctly with pandas and print it.

**Input requirements:** No user input required.

**Expected behavior:** A 3-row DataFrame with the right columns.

**Expected output:**

```text
  service  port protocol
0     ssh    22      tcp
1     dns    53      udp
2   https   443      tcp
```

## Task 2 — Medium: Excel round trip

**Problem statement:** Read `../../datasets/sales.xlsx`, keep only `Laptop` rows, write them to `laptops.xlsx` (sheet `laptops`), read it back and print the number of rows and the total units.

**Input requirements:** No user input required.

**Expected behavior:** Row count and units for laptops.

**Expected output:**

```text
rows: 13 | units: 170
```

## Task 3 — Practical Challenge: Metrics export pipeline

**Problem statement:** Read `../../datasets/server_metrics.csv` with `parse_dates=["timestamp"]`, compute per-server mean CPU and max response time, and export the result to `metrics_summary.csv`, `metrics_summary.json` (records) and an Excel file with two sheets (`raw`, `summary`). Print the summary and the sheet names of the Excel file.

**Input requirements:** No user input required.

**Expected behavior:** A summary table and `['raw', 'summary']`.

**Expected output:**

```text
     server  mean_cpu  max_response_ms
0   WEB-01       61.3            185.0
1     db-01      52.7            476.0
2    web-01      59.1            357.0
3    web-02      52.5            394.0
['raw', 'summary']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
