"""
Day 087 — Pandas Series and DataFrames: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import pandas as pd

pd.set_option("display.width", 120)

# ===== Task 1 =====
staff = pd.DataFrame({"name": ["Asha", "Ravi", "Meera", "John"],
                      "team": ["devops", "data", "devops", "ml"],
                      "salary": [95000, 88000, 99000, 105000]})
print(staff)
print(staff.loc[staff["team"] == "devops", "name"].tolist())

# ===== Task 2 =====
houses = pd.read_csv("../../datasets/house_prices.csv")
houses["price_per_sqft"] = (houses["price"] / houses["size_sqft"]).round(2)
houses["age_group"] = pd.cut(houses["age_years"], bins=[-1, 9, 24, 200], labels=["new", "mid", "old"])
print(houses.head())
for group in ["new", "mid", "old"]:
    print(group, round(houses.loc[houses["age_group"] == group, "price_per_sqft"].mean(), 2))

# ===== Task 3 =====
df = pd.read_csv("../../datasets/servers.csv")
df["risk_score"] = 0.5 * df["cpu_usage"] + 0.3 * df["memory_usage"] + 0.2 * df["disk_usage"]
df["rank"] = df["risk_score"].rank(ascending=False).astype(int)
top = df.sort_values("rank").head(5)
print(top[["hostname", "environment", "risk_score", "rank"]].round(1).to_string(index=False))
for env in sorted(df["environment"].unique()):
    print(env, round(df.loc[df["environment"] == env, "risk_score"].mean(), 1))
