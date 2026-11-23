"""
Day 090 — Data Cleaning and Handling Missing Values: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import numpy as np
import pandas as pd

pd.set_option("display.width", 120)

# ===== Task 1 =====
df = pd.DataFrame({"host": ["a", "b", "c", "d", "e"], "cpu": [50, None, 70, None, 30],
                   "owner": ["team1", None, "team2", "team3", None]})
report = pd.DataFrame({"missing": df.isna().sum(), "percent": (df.isna().mean() * 100).round(0)})
print(report)
df = df.dropna(subset=["cpu"])
df["owner"] = df["owner"].fillna("unknown")
print(df)

# ===== Task 2 =====
raw = pd.Series(["85", "90%", "n/a", "72.5", ""])
stripped = raw.str.rstrip("%")
numeric = pd.to_numeric(stripped, errors="coerce")
filled = numeric.fillna(numeric.median())
print(stripped.tolist())
print(numeric.tolist())
print(filled.tolist())

# ===== Task 3 =====
rng = np.random.default_rng(0)
houses = pd.read_csv("../../datasets/house_prices.csv")
damaged = houses.copy()
damaged.loc[rng.choice(len(damaged), 10, replace=False), "price"] = np.nan
damaged = pd.concat([damaged, damaged.iloc[:5]], ignore_index=True)
damaged.loc[rng.choice(len(houses), 3, replace=False), "bedrooms"] = -1


def clean_houses(df):
    df = df.copy()
    n = len(df)
    df = df.dropna(subset=["price"])
    print(f"dropped {n - len(df)} rows with missing price (label)")
    n = len(df)
    df = df.drop_duplicates()
    print(f"dropped {n - len(df)} duplicates")
    bad = df["bedrooms"] < 1
    df.loc[bad, "bedrooms"] = int(df.loc[~bad, "bedrooms"].median())
    print(f"fixed {bad.sum()} invalid bedroom values")
    assert df["price"].notna().all() and not df.duplicated().any() and (df["bedrooms"] >= 1).all()
    return df


print("damaged shape:", damaged.shape)
clean = clean_houses(damaged)
print("final shape:", clean.shape)
