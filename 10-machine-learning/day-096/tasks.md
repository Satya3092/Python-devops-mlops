# Day 096 — Practice Tasks: Classification and Model Evaluation

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Compute metrics manually

**Problem statement:** For actual `[1, 0, 1, 1, 0, 0, 1, 0]` and predicted `[1, 0, 0, 1, 0, 1, 1, 0]`, compute TP, FP, FN, TN, precision, recall and F1 by hand (with Python arithmetic) and compare with scikit-learn.

**Input requirements:** No user input required.

**Expected behavior:** Precision 0.75, recall 0.75, F1 0.75 both ways.

**Expected output:**

```text
TP=3 FP=1 FN=1 TN=3 precision=0.75 recall=0.75 f1=0.75
sklearn: precision=0.75 recall=0.75 f1=0.75
```

## Task 2 — Medium: Iris evaluation

**Problem statement:** Train a `DecisionTreeClassifier(max_depth=3)` on Iris (70/30, stratified, random_state 42) and print the confusion matrix and classification report.

**Input requirements:** No user input required.

**Expected behavior:** A 3×3 confusion matrix and per-class metrics.

**Expected output:**

```text
[[15  0  0]
 [ 0 14  1]
 [ 0  0 15]]
              precision    recall  f1-score   support

      setosa      1.000     1.000     1.000        15
  versicolor      1.000     0.933     0.966        15
   virginica      0.938     1.000     0.968        15

    accuracy                          0.978        45
   macro avg      0.979     0.978     0.978        45
weighted avg      0.979     0.978     0.978        45
```

## Task 3 — Practical Challenge: Pick the operating threshold

**Problem statement:** For the failure dataset and a logistic-regression pipeline, find the highest threshold (step 0.05 from 0.05 to 0.95) that still achieves **recall ≥ 0.85** on the test set. Print that threshold with its precision, recall and number of alerts, and save the model's metrics to `metrics.json`.

**Input requirements:** No user input required.

**Expected behavior:** The chosen threshold and a metrics file.

**Expected output:**

```text
threshold=0.45 precision=0.80 recall=0.89 alerts=20
{"threshold": 0.45, "precision": 0.8, "recall": 0.889}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
