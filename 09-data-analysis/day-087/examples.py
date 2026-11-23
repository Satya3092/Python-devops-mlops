"""
Day 087 — Pandas Series and DataFrames
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Series and DataFrame basics
# ======================================================================
import pandas as pd

cpu = pd.Series([45, 72, 91, 38], index=["web-01", "web-02", "db-01", "cache-01"], name="cpu")
print(cpu)
print("db-01:", cpu["db-01"], "| over 70:", cpu[cpu > 70].to_dict())
print("mean:", cpu.mean())

df = pd.DataFrame({
    "host": ["web-01", "web-02", "db-01", "cache-01"],
    "env": ["prod", "prod", "prod", "dev"],
    "cpu": [45, 72, 91, 38],
    "memory_gb": [8, 8, 64, 4],
})
print(df)
print("iloc[0, 0]:", df.iloc[0, 0], "| first two rows:\n", df.iloc[:2])

indexed = df.set_index("host")
print("loc['db-01', 'cpu']:", indexed.loc["db-01", "cpu"])
print(indexed.loc["web-02":"db-01", ["env", "cpu"]])     # label slice includes db-01

# ======================================================================
# Example 2 — Enriching a server table with new columns
# ======================================================================
import numpy as np
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")

df["memory_per_core"] = df["memory_gb"] / df["cpu_cores"]
df["max_usage"] = df[["cpu_usage", "memory_usage", "disk_usage"]].max(axis=1)
df["needs_attention"] = np.where(df["max_usage"] >= 75, "yes", "no")
df["load_band"] = pd.cut(df["cpu_usage"], bins=[0, 40, 75, 100], labels=["low", "medium", "high"])
df["tier"] = df["environment"].map({"prod": 1, "staging": 2, "dev": 3})
df = df.rename(columns={"hostname": "host"}).drop(columns=["region"])

print(df.loc[df["needs_attention"] == "yes", ["host", "environment", "max_usage", "load_band", "tier"]].head(6))
print()
print("Load bands:", df["load_band"].value_counts().sort_index().to_dict())
print("Columns now:", list(df.columns))

summary = df.assign(cost_per_month=df["cpu_cores"] * 15 + df["memory_gb"] * 4)
print("Estimated monthly cost (top 3):")
print(summary.nlargest(3, "cost_per_month")[["host", "cpu_cores", "memory_gb", "cost_per_month"]])
