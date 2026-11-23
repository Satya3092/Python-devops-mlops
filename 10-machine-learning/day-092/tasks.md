# Day 092 — Practice Tasks: Supervised vs Unsupervised Learning

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Name the problem type

**Problem statement:** For each question print supervised-regression, supervised-classification or unsupervised: (1) Will this build fail? (2) How many GB will logs use tomorrow? (3) Which users behave similarly? (4) Which alert severity (1–4)? (5) Which transactions look unusual (no labels)?

**Input requirements:** No user input required.

**Expected behavior:** Five correct types.

**Expected output:**

```text
Will this build fail?              supervised-classification
How many GB of logs tomorrow?      supervised-regression
Which users behave similarly?      unsupervised
Which alert severity (1-4)?        supervised-classification
Unusual transactions, no labels    unsupervised
```

## Task 2 — Medium: Cluster the server dataset

**Problem statement:** Cluster `servers.csv` on cpu/memory/disk usage (scaled) into 3 groups with K-Means and print, per cluster, the number of servers, the average usage values and the most common `status`.

**Input requirements:** No user input required.

**Expected behavior:** Three clusters with averages and dominant status.

**Expected output:**

```text
         servers   cpu  memory  disk   status
cluster                                      
0              6  29.3    83.0  71.0  warning
1              9  62.2    48.2  32.6  healthy
2              5  70.4    40.0  72.8  warning
```

## Task 3 — Practical Challenge: Anomaly detector for metrics

**Problem statement:** Load `server_metrics.csv`, drop rows with missing values, scale cpu/memory/response_ms and run IsolationForest (contamination 0.05). Print the anomalous rows (timestamp, server, cpu, memory, response_ms).

**Input requirements:** No user input required.

**Expected behavior:** A few unusual readings.

**Expected output:**

```text
       timestamp server  cpu  memory  response_ms
2026-11-20 10:35 web-02 28.6    90.6        151.0
2026-11-20 10:40  db-01 88.1    99.9        216.0
2026-11-20 13:20 web-02 96.9    62.5        394.0
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
