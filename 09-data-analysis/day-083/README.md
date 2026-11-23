# Day 083 — Introduction to Data Science and Data Analysis

[⬅ Day 082](../../08-api-cloud/day-082/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 084 ➡](../../09-data-analysis/day-084/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 9 — Data Analysis and ML Preparation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain the data analysis workflow: question → collect → clean → explore → visualise → communicate
- Distinguish data types (numerical, categorical, time series) and descriptive statistics
- Compute basic statistics with the standard library `statistics` module and draw a first chart

## 2. Topic Explanation

**Data analysis** is turning raw data into answers. **Data science** adds prediction (machine learning) on top. As a DevOps engineer you already do this informally: "Why did latency spike at 10:05?" is a data question.

**The workflow**
1. **Ask** a clear question — "Which servers are at risk of running out of disk this month?"
2. **Collect** data — logs, metrics exports, CSV from CMDB, APIs.
3. **Clean** — fix types, handle missing values, remove duplicates (Day 90).
4. **Explore** — statistics, grouping, filtering (Days 86–89).
5. **Visualise** — charts reveal patterns tables hide.
6. **Communicate** — a report, dashboard or alert.
7. (**Model** — predict the future with ML, Days 91–96.)

**Kinds of data**
- **Numerical**: continuous (CPU 73.4 %) or discrete (restart count 3).
- **Categorical**: environment (`prod`/`dev`), region, status.
- **Time series**: values over time (metrics every minute).

**Descriptive statistics**
- **Mean** (average) — sensitive to outliers.
- **Median** (middle value) — robust to outliers. A latency median of 120 ms with a mean of 400 ms means a few very slow requests.
- **Mode** — most frequent value.
- **Standard deviation** — how spread out values are.
- **Percentiles** — p95 latency = 95 % of requests were faster than this (SLOs use p95/p99!).

The Python data stack: **NumPy** (fast arrays) → **pandas** (tables) → **matplotlib** (charts) → **scikit-learn** (ML).

> Examples read the sample datasets in [`datasets/`](../../datasets/) using the relative path `../../datasets/...`, so run them from inside this day's folder. Install the libraries with `pip install numpy pandas matplotlib openpyxl`.

## 3. Syntax

```python
import statistics as st
st.mean(values)   st.median(values)   st.mode(values)
st.stdev(values)  st.quantiles(values, n=100)[94]   # p95
```

| Part | Meaning |
|---|---|
| `mean` | Arithmetic average. |
| `median` | Middle value of the sorted data. |
| `stdev` | Sample standard deviation (spread). |
| `quantiles(n=100)` | Cut points; index 94 is the 95th percentile. |

## 4. Example 1 — Basic Example: Descriptive statistics of response times

```python
import statistics as st

response_ms = [120, 98, 134, 101, 87, 1450, 143, 110, 99, 125, 131, 2100, 118, 105, 96, 122, 140, 108, 97, 115]

print("count :", len(response_ms))
print("mean  :", round(st.mean(response_ms), 1), "ms")
print("median:", st.median(response_ms), "ms")
print("stdev :", round(st.stdev(response_ms), 1), "ms")
print("min/max:", min(response_ms), "/", max(response_ms), "ms")
percentiles = st.quantiles(response_ms, n=100)
print("p50 / p95 / p99:", round(percentiles[49]), "/", round(percentiles[94]), "/", round(percentiles[98]), "ms")

without_outliers = [v for v in response_ms if v < 1000]
print("mean without the 2 outliers:", round(st.mean(without_outliers), 1), "ms")
print("Lesson: one slow request moves the mean a lot, the median barely.")
```

## 5. Example 2 — Practical Example: From a CSV to an answer and a chart

```python
import csv
import statistics as st
from collections import defaultdict

import matplotlib
matplotlib.use("Agg")                         # draw to a file, no window needed
import matplotlib.pyplot as plt

# Question: which environment runs hottest, and how many servers need attention?
by_env = defaultdict(list)
statuses = defaultdict(int)
with open("../../datasets/servers.csv", newline="") as f:
    for row in csv.DictReader(f):
        by_env[row["environment"]].append(int(row["cpu_usage"]))
        statuses[row["status"]] += 1

print(f"{'ENV':<9}{'N':>3}{'MEAN':>7}{'MEDIAN':>8}{'MAX':>5}")
for env, values in sorted(by_env.items()):
    print(f"{env:<9}{len(values):>3}{st.mean(values):>7.1f}{st.median(values):>8}{max(values):>5}")
print("Status counts:", dict(statuses))

envs = sorted(by_env)
plt.figure(figsize=(6, 3.5))
plt.bar(envs, [st.mean(by_env[e]) for e in envs], color=["#4C72B0", "#55A868", "#C44E52"])
plt.axhline(75, linestyle="--", color="gray", label="warning threshold")
plt.title("Average CPU usage by environment")
plt.ylabel("CPU %")
plt.legend()
plt.tight_layout()
plt.savefig("cpu_by_env.png", dpi=100)
print("Chart saved to cpu_by_env.png")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The mean (~280 ms) is pulled up by two very slow requests; the median (~117 ms) describes the "typical" request. This is why monitoring dashboards show percentiles.
- `quantiles(n=100)` returns 99 cut points; index 94 is p95, 98 is p99.

**Example 2**
- `csv.DictReader` reads the server dataset; values are grouped by environment with `defaultdict(list)`.
- A small aligned table answers the question numerically.
- `matplotlib.use("Agg")` renders without a display (needed on servers/CI); `plt.savefig` writes a PNG you can attach to a report or Slack message.

## 7. Expected Output

**Example 1:**

```text
count : 20
mean  : 279.9 ms
median: 116.5 ms
stdev : 522.3 ms
min/max: 87 / 2100 ms
p50 / p95 / p99: 116 / 2068 / 2614 ms
mean without the 2 outliers: 113.8 ms
Lesson: one slow request moves the mean a lot, the median barely.
```

**Example 2:**

```text
ENV        N   MEAN  MEDIAN  MAX
dev        7   54.0      51   92
prod       6   49.0    58.5   78
staging    7   59.4      49   95
Status counts: {'warning': 10, 'critical': 4, 'healthy': 6}
Chart saved to cpu_by_env.png
```

## 8. Common Mistakes

**1. Reporting only the mean**

Means hide outliers and skew. Always look at median and p95/p99 for latency-like data.

**2. Starting without a question**

Exploring data aimlessly wastes time. Write the question first.

**3. Trusting raw data**

Exports contain duplicates, blanks and wrong types. Inspect and clean before concluding (Day 90).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Statistics of build times:** For build durations `[312, 298, 1045, 305, 287, 330, 299, 315, 290, 301]` print mean, median, standard deviation and p90.
- **Task 2 (Medium) — Classify the data:** For each column of `../../datasets/servers.csv` print whether it is numerical or categorical (try converting the first value to float).
- **Task 3 (Practical Challenge) — Disk-risk question:** Answer: 'Which servers have disk usage above the 75th percentile of all servers, and which environment do they belong to?' Print the threshold, the servers and a count per environment. Save a histogram of disk usage to `disk_hist.png`.

## 10. DevOps/MLOps Connection

- **DevOps / SRE:** SLOs are statistics (p99 latency, availability %); capacity planning and incident reviews are data analysis.
- **Cloud:** cost analysis (which team/service drives spend?) is grouping and summarising billing data.
- **Data engineering:** pipelines prepare clean data for analysts and models.
- **MLOps:** before training, you explore data; after deployment, you monitor prediction distributions for drift — the same statistics.

## 11. Interview Questions

**Q1. Why use the median or p95 instead of the mean for latency?**

<details><summary>Show answer</summary>

Latency distributions are skewed by outliers; the median shows the typical experience and p95/p99 show tail latency that users feel.

</details>

**Q2. What are the main steps of a data analysis workflow?**

<details><summary>Show answer</summary>

Define the question, collect data, clean it, explore/analyse, visualise, communicate findings (and optionally model).

</details>

**Q3. What is the difference between categorical and numerical data?**

<details><summary>Show answer</summary>

Numerical data are quantities you can do arithmetic on; categorical data are labels/groups (possibly ordered) without numeric meaning.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 83 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 082](../../08-api-cloud/day-082/README.md) | [📚 Phase 9: Data Analysis and ML Preparation](../README.md) | [🏠 Home](../../README.md) | [Day 084 ➡](../../09-data-analysis/day-084/README.md)
