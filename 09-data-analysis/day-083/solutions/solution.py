"""
Day 083 — Introduction to Data Science and Data Analysis: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import csv
import statistics as st
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ===== Task 1 =====
builds = [312, 298, 1045, 305, 287, 330, 299, 315, 290, 301]
print(f"mean={st.mean(builds):.1f} median={st.median(builds)} stdev={st.stdev(builds):.1f} "
      f"p90={st.quantiles(builds, n=10)[8]:.1f}")

# ===== Task 2 =====
with open("../../datasets/servers.csv", newline="") as f:
    first = next(csv.DictReader(f))
for column, value in first.items():
    try:
        float(value)
        kind = "numerical"
    except ValueError:
        kind = "categorical"
    print(f"{column:<13} {kind}")

# ===== Task 3 =====
with open("../../datasets/servers.csv", newline="") as f:
    rows = list(csv.DictReader(f))
disk = [int(r["disk_usage"]) for r in rows]
threshold = st.quantiles(disk, n=4)[2]
risky = [r for r in rows if int(r["disk_usage"]) > threshold]
print(f"75th percentile threshold: {threshold}%")
for r in risky:
    print(f"  {r['hostname']:<16} {r['disk_usage']}%  ({r['environment']})")
print("Per environment:", dict(Counter(r["environment"] for r in risky)))
plt.hist(disk, bins=8, edgecolor="black")
plt.axvline(threshold, color="red", linestyle="--")
plt.title("Disk usage distribution")
plt.savefig("disk_hist.png")
print("Saved disk_hist.png")
