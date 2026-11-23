# Day 094 — Introduction to Scikit-Learn

[⬅ Day 093](../../10-machine-learning/day-093/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 095 ➡](../../10-machine-learning/day-095/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 10 — Machine Learning Fundamentals | 🔴 Advanced beginner (ML) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use scikit-learn's consistent estimator API: `fit`, `predict`, `score`, `transform`
- Preprocess data with scalers and encoders
- Chain preprocessing and a model in a `Pipeline` and evaluate with cross-validation

## 2. Topic Explanation

**scikit-learn** (`sklearn`) is the standard library for classic machine learning in Python. Its superpower is a **consistent API** — learn it once, use any algorithm:

| Method | Used on | Does |
|---|---|---|
| `fit(X, y)` | every estimator | learn from data |
| `predict(X)` | models | make predictions |
| `predict_proba(X)` | classifiers | class probabilities |
| `score(X, y)` | models | default metric (accuracy / R²) |
| `transform(X)` | preprocessors | change data (scale, encode) |
| `fit_transform(X)` | preprocessors | fit then transform (training data only!) |

Swapping `LogisticRegression()` for `RandomForestClassifier()` changes **one line** — polymorphism from Day 65!

**Preprocessing**
- `StandardScaler` — mean 0, std 1 per feature.
- `OneHotEncoder` — turns categories (`prod`, `dev`) into 0/1 columns.
- `ColumnTransformer` — different preprocessing for numeric and categorical columns.

**Pipeline** — glue preprocessing + model into one object:
- Prevents leakage (the scaler is fitted on training folds only).
- One object to `fit`, `predict`, **save** and **deploy** (Day 97–100).

**Cross-validation** (`cross_val_score`) — train/test on several different splits (folds) and average → a more reliable estimate than one split.

Built-in toy datasets (`load_iris`, `load_diabetes`) ship with scikit-learn, so they work offline.

> Install the ML libraries with `pip install numpy pandas scikit-learn matplotlib`. Examples use `random_state=42` so your numbers match the expected output (tiny differences can appear across library versions). Run from inside this day's folder so `../../datasets/` resolves.

## 3. Syntax

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

pipe = Pipeline([("scale", StandardScaler()), ("model", LogisticRegression())])
pipe.fit(X_train, y_train)
pipe.predict(X_test); pipe.score(X_test, y_test)
cross_val_score(pipe, X, y, cv=5)
```

| Part | Meaning |
|---|---|
| `estimator` | Any object with fit (+ predict or transform). |
| `Pipeline([(name, step), ...])` | Steps run in order; last is usually the model. |
| `ColumnTransformer` | Apply different transforms to different columns. |
| `cross_val_score(cv=5)` | 5-fold cross-validation scores. |

## 4. Example 1 — Basic Example: The fit / predict / score pattern on the Iris dataset

```python
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

iris = load_iris(as_frame=True)                   # bundled with scikit-learn, no download
X, y = iris.data, iris.target
print("Features:", list(X.columns))
print("Classes :", list(iris.target_names), "| samples:", len(X))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

for model in [KNeighborsClassifier(n_neighbors=5), LogisticRegression(max_iter=500), DecisionTreeClassifier(random_state=42)]:
    model.fit(X_train, y_train)                    # same API for every algorithm
    print(f"{type(model).__name__:<24} test accuracy = {model.score(X_test, y_test):.3f}")

flower = X_test.iloc[[0]]
best = LogisticRegression(max_iter=500).fit(X_train, y_train)
print("Prediction for first test flower:", iris.target_names[best.predict(flower)[0]],
      "| probabilities:", best.predict_proba(flower).round(3)[0].tolist())
```

## 5. Example 2 — Practical Example: Preprocessing + model in one Pipeline, with cross-validation

```python
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

df = pd.read_csv("../../datasets/server_failures.csv")
# add a categorical feature so we can practise encoding
df["environment"] = ["prod" if i % 3 == 0 else "staging" if i % 3 == 1 else "dev" for i in range(len(df))]
numeric = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
categorical = ["environment"]
X, y = df[numeric + categorical], df["failure"]

preprocess = ColumnTransformer([
    ("num", StandardScaler(), numeric),
    ("cat", OneHotEncoder(handle_unknown="ignore"), categorical),
])

for name, model in [("logistic_regression", LogisticRegression(max_iter=1000)),
                    ("random_forest", RandomForestClassifier(n_estimators=200, random_state=42))]:
    pipe = Pipeline([("preprocess", preprocess), ("model", model)])
    scores = cross_val_score(pipe, X, y, cv=5)
    print(f"{name:<20} 5-fold accuracy: {scores.mean():.3f} (+/- {scores.std():.3f})")

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
pipe = Pipeline([("preprocess", preprocess), ("model", LogisticRegression(max_iter=1000))]).fit(X_train, y_train)
print("Pipeline steps:", list(pipe.named_steps))
print("Encoded feature names:", list(pipe.named_steps["preprocess"].get_feature_names_out())[-3:])
new_server = pd.DataFrame([{"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7,
                            "response_time_ms": 650, "environment": "prod"}])
print("Failure probability for a stressed prod server:", round(pipe.predict_proba(new_server)[0, 1], 3))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `load_iris(as_frame=True)` gives a DataFrame of 4 flower measurements and 3 species.
- Three different algorithms are trained and scored with **identical code** — the estimator API.
- `predict_proba` shows how confident the model is for each class.

**Example 2**
- `ColumnTransformer` scales numeric columns and one-hot encodes the `environment` column.
- `Pipeline` chains preprocessing and the model. During cross-validation, the scaler is re-fitted on each training fold only → no leakage.
- `cross_val_score(cv=5)` trains/evaluates 5 times on different splits; mean ± std is more trustworthy than a single split.
- The fitted pipeline accepts **raw** data (including the text column) for prediction — exactly what you'll deploy behind an API.

## 7. Expected Output

**Example 1:**

```text
Features: ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
Classes : [np.str_('setosa'), np.str_('versicolor'), np.str_('virginica')] | samples: 150
KNeighborsClassifier     test accuracy = 0.978
LogisticRegression       test accuracy = 0.933
DecisionTreeClassifier   test accuracy = 0.933
Prediction for first test flower: virginica | probabilities: [0.0, 0.032, 0.968]
```

**Example 2:**

```text
logistic_regression  5-fold accuracy: 0.897 (+/- 0.012)
random_forest        5-fold accuracy: 0.863 (+/- 0.016)
Pipeline steps: ['preprocess', 'model']
Encoded feature names: ['cat__environment_dev', 'cat__environment_prod', 'cat__environment_staging']
Failure probability for a stressed prod server: 0.998
```

## 8. Common Mistakes

**1. `fit_transform` on test data**

Fitting the scaler on test data leaks information. Fit on train, `transform` test — or let a Pipeline handle it.

**2. Unscaled features for distance/linear models**

KNN, SVM, logistic regression work better with scaled features. Tree models don't need scaling.

**3. Different preprocessing at serving time**

Save and deploy the whole Pipeline, not just the model.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Your first model:** Train a `KNeighborsClassifier(n_neighbors=3)` on Iris (75/25 split, random_state 1) and print its test accuracy and the prediction for the measurements `[5.9, 3.0, 5.1, 1.8]`.
- **Task 2 (Medium) — Scaler by hand:** Fit a `StandardScaler` on `[[10], [20], [30]]`, print `mean_` and `scale_`, transform `[[20], [40]]` and verify the result manually with `(x - mean) / std`.
- **Task 3 (Practical Challenge) — Model comparison pipeline:** Using `server_failures.csv`, compare `LogisticRegression`, `DecisionTreeClassifier(max_depth=4)` and `RandomForestClassifier(n_estimators=100)` inside pipelines with `StandardScaler`, using 5-fold cross-validation. Print a ranked table and the winner.

## 10. DevOps/MLOps Connection

- **DevOps parallel:** a scikit-learn Pipeline is like a Docker image for your model — preprocessing and model packaged together so "it works on my machine" also works in production.
- **MLOps:** the fitted Pipeline is the artefact you version, save (Day 97), serve (Day 98) and containerise (Day 99). Cross-validation scores become quality gates in CI.
- **AIOps:** the same API powers anomaly detection and incident prediction models on operational data.

## 11. Interview Questions

**Q1. What is the scikit-learn estimator API?**

<details><summary>Show answer</summary>

A consistent interface: `fit` to learn, `predict`/`predict_proba` for models, `transform` for preprocessors, `score` for default evaluation.

</details>

**Q2. Why use a Pipeline?**

<details><summary>Show answer</summary>

It bundles preprocessing and the model, prevents leakage during cross-validation and guarantees identical processing at training and inference time.

</details>

**Q3. What is k-fold cross-validation?**

<details><summary>Show answer</summary>

Splitting data into k folds, training on k−1 and testing on the remaining fold k times, then averaging the scores for a more robust estimate.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 94 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 093](../../10-machine-learning/day-093/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 095 ➡](../../10-machine-learning/day-095/README.md)
