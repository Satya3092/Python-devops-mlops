"""
Day 086 — Pandas Introduction: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import pandas as pd

pd.set_option("display.width", 120)
houses = pd.read_csv("../../datasets/house_prices.csv")

# ===== Task 1 =====
print(houses.shape)
print(list(houses.columns))
print(houses.head(3))
print(houses.dtypes)

# ===== Task 2 =====
print("mean:", round(houses["price"].mean()), "median:", houses["price"].median(), "max:", houses["price"].max())
print(houses["bedrooms"].value_counts().sort_index())

# ===== Task 3 =====
df = pd.read_csv("../../datasets/servers.csv")
print("Critical servers:", (df["status"] == "critical").sum())
print("Highest CPU:", df.loc[df["cpu_usage"].idxmax(), "hostname"])
for env in sorted(df["environment"].unique()):
    print(f"  avg disk {env}: {df[df['environment'] == env]['disk_usage'].mean():.1f}%")
print(f"Healthy: {(df['status'] == 'healthy').mean() * 100:.0f}%")
