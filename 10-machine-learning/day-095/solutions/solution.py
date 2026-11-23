"""
Day 095 — Linear Regression: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

# ===== Task 1 =====
lines = np.array([50, 120, 200, 310, 400, 520]).reshape(-1, 1)
minutes = np.array([3.1, 4.0, 5.2, 6.4, 7.1, 8.6])
m = LinearRegression().fit(lines, minutes)
print(f"slope={m.coef_[0]:.4f} min/line intercept={m.intercept_:.2f}")
print(f"750 lines -> {m.predict([[750]])[0]:.1f} minutes")

# ===== Task 2 =====
df = pd.read_csv("../../datasets/house_prices.csv")
X, y = df.drop(columns=["price"]), df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LinearRegression().fit(X_train, y_train)
for name, Xs, ys in [("train", X_train, y_train), ("test", X_test, y_test)]:
    p = model.predict(Xs)
    print(f"{name}: MAE={mean_absolute_error(ys, p):,.0f} RMSE={mean_squared_error(ys, p) ** 0.5:,.0f} R2={r2_score(ys, p):.3f}")
print("Scores are close -> the linear model is not overfitting.")

# ===== Task 3 =====
rng = np.random.default_rng(5)
months = np.arange(1, 13).reshape(-1, 1)
cost = 2000 + 150 * months.ravel() + rng.normal(0, 120, 12)
f = LinearRegression().fit(months, cost)
print(f"monthly growth: {f.coef_[0]:.0f}")
for month in (13, 14, 15):
    print(f"month {month}: {f.predict([[month]])[0]:,.0f}")
breach = next(m for m in range(13, 61) if f.predict([[m]])[0] > 4500)
print("Budget of 4,500 exceeded in month", breach)
