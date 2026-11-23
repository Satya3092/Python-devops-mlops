# Day 095 — Linear Regression

[⬅ Day 094](../../10-machine-learning/day-094/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 096 ➡](../../10-machine-learning/day-096/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 10 — Machine Learning Fundamentals | 🔴 Advanced beginner (ML) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Understand linear regression: coefficients, intercept and the line of best fit
- Train a regression model to predict house prices and interpret its coefficients
- Evaluate regression with MAE, RMSE and R², and visualise predictions

## 2. Topic Explanation

**Linear regression** predicts a number by drawing the "best" straight line (or plane, with many features) through the data:

```
price = intercept + coef_1 × size + coef_2 × bedrooms + coef_3 × age + coef_4 × distance
```

- **Coefficients** — how much the prediction changes when a feature increases by 1 (holding others constant). A negative coefficient for `age_years` means older houses are cheaper.
- **Intercept** — the prediction when all features are 0 (a mathematical anchor).
- "Best" = minimises the sum of **squared errors** between predictions and true values (*ordinary least squares*).

**Regression metrics**

| Metric | Meaning | Good when |
|---|---|---|
| **MAE** (mean absolute error) | average size of the mistake, in the label's units | small |
| **RMSE** (root mean squared error) | like MAE but punishes big mistakes more | small |
| **R²** (coefficient of determination) | share of variance explained (1 = perfect, 0 = no better than predicting the mean) | close to 1 |

Always compare with a **baseline** (e.g. always predict the average price).

DevOps examples: forecast disk usage growth, predict build duration from lines changed, estimate monthly cloud cost from traffic.

> Install the ML libraries with `pip install numpy pandas scikit-learn matplotlib`. Examples use `random_state=42` so your numbers match the expected output (tiny differences can appear across library versions). Run from inside this day's folder so `../../datasets/` resolves.

## 3. Syntax

```python
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
model = LinearRegression().fit(X_train, y_train)
model.coef_, model.intercept_
y_pred = model.predict(X_test)
mean_absolute_error(y_test, y_pred); mean_squared_error(y_test, y_pred) ** 0.5; r2_score(y_test, y_pred)
```

| Part | Meaning |
|---|---|
| `LinearRegression()` | Ordinary least-squares linear model. |
| `coef_ / intercept_` | Learned weights per feature and the constant. |
| `MAE / RMSE` | Average error in label units. |
| `R²` | Fraction of variance explained. |

## 4. Example 1 — Basic Example: One feature: disk usage growth forecast

```python
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
```

## 5. Example 2 — Practical Example: Multiple features: predicting house prices

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Features must be 2-D, so `reshape(-1, 1)` turns 14 days into a 14×1 matrix.
- The coefficient is the daily growth; solving `intercept + coef × day = 500` predicts when the disk fills up — **predictive capacity planning**.

**Example 2**
- Four features predict price. Coefficients are interpretable: e.g. each extra sqft adds ~150, each year of age subtracts ~1,200 (the dataset generator used similar values — the model recovered them).
- MAE/RMSE are compared to a **baseline** that always predicts the average price; R² ≈ 0.95 means the model explains ~95 % of the price variation.
- The actual-vs-predicted plot should hug the red diagonal.

## 7. Expected Output

**Example 1:**

```text
growth per day: 4.29 GB | intercept: 405.2 GB
R² on history: 0.9975
day 21: predicted 495 GB
day 28: predicted 525 GB
Disk predicted to be full around day 22 -> plan the expansion now!
```

**Example 2:**

```text
Coefficients (price change per +1 unit):
  size_sqft           149
  bedrooms         11,073
  age_years        -1,185
  distance_km      -2,242
  intercept        45,728
MAE :     15,248   (baseline 129,579)
RMSE:     19,831
R²  :      0.983
Predicted price for a 1800 sqft, 3-bed, 5-year-old house 8 km out: 323,389
Saved actual_vs_predicted.png
```

## 8. Common Mistakes

**1. 1-D X**

`model.fit(days, y)` with a 1-D `days` raises `ValueError: Expected 2D array`. Use `reshape(-1, 1)` or a DataFrame.

**2. Extrapolating too far**

A line fitted on 14 days may not hold for 6 months (growth can accelerate). Re-train regularly.

**3. Reading coefficients of unscaled, correlated features as 'importance'**

Coefficients depend on units and correlations (size and bedrooms move together). Interpret carefully.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Build time predictor:** Given lines changed `[50, 120, 200, 310, 400, 520]` and build minutes `[3.1, 4.0, 5.2, 6.4, 7.1, 8.6]`, fit a linear regression, print the slope and intercept and predict the build time for 750 lines.
- **Task 2 (Medium) — Evaluate properly:** Train the house-price model on 80 % of the data and print MAE, RMSE and R² on both train and test sets. Is it overfitting?
- **Task 3 (Practical Challenge) — Cloud cost forecast:** Simulate 12 months of cost where `cost = 2000 + 150*month + noise` (`default_rng(5)`, noise std 120). Fit a regression, print the monthly growth and forecast months 13–15, and print the month when cost first exceeds a 4,500 budget.

## 10. DevOps/MLOps Connection

- **DevOps / SRE:** capacity forecasting (disk, memory, traffic), predicting build/test durations to optimise CI, estimating cost growth.
- **Cloud FinOps:** regression on usage and cost data drives budgets and reserved-instance decisions.
- **MLOps:** regression models are common in production (demand, pricing, ETA). You'll monitor their MAE in production and retrain when it drifts.

## 11. Interview Questions

**Q1. What do the coefficients of a linear regression mean?**

<details><summary>Show answer</summary>

The expected change in the prediction for a one-unit increase in that feature, holding other features constant.

</details>

**Q2. What is the difference between MAE and RMSE?**

<details><summary>Show answer</summary>

Both measure average error in label units; RMSE squares errors before averaging, so it penalises large errors more.

</details>

**Q3. What does an R² of 0 mean?**

<details><summary>Show answer</summary>

The model explains none of the variance — it's no better than always predicting the mean (negative values mean worse).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 95 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 094](../../10-machine-learning/day-094/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 096 ➡](../../10-machine-learning/day-096/README.md)
