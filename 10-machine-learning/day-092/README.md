# Day 092 — Supervised vs Unsupervised Learning

[⬅ Day 091](../../10-machine-learning/day-091/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 093 ➡](../../10-machine-learning/day-093/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 10 — Machine Learning Fundamentals | 🔴 Advanced beginner (ML) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Distinguish supervised (labelled) and unsupervised (unlabelled) learning
- Recognise regression vs classification within supervised learning
- Apply a clustering algorithm (K-Means) and an anomaly detector to server data

## 2. Topic Explanation

**Supervised learning** — you have **labels** (the right answers) for past examples. The model learns the mapping *inputs → label*.
- **Regression**: the label is a **number** (house price, next hour's traffic, disk usage in 7 days).
- **Classification**: the label is a **category** (failure / no failure, spam / not spam, severity 1–4).

**Unsupervised learning** — **no labels**. The model finds structure by itself.
- **Clustering**: group similar items (servers with similar usage patterns, similar log messages). Algorithm: K-Means.
- **Anomaly detection**: find unusual points (a server behaving unlike all others). Algorithm: Isolation Forest.
- **Dimensionality reduction**: compress many features into few (PCA) for visualisation.

| | Supervised | Unsupervised |
|---|---|---|
| Needs labels? | Yes | No |
| Goal | Predict a known target | Discover structure |
| Examples | failure prediction, price | grouping servers, anomalies |
| Evaluation | compare with true labels | harder: domain judgement |

(Other families: **reinforcement learning** — an agent learns by trial and reward, e.g. autoscaling policies; **semi-/self-supervised** — mostly unlabelled data, used heavily in LLMs.)

Analogy: supervised = studying with an answer key; unsupervised = sorting a box of mixed Lego by shape and colour without instructions.

> Install the ML libraries with `pip install numpy pandas scikit-learn matplotlib`. Examples use `random_state=42` so your numbers match the expected output (tiny differences can appear across library versions). Run from inside this day's folder so `../../datasets/` resolves.

## 3. Syntax

```python
# supervised                          # unsupervised
model.fit(X, y)                        model.fit(X)          # no y!
model.predict(X_new)  -> labels        model.predict(X) -> cluster ids / anomaly flags
```

| Part | Meaning |
|---|---|
| `X` | Feature matrix: rows = examples, columns = features. |
| `y` | Labels (only in supervised learning). |
| `KMeans(n_clusters=k)` | Groups data into k clusters. |
| `IsolationForest` | Flags points that are easy to isolate (anomalies) as -1. |

## 4. Example 1 — Basic Example: Same data, two kinds of question

```python
import pandas as pd
from sklearn.linear_model import LinearRegression, LogisticRegression

df = pd.read_csv("../../datasets/server_failures.csv")
X = df[["cpu_usage", "memory_usage", "disk_usage", "error_count"]]

# Supervised - CLASSIFICATION: label is a category (0/1)
classifier = LogisticRegression(max_iter=1000).fit(X, df["failure"])
print("Classification -> failure for a busy server?",
      classifier.predict(pd.DataFrame([[95, 92, 90, 8]], columns=X.columns))[0])

# Supervised - REGRESSION: label is a number
regressor = LinearRegression().fit(X, df["response_time_ms"])
print("Regression -> predicted response time:",
      round(regressor.predict(pd.DataFrame([[95, 92, 90, 8]], columns=X.columns))[0]), "ms")

print("Labels available? classification y:", df["failure"].unique().tolist(),
      "| regression y range:", (int(df["response_time_ms"].min()), int(df["response_time_ms"].max())))
```

## 5. Example 2 — Practical Example: Unsupervised: clustering servers and spotting anomalies

```python
import numpy as np
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler

rng = np.random.default_rng(42)
# Three hidden workload types (we DON'T tell the algorithm): web, database, batch
web = rng.normal([40, 30, 200], [5, 5, 30], size=(30, 3))       # cpu %, memory %, network Mbps
db = rng.normal([55, 85, 60], [5, 4, 15], size=(30, 3))
batch = rng.normal([90, 50, 20], [4, 6, 8], size=(30, 3))
odd = np.array([[5, 98, 900]])                                  # one strange server
X = np.vstack([web, db, batch, odd])

X_scaled = StandardScaler().fit_transform(X)                    # put features on the same scale
kmeans = KMeans(n_clusters=3, n_init=10, random_state=42).fit(X_scaled)
for cluster in range(3):
    members = X[kmeans.labels_ == cluster]
    print(f"cluster {cluster}: {len(members):>2} servers, mean cpu={members[:, 0].mean():5.1f} "
          f"mem={members[:, 1].mean():5.1f} net={members[:, 2].mean():6.1f}")

iso = IsolationForest(contamination=0.01, random_state=42).fit(X_scaled)
flags = iso.predict(X_scaled)                                   # -1 = anomaly
print("anomalies found at rows:", np.where(flags == -1)[0].tolist())
print("row 90 values:", X[90].round(1).tolist())
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Both models are **supervised** — they receive `y`.
- `LogisticRegression` predicts a **category** (failure 0/1) → classification.
- `LinearRegression` predicts a **number** (response time) → regression.
- Model inputs are DataFrames with the same column names used in training.

**Example 2**
- We generate three workload types but **never give labels** to the algorithm.
- `StandardScaler` rescales features so network Mbps (hundreds) doesn't dominate CPU % (tens).
- `KMeans(n_clusters=3)` rediscovers the three groups (web, database, batch) from the numbers alone.
- `IsolationForest` flags the strange server (row 90) as an anomaly (`-1`) — unsupervised anomaly detection, a core AIOps technique.

## 7. Expected Output

**Example 1:**

```text
Classification -> failure for a busy server? 1
Regression -> predicted response time: 303 ms
Labels available? classification y: [0, 1] | regression y range: (30, 714)
```

**Example 2:**

```text
cluster 0: 30 servers, mean cpu= 54.7 mem= 84.3 net=  57.9
cluster 1: 30 servers, mean cpu= 89.7 mem= 50.9 net=  19.2
cluster 2: 31 servers, mean cpu= 39.0 mem= 31.8 net= 225.2
anomalies found at rows: [90]
row 90 values: [5.0, 98.0, 900.0]
```

## 8. Common Mistakes

**1. Forgetting to scale for distance-based algorithms**

K-Means uses distances; features with large ranges dominate. Scale first.

**2. Calling clusters 'labels'**

Cluster ids (0, 1, 2) are arbitrary groupings, not meaningful classes, until a human interprets them.

**3. Choosing regression for categories**

Predicting `failure` with linear regression gives numbers like 0.37. Use a classifier.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Name the problem type:** For each question print supervised-regression, supervised-classification or unsupervised: (1) Will this build fail? (2) How many GB will logs use tomorrow? (3) Which users behave similarly? (4) Which alert severity (1–4)? (5) Which transactions look unusual (no labels)?
- **Task 2 (Medium) — Cluster the server dataset:** Cluster `servers.csv` on cpu/memory/disk usage (scaled) into 3 groups with K-Means and print, per cluster, the number of servers, the average usage values and the most common `status`.
- **Task 3 (Practical Challenge) — Anomaly detector for metrics:** Load `server_metrics.csv`, drop rows with missing values, scale cpu/memory/response_ms and run IsolationForest (contamination 0.05). Print the anomalous rows (timestamp, server, cpu, memory, response_ms).

## 10. DevOps/MLOps Connection

- **DevOps / AIOps:** unsupervised anomaly detection on metrics (no one labels "normal" data), clustering alerts or log lines to reduce noise.
- **Capacity planning:** clustering workloads to choose instance families; regression to forecast growth.
- **MLOps:** you'll operate both kinds — supervised models need labelled data pipelines and accuracy monitoring; unsupervised ones need careful thresholds and human feedback loops.

## 11. Interview Questions

**Q1. What is the difference between supervised and unsupervised learning?**

<details><summary>Show answer</summary>

Supervised learning trains on labelled examples to predict a target; unsupervised learning finds structure (clusters, anomalies) in unlabelled data.

</details>

**Q2. What is the difference between regression and classification?**

<details><summary>Show answer</summary>

Regression predicts continuous numbers; classification predicts discrete categories.

</details>

**Q3. Why scale features before K-Means?**

<details><summary>Show answer</summary>

K-Means relies on Euclidean distance, so features with larger ranges would dominate the clustering.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 92 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 091](../../10-machine-learning/day-091/README.md) | [📚 Phase 10: Machine Learning Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 093 ➡](../../10-machine-learning/day-093/README.md)
