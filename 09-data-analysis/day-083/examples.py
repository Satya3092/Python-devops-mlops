"""
Day 083 — Introduction to Data Science and Data Analysis
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Descriptive statistics of response times
# ======================================================================
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

# ======================================================================
# Example 2 — From a CSV to an answer and a chart
# ======================================================================
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
