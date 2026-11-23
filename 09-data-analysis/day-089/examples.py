"""
Day 089 — Data Filtering, Sorting, and Grouping
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Filtering and sorting servers
# ======================================================================
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")
cols = ["hostname", "environment", "region", "cpu_usage", "disk_usage", "status"]

print("Prod servers with CPU > 60:")
print(df[(df["environment"] == "prod") & (df["cpu_usage"] > 60)][cols])

print("\nIn Mumbai or Ireland regions, disk between 60 and 90:")
print(df[df["region"].isin(["ap-south-1", "eu-west-1"]) & df["disk_usage"].between(60, 90)][cols])

print("\nUnhealthy servers whose hostname contains '-web-1' (query + str):")
unhealthy = df.query("status != 'healthy'")
print(unhealthy[unhealthy["hostname"].str.contains("-web-1")][["hostname", "status"]])

print("\nTop 5 by CPU, ties broken by disk:")
print(df.sort_values(["cpu_usage", "disk_usage"], ascending=[False, False]).head(5)[cols])

# ======================================================================
# Example 2 — Grouping: per-environment stats, pivots and time windows
# ======================================================================
import pandas as pd

pd.set_option("display.width", 120)
servers = pd.read_csv("../../datasets/servers.csv")

summary = servers.groupby("environment").agg(
    servers=("hostname", "count"),
    avg_cpu=("cpu_usage", "mean"),
    max_disk=("disk_usage", "max"),
    total_memory_gb=("memory_gb", "sum"),
).round(1).sort_values("avg_cpu", ascending=False)
print(summary)

print("\nStatus by environment (crosstab):")
print(pd.crosstab(servers["environment"], servers["status"]))

sales = pd.read_csv("../../datasets/sales.csv", parse_dates=["date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
pivot = sales.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum", fill_value=0)
print("\nRevenue pivot (region x product):")
print(pivot)
print("Best region:", pivot.sum(axis=1).idxmax(), "| best product:", pivot.sum(axis=0).idxmax())

metrics = pd.read_csv("../../datasets/server_metrics.csv", parse_dates=["timestamp"])
hourly = metrics.set_index("timestamp").resample("1h")["cpu"].mean().round(1)
print("\nFleet average CPU per hour:")
print(hourly)
