# Day 096 — Classification and Model Evaluation

[⬅ Day 095](../../10-machine-learning/day-095/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 097 ➡](../../11-mlops/day-097/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 10 — Machine Learning Fundamentals | 🔴 Advanced beginner (ML) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Train classifiers (logistic regression, random forest) to predict server failures
- Evaluate with a confusion matrix, accuracy, precision, recall, F1 and ROC AUC
- Choose a decision threshold based on the business cost of mistakes

## 2. Topic Explanation

**Classification** predicts a category. For binary problems (failure yes/no) models usually output a **probability**, and a **threshold** (default 0.5) turns it into a decision.

**Why accuracy is not enough:** if only 18 % of servers fail, a model that *always* says "no failure" is 82 % accurate — and useless.

**Confusion matrix**

| | Predicted no | Predicted yes |
|---|---|---|
| **Actual no** | True Negative (TN) | False Positive (FP) — false alarm |
| **Actual yes** | False Negative (FN) — missed failure | True Positive (TP) |

**Metrics**
- **Accuracy** = (TP + TN) / all
- **Precision** = TP / (TP + FP) — "when we alert, how often is it real?" (low precision = alert fatigue)
- **Recall** = TP / (TP + FN) — "of the real failures, how many did we catch?" (low recall = missed incidents)
- **F1** = harmonic mean of precision and recall
- **ROC AUC** — how well the model *ranks* positives above negatives across all thresholds (0.5 random, 1.0 perfect)

**The threshold is a business decision.** For outage prediction a missed failure (FN) is expensive → lower the threshold to raise recall, accepting more false alarms. For auto-remediation that reboots servers, false positives are costly → raise the threshold for precision.

Analogy: a smoke detector. High recall = never misses a fire but beeps at toast. High precision = only beeps for real fires but might miss one.

> Install the ML libraries with `pip install numpy pandas scikit-learn matplotlib`. Examples use `random_state=42` so your numbers match the expected output (tiny differences can appear across library versions). Run from inside this day's folder so `../../datasets/` resolves.

## 3. Syntax

```python
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             confusion_matrix, classification_report, roc_auc_score)
y_pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]
custom = (proba >= 0.3).astype(int)            # custom threshold
confusion_matrix(y_test, y_pred); classification_report(y_test, y_pred)
roc_auc_score(y_test, proba)
```

| Part | Meaning |
|---|---|
| `predict_proba[:, 1]` | Probability of the positive class. |
| `threshold` | Probability cut-off for predicting 1. |
| `confusion_matrix` | [[TN, FP], [FN, TP]]. |
| `classification_report` | Precision/recall/F1 per class. |
| `roc_auc_score` | Threshold-independent ranking quality. |

## 4. Example 1 — Basic Example: Metrics by hand: why accuracy can lie

```python
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score

actual = [0, 0, 0, 0, 0, 0, 0, 0, 1, 1]           # 2 real failures out of 10
lazy_model = [0] * 10                              # always "no failure"
alert_model = [0, 0, 0, 0, 0, 1, 1, 0, 1, 1]       # catches both, 2 false alarms

for name, predicted in [("lazy", lazy_model), ("alerting", alert_model)]:
    tn, fp, fn, tp = confusion_matrix(actual, predicted).ravel()
    print(f"{name:<9} TN={tn} FP={fp} FN={fn} TP={tp} | "
          f"accuracy={accuracy_score(actual, predicted):.2f} "
          f"precision={precision_score(actual, predicted, zero_division=0):.2f} "
          f"recall={recall_score(actual, predicted):.2f} "
          f"f1={f1_score(actual, predicted, zero_division=0):.2f}")
print("The lazy model is 80% accurate but catches 0 failures (recall 0.00)!")
```

## 5. Example 2 — Practical Example: Predicting server failures and choosing a threshold

```python
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, precision_score, recall_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../../datasets/server_failures.csv")
X, y = df.drop(columns=["failure"]), df["failure"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

models = {
    "logistic_regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)),
    "random_forest": RandomForestClassifier(n_estimators=300, max_depth=6, random_state=42),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    proba = model.predict_proba(X_test)[:, 1]
    print(f"{name:<20} ROC AUC = {roc_auc_score(y_test, proba):.3f}")

best = models["logistic_regression"]
proba = best.predict_proba(X_test)[:, 1]
print("\nDefault threshold 0.5:")
print(confusion_matrix(y_test, best.predict(X_test)))
print(classification_report(y_test, best.predict(X_test), target_names=["ok", "failure"], digits=3))

print("Threshold trade-off (missed failure = expensive):")
print(f"{'threshold':>9} {'precision':>9} {'recall':>7} {'alerts':>7} {'missed':>7}")
for threshold in (0.2, 0.3, 0.5, 0.7):
    pred = (proba >= threshold).astype(int)
    missed = int(((pred == 0) & (y_test == 1)).sum())
    print(f"{threshold:>9} {precision_score(y_test, pred, zero_division=0):>9.2f} "
          f"{recall_score(y_test, pred):>7.2f} {pred.sum():>7} {missed:>7}")

importances = pd.Series(models["random_forest"].feature_importances_, index=X.columns).sort_values(ascending=False)
print("\nRandom forest feature importance:", importances.round(3).to_dict())
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `confusion_matrix(...).ravel()` returns TN, FP, FN, TP.
- The lazy model reaches 80 % accuracy while catching **zero** failures — recall exposes it.
- The alerting model has lower precision (false alarms) but perfect recall.

**Example 2**
- Both models output probabilities; **ROC AUC** compares how well they rank risky servers, independent of any threshold.
- `classification_report` prints precision/recall/F1 per class.
- The threshold table shows the trade-off: lowering the threshold catches more failures (higher recall, fewer missed) at the price of more alerts (lower precision). Pick the row that matches the business cost — e.g. 0.3 for an early-warning system.
- `feature_importances_` shows which metrics the forest relies on most (errors, memory, CPU...).

## 7. Expected Output

**Example 1:**

```text
lazy      TN=8 FP=0 FN=2 TP=0 | accuracy=0.80 precision=0.00 recall=0.00 f1=0.00
alerting  TN=6 FP=2 FN=0 TP=2 | accuracy=0.80 precision=0.50 recall=1.00 f1=0.67
The lazy model is 80% accurate but catches 0 failures (recall 0.00)!
```

**Example 2:**

```text
logistic_regression  ROC AUC = 0.981
random_forest        ROC AUC = 0.951

Default threshold 0.5:
[[78  4]
 [ 3 15]]
              precision    recall  f1-score   support

          ok      0.963     0.951     0.957        82
     failure      0.789     0.833     0.811        18

    accuracy                          0.930       100
   macro avg      0.876     0.892     0.884       100
weighted avg      0.932     0.930     0.931       100

Threshold trade-off (missed failure = expensive):
threshold precision  recall  alerts  missed
      0.2      0.67    1.00      27       0
      0.3      0.70    0.89      23       2
      0.5      0.79    0.83      19       3
      0.7      0.92    0.61      12       7

Random forest feature importance: {'memory_usage': 0.28, 'cpu_usage': 0.268, 'disk_usage': 0.228, 'error_count': 0.118, 'response_time_ms': 0.107}
```

## 8. Common Mistakes

**1. Reporting only accuracy on imbalanced data**

Always look at precision, recall and the confusion matrix.

**2. Keeping the default 0.5 threshold blindly**

Choose the threshold from business costs (missed incident vs false alarm) on validation data.

**3. Tuning on the test set**

If you pick the threshold or hyper-parameters by looking at the test set repeatedly, it stops being an honest estimate. Use a validation set or cross-validation.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Compute metrics manually:** For actual `[1, 0, 1, 1, 0, 0, 1, 0]` and predicted `[1, 0, 0, 1, 0, 1, 1, 0]`, compute TP, FP, FN, TN, precision, recall and F1 by hand (with Python arithmetic) and compare with scikit-learn.
- **Task 2 (Medium) — Iris evaluation:** Train a `DecisionTreeClassifier(max_depth=3)` on Iris (70/30, stratified, random_state 42) and print the confusion matrix and classification report.
- **Task 3 (Practical Challenge) — Pick the operating threshold:** For the failure dataset and a logistic-regression pipeline, find the highest threshold (step 0.05 from 0.05 to 0.95) that still achieves **recall ≥ 0.85** on the test set. Print that threshold with its precision, recall and number of alerts, and save the model's metrics to `metrics.json`.

## 10. DevOps/MLOps Connection

- **DevOps / SRE:** alerting is a classification problem — precision = alert quality, recall = coverage. The same trade-off you tune in Prometheus rules appears in ML thresholds.
- **AIOps:** failure prediction, incident severity classification and change-risk scoring ("will this deployment fail?").
- **MLOps:** these metrics become **quality gates** in CI ("deploy only if recall ≥ 0.85 and AUC ≥ 0.9") and are monitored in production to detect model decay.

## 11. Interview Questions

**Q1. Explain precision and recall.**

<details><summary>Show answer</summary>

Precision is the fraction of positive predictions that were correct; recall is the fraction of actual positives the model found.

</details>

**Q2. Why can accuracy be misleading?**

<details><summary>Show answer</summary>

On imbalanced data a model can achieve high accuracy by always predicting the majority class while missing every positive case.

</details>

**Q3. How do you choose a classification threshold?**

<details><summary>Show answer</summary>

Based on the business cost of false positives vs false negatives, using validation data and precision–recall trade-offs (not the test set).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 96 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 095](../../10-machine-learning/day-095/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 097 ➡](../../11-mlops/day-097/README.md)
