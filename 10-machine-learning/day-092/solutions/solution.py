"""
Day 092 — Supervised vs Unsupervised Learning: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

pd.set_option("display.width", 120)

# ===== Task 1 =====
for question, kind in [("Will this build fail?", "supervised-classification"),
                       ("How many GB of logs tomorrow?", "supervised-regression"),
                       ("Which users behave similarly?", "unsupervised"),
                       ("Which alert severity (1-4)?", "supervised-classification"),
                       ("Unusual transactions, no labels", "unsupervised")]:
    print(f"{question:<34} {kind}")

# ===== Task 2 =====
servers = pd.read_csv("../../datasets/servers.csv")
features = ["cpu_usage", "memory_usage", "disk_usage"]
servers["cluster"] = KMeans(n_clusters=3, n_init=10, random_state=42).fit_predict(
    StandardScaler().fit_transform(servers[features]))
summary = servers.groupby("cluster").agg(servers=("hostname", "count"), cpu=("cpu_usage", "mean"),
                                         memory=("memory_usage", "mean"), disk=("disk_usage", "mean"),
                                         status=("status", lambda s: s.mode()[0])).round(1)
print(summary)

# ===== Task 3 =====
metrics = pd.read_csv("../../datasets/server_metrics.csv").dropna()
cols = ["cpu", "memory", "response_ms"]
flags = IsolationForest(contamination=0.05, random_state=42).fit_predict(StandardScaler().fit_transform(metrics[cols]))
print(metrics[flags == -1][["timestamp", "server"] + cols].to_string(index=False))
