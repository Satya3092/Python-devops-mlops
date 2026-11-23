"""
Day 086 — Pandas Introduction
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Load and inspect a dataset
# ======================================================================
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")

print("shape:", df.shape)
print("columns:", list(df.columns))
print(df.head())
print()
df.info()

# ======================================================================
# Example 2 — First questions answered with pandas
# ======================================================================
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/servers.csv")

print(df.describe().round(1))
print()
print("Servers per environment:")
print(df["environment"].value_counts())
print()
print("Status counts:", df["status"].value_counts().to_dict())
print("Regions used:", sorted(df["region"].unique()), "| distinct:", df["region"].nunique())
print("Average CPU usage:", round(df["cpu_usage"].mean(), 1))
print("Total memory (GB):", df["memory_gb"].sum())
print()
print(df[["hostname", "cpu_usage", "status"]].head(3))
