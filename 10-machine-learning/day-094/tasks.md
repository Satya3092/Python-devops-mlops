# Day 094 — Practice Tasks: Introduction to Scikit-Learn

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Your first model

**Problem statement:** Train a `KNeighborsClassifier(n_neighbors=3)` on Iris (75/25 split, random_state 1) and print its test accuracy and the prediction for the measurements `[5.9, 3.0, 5.1, 1.8]`.

**Input requirements:** No user input required.

**Expected behavior:** Accuracy and the predicted species name.

**Expected output:**

```text
accuracy: 1.0
prediction: virginica
```

## Task 2 — Medium: Scaler by hand

**Problem statement:** Fit a `StandardScaler` on `[[10], [20], [30]]`, print `mean_` and `scale_`, transform `[[20], [40]]` and verify the result manually with `(x - mean) / std`.

**Input requirements:** No user input required.

**Expected behavior:** `[[0.0], [2.449...]]` both ways.

**Expected output:**

```text
mean: [20.] scale: [8.16496581]
[[0.        ]
 [2.44948974]]
[[0.        ]
 [2.44948974]]
```

## Task 3 — Practical Challenge: Model comparison pipeline

**Problem statement:** Using `server_failures.csv`, compare `LogisticRegression`, `DecisionTreeClassifier(max_depth=4)` and `RandomForestClassifier(n_estimators=100)` inside pipelines with `StandardScaler`, using 5-fold cross-validation. Print a ranked table and the winner.

**Input requirements:** No user input required.

**Expected behavior:** A ranked table of three models.

**Expected output:**

```text
1. LogisticRegression       0.903
2. RandomForestClassifier   0.882
3. DecisionTreeClassifier   0.850
Winner: LogisticRegression
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
