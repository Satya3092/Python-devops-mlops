# Day 083 — Practice Tasks: Introduction to Data Science and Data Analysis

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Statistics of build times

**Problem statement:** For build durations `[312, 298, 1045, 305, 287, 330, 299, 315, 290, 301]` print mean, median, standard deviation and p90.

**Input requirements:** No user input required.

**Expected behavior:** Mean ≈ 378.2, median 303.0.

**Expected output:**

```text
mean=378.2 median=303.0 stdev=234.6 p90=973.5
```

## Task 2 — Medium: Classify the data

**Problem statement:** For each column of `../../datasets/servers.csv` print whether it is numerical or categorical (try converting the first value to float).

**Input requirements:** No user input required.

**Expected behavior:** hostname/environment/region/status categorical; others numerical.

**Expected output:**

```text
hostname      categorical
environment   categorical
region        categorical
cpu_cores     numerical
memory_gb     numerical
cpu_usage     numerical
memory_usage  numerical
disk_usage    numerical
status        categorical
```

## Task 3 — Practical Challenge: Disk-risk question

**Problem statement:** Answer: 'Which servers have disk usage above the 75th percentile of all servers, and which environment do they belong to?' Print the threshold, the servers and a count per environment. Save a histogram of disk usage to `disk_hist.png`.

**Input requirements:** No user input required.

**Expected behavior:** Threshold, a list of servers and env counts; the chart file is created.

**Expected output:**

```text
75th percentile threshold: 74.25%
  prod-web-03      75%  (prod)
  prod-web-06      82%  (prod)
  dev-web-08       82%  (dev)
  staging-web-10   88%  (staging)
  staging-web-19   84%  (staging)
Per environment: {'prod': 2, 'dev': 1, 'staging': 2}
Saved disk_hist.png
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
