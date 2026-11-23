"""
Day 095 — Linear Regression
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — One feature: disk usage growth forecast
# ======================================================================
import numpy as np
from sklearn.linear_model import LinearRegression

days = np.arange(1, 15).reshape(-1, 1)                    # X must be 2-D: (samples, features)
disk_used_gb = np.array([410, 414, 419, 421, 427, 430, 436, 438, 445, 447, 452, 457, 461, 466])

model = LinearRegression().fit(days, disk_used_gb)
print(f"growth per day: {model.coef_[0]:.2f} GB | intercept: {model.intercept_:.1f} GB")
print("R² on history:", round(model.score(days, disk_used_gb), 4))

capacity_gb = 500
for future_day in (21, 28):
    print(f"day {future_day}: predicted {model.predict([[future_day]])[0]:.0f} GB")
day_full = (capacity_gb - model.intercept_) / model.coef_[0]
print(f"Disk predicted to be full around day {day_full:.0f} -> plan the expansion now!")

# ======================================================================
# Example 2 — Multiple features: predicting house prices
# ======================================================================
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../datasets/house_prices.csv")
X = df[["size_sqft", "bedrooms", "age_years", "distance_km"]]
y = df["price"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression().fit(X_train, y_train)
print("Coefficients (price change per +1 unit):")
for feature, coef in zip(X.columns, model.coef_):
    print(f"  {feature:<12} {coef:>10,.0f}")
print(f"  intercept    {model.intercept_:>10,.0f}")

y_pred = model.predict(X_test)
baseline = [y_train.mean()] * len(y_test)
print(f"MAE : {mean_absolute_error(y_test, y_pred):>10,.0f}   (baseline {mean_absolute_error(y_test, baseline):,.0f})")
print(f"RMSE: {mean_squared_error(y_test, y_pred) ** 0.5:>10,.0f}")
print(f"R²  : {r2_score(y_test, y_pred):>10.3f}")

house = pd.DataFrame([{"size_sqft": 1800, "bedrooms": 3, "age_years": 5, "distance_km": 8}])
print(f"Predicted price for a 1800 sqft, 3-bed, 5-year-old house 8 km out: {model.predict(house)[0]:,.0f}")

plt.figure(figsize=(5, 5))
plt.scatter(y_test, y_pred, alpha=0.7)
plt.plot([y.min(), y.max()], [y.min(), y.max()], "r--", label="perfect prediction")
plt.xlabel("actual price"); plt.ylabel("predicted price"); plt.legend(); plt.tight_layout()
plt.savefig("actual_vs_predicted.png", dpi=100)
print("Saved actual_vs_predicted.png")
