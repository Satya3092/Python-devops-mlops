"""
Day 089 — Data Filtering, Sorting, and Grouping: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import pandas as pd

pd.set_option("display.width", 120)

# ===== Task 1 =====
houses = pd.read_csv("../../datasets/house_prices.csv")
mask = (houses["bedrooms"] >= 3) & (houses["distance_km"] < 10) & (houses["price"] < 400_000)
matches = houses[mask].sort_values("price")
print("matches:", len(matches))
print(matches.head())

# ===== Task 2 =====
sales = pd.read_csv("../../datasets/sales.csv", parse_dates=["date"])
sales["revenue"] = sales["units"] * sales["unit_price"]
print(sales.groupby("region")["revenue"].sum().sort_values(ascending=False))
print(sales.groupby("product")["units"].mean().round(1))
monthly = sales.groupby(sales["date"].dt.to_period("M"))["revenue"].sum()
print("Best month:", monthly.idxmax(), "with", monthly.max())

# ===== Task 3 =====
df = pd.read_csv("../../datasets/server_failures.csv")
df["error_band"] = pd.cut(df["error_count"], bins=[-1, 2, 5, 100], labels=["0-2", "3-5", "6+"])
by_errors = df.groupby("error_band", observed=True)["failure"].agg(failure_rate="mean", servers="count")
by_errors["failure_rate"] = (by_errors["failure_rate"] * 100).round(1)
print(by_errors)
bands = [0, 50, 80, 101]
labels = ["<50", "50-80", "80+"]
df["cpu_band"] = pd.cut(df["cpu_usage"], bins=bands, labels=labels, right=False)
df["mem_band"] = pd.cut(df["memory_usage"], bins=bands, labels=labels, right=False)
pivot = df.pivot_table(index="cpu_band", columns="mem_band", values="failure", aggfunc="mean", observed=True)
print((pivot * 100).round(1))
print("Insight: failures concentrate where errors are frequent and CPU and memory are both high.")
