# Day 095 — Practice Tasks: Linear Regression

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Build time predictor

**Problem statement:** Given lines changed `[50, 120, 200, 310, 400, 520]` and build minutes `[3.1, 4.0, 5.2, 6.4, 7.1, 8.6]`, fit a linear regression, print the slope and intercept and predict the build time for 750 lines.

**Input requirements:** No user input required.

**Expected behavior:** ~0.011 min per line and a prediction around 11 minutes.

**Expected output:**

```text
slope=0.0115 min/line intercept=2.67
750 lines -> 11.3 minutes
```

## Task 2 — Medium: Evaluate properly

**Problem statement:** Train the house-price model on 80 % of the data and print MAE, RMSE and R² on both train and test sets. Is it overfitting?

**Input requirements:** No user input required.

**Expected behavior:** Similar train and test scores → not overfitting.

**Expected output:**

```text
train: MAE=14,123 RMSE=18,441 R2=0.983
test: MAE=15,248 RMSE=19,831 R2=0.983
Scores are close -> the linear model is not overfitting.
```

## Task 3 — Practical Challenge: Cloud cost forecast

**Problem statement:** Simulate 12 months of cost where `cost = 2000 + 150*month + noise` (`default_rng(5)`, noise std 120). Fit a regression, print the monthly growth and forecast months 13–15, and print the month when cost first exceeds a 4,500 budget.

**Input requirements:** No user input required.

**Expected behavior:** Growth ≈ 150/month, forecasts and the budget-breach month.

**Expected output:**

```text
monthly growth: 158
month 13: 3,993
month 14: 4,151
month 15: 4,308
Budget of 4,500 exceeded in month 17
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
