# Day 093 — Features, Labels, Training Data, and Testing Data

[⬅ Day 092](../../10-machine-learning/day-092/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 094 ➡](../../10-machine-learning/day-094/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 10 — Machine Learning Fundamentals | 🔴 Advanced beginner (ML) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Identify features (X) and labels (y) in a dataset
- Split data into training and testing sets with `train_test_split` (and stratify)
- Explain overfitting, underfitting and data leakage

## 2. Topic Explanation

**Vocabulary you'll use every day in ML:**

| Term | Meaning | Server-failure example |
|---|---|---|
| **Dataset** | the table of examples | `server_failures.csv` |
| **Sample / row** | one example | one server at one moment |
| **Feature (X)** | an input column | cpu_usage, memory_usage, error_count |
| **Label / target (y)** | what we want to predict | failure (0/1) |
| **Training data** | rows the model learns from | ~80 % |
| **Testing data** | rows held back to evaluate | ~20 % |
| **Prediction** | the model's output for new X | failure = 1 |

**Why split?** A student who memorises last year's exam answers gets 100 % on that exam but fails a new one. Evaluating a model on the data it trained on is the same mistake. The **test set** simulates new, unseen data.

**Overfitting** — the model memorises training data (great train score, poor test score). **Underfitting** — the model is too simple (poor on both). The goal is good performance on **unseen** data (*generalisation*).

**Data leakage** — information from the test set or from the future sneaks into training (e.g. scaling with statistics computed on all data, or a feature that is only known *after* the failure). It produces unrealistically good scores that collapse in production.

`train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)`:
- `random_state` makes the split reproducible.
- `stratify=y` keeps the same class proportions in both sets (important when failures are rare).

> Install the ML libraries with `pip install numpy pandas scikit-learn matplotlib`. Examples use `random_state=42` so your numbers match the expected output (tiny differences can appear across library versions). Run from inside this day's folder so `../../datasets/` resolves.

## 3. Syntax

```python
from sklearn.model_selection import train_test_split
X = df[feature_columns]
y = df["label"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

| Part | Meaning |
|---|---|
| `X` | Features (2-D: rows × columns). |
| `y` | Label (1-D). |
| `test_size` | Fraction kept for testing. |
| `random_state` | Seed for a reproducible shuffle. |
| `stratify=y` | Keep class balance identical in train and test. |

## 4. Example 1 — Basic Example: Features, labels and a stratified split

```python
import pandas as pd
from sklearn.model_selection import train_test_split

df = pd.read_csv("../../datasets/server_failures.csv")
feature_columns = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
X = df[feature_columns]
y = df["failure"]
print("X shape:", X.shape, "| y shape:", y.shape)
print("Class balance (all):", y.value_counts(normalize=True).round(3).to_dict())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print("Train:", X_train.shape, "Test:", X_test.shape)
print("Failure rate train/test:", round(y_train.mean(), 3), "/", round(y_test.mean(), 3))
print("No overlap between sets:", set(X_train.index).isdisjoint(X_test.index))
print(X_train.head(3))
```

## 5. Example 2 — Practical Example: Overfitting vs underfitting in action

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

df = pd.read_csv("../../datasets/server_failures.csv")
X = df[["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]]
y = df["failure"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

print(f"{'max_depth':>9} {'train acc':>10} {'test acc':>9}  verdict")
for depth in [1, 3, 5, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=42).fit(X_train, y_train)
    train_acc = tree.score(X_train, y_train)
    test_acc = tree.score(X_test, y_test)
    gap = train_acc - test_acc
    verdict = "overfitting (memorised)" if gap > 0.1 else "underfitting?" if train_acc < 0.85 else "good balance"
    print(f"{str(depth):>9} {train_acc:>10.3f} {test_acc:>9.3f}  {verdict}")

baseline = max(y_test.mean(), 1 - y_test.mean())
print(f"Baseline (always predict 'no failure'): {baseline:.3f}  <- any model must beat this")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `X` (5 feature columns) and `y` (the `failure` label) are separated explicitly.
- `stratify=y` keeps the ~18 % failure rate identical in train and test.
- The index sets don't overlap: no test row was seen during training.

**Example 2**
- A depth-1 tree is too simple (underfits).
- An unlimited tree (`max_depth=None`) scores **1.0 on training data** but much lower on test data — it memorised noise (overfitting).
- A medium depth balances both. Choosing such settings is **hyper-parameter tuning**.
- The **baseline** (always predicting the majority class) shows why accuracy alone can mislead on imbalanced data (Day 96 covers better metrics).

## 7. Expected Output

**Example 1:**

```text
X shape: (400, 5) | y shape: (400,)
Class balance (all): {0: 0.815, 1: 0.185}
Train: (320, 5) Test: (80, 5)
Failure rate train/test: 0.184 / 0.188
No overlap between sets: True
     cpu_usage  memory_usage  disk_usage  error_count  response_time_ms
192       25.4          99.1        90.4            3               281
297       22.9          49.6        65.1            5               340
280       38.1          86.5        97.0            4               140
```

**Example 2:**

```text
max_depth  train acc  test acc  verdict
        1      0.813     0.820  underfitting?
        3      0.903     0.840  good balance
        5      0.963     0.870  good balance
     None      1.000     0.850  overfitting (memorised)
Baseline (always predict 'no failure'): 0.820  <- any model must beat this
```

## 8. Common Mistakes

**1. Evaluating on training data**

Training accuracy is optimistic. Always report test (or cross-validation) scores.

**2. Data leakage**

Fitting a scaler/encoder on the whole dataset or using future information as a feature leaks test information. Fit preprocessing on the training set only (pipelines on Day 100 do this for you).

**3. Unstratified splits for rare classes**

With rare failures, a random split can leave very few positives in the test set. Use `stratify=y`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Pick X and y:** For `house_prices.csv`, define X as every column except `price` and y as `price`. Print the feature names, X shape and the first 3 labels.
- **Task 2 (Medium) — Split and verify:** Split the house data 70/30 with `random_state=7`. Print the sizes, the mean price in each split and verify no index appears in both.
- **Task 3 (Practical Challenge) — Leakage detective:** Add a leaky feature to the failure dataset: `incident_ticket_opened = failure` (only known after a failure!). Train a depth-3 tree with and without it and compare test accuracy. Print a warning explaining why the leaky model would fail in production.

## 10. DevOps/MLOps Connection

- **DevOps analogy:** train/test split is like staging vs production — you validate on something the code (model) hasn't "seen".
- **Data engineering:** feature pipelines must only use information available **at prediction time** (point-in-time correctness) — the root of many leakage bugs.
- **MLOps:** reproducible splits (`random_state`, versioned datasets) let CI re-train and compare models fairly; evaluation on a held-out set is the quality gate before deployment.

## 11. Interview Questions

**Q1. What are features and labels?**

<details><summary>Show answer</summary>

Features are the input variables used to make a prediction; the label (target) is the value the model learns to predict.

</details>

**Q2. Why do we need a separate test set?**

<details><summary>Show answer</summary>

To estimate performance on unseen data; training-set scores are biased because the model has already seen those examples.

</details>

**Q3. What is data leakage? Give an example.**

<details><summary>Show answer</summary>

When information unavailable at prediction time (test data or future information) influences training, e.g. fitting a scaler on the full dataset or using a post-outcome field as a feature.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 93 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 092](../../10-machine-learning/day-092/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 094 ➡](../../10-machine-learning/day-094/README.md)
