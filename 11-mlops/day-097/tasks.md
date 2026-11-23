# Day 097 — Practice Tasks: Saving and Loading ML Models using Pickle/Joblib

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Save and reload

**Problem statement:** Train a `DecisionTreeClassifier(max_depth=3)` on Iris, save it with joblib to `iris_tree.joblib`, reload it, and print predictions for the first 3 rows from both models.

**Input requirements:** No user input required.

**Expected behavior:** Identical predictions.

**Expected output:**

```text
[0, 0, 0] [0, 0, 0]
```

## Task 2 — Medium: Model registry folder

**Problem statement:** Train two versions of a regression model on `house_prices.csv` (v1 with `size_sqft` only, v2 with all features). Save each as `registry/house-v<N>.joblib` with metrics (R² on a test split). Write `latest_best(registry)` that loads every bundle and returns the version with the best R².

**Input requirements:** No user input required.

**Expected behavior:** v2 is selected as best.

**Expected output:**

```text
saved v1 r2=0.964
saved v2 r2=0.983
best version: 2 r2: 0.9833
```

## Task 3 — Practical Challenge: Prediction CLI

**Problem statement:** Write a function `predict_from_file(model_path, csv_path)` that loads a saved failure-model bundle (create it in the solution), reads a CSV of new servers, validates that all required feature columns exist (raise `ValueError` otherwise), and writes `predictions.csv` with probability and failure columns. Print the result.

**Input requirements:** No user input required.

**Expected behavior:** A predictions table for 3 servers.

**Expected output:**

```text
       host  probability  failure
0    web-01        0.000    False
1     db-01        1.000     True
2  cache-01        0.701     True
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
