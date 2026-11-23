# Day 097 — Saving and Loading ML Models using Pickle/Joblib

[⬅ Day 096](../../10-machine-learning/day-096/README.md) | [📚 Phase 11: MLOps Foundation](../README.md) | [🏠 Home](../../README.md) | [Day 098 ➡](../../11-mlops/day-098/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 11 — MLOps Foundation | 🔴 Advanced beginner (MLOps) | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Serialize trained models with `pickle` and `joblib` and load them back
- Save a model *bundle* with metadata (version, features, metrics, library versions, data hash)
- Understand security and compatibility risks of pickled models

## 2. Topic Explanation

Training can take minutes or days. Once a model is trained you **save** it to a file (**serialization**) so other programs — an API, a batch job, a container — can **load** it and make predictions without retraining. In MLOps the saved model is a **build artefact**, just like a Docker image or a JAR.

| Tool | Use |
|---|---|
| `pickle` (standard library) | serialise any Python object |
| `joblib` | like pickle but efficient for large NumPy arrays; the scikit-learn recommendation; supports compression |
| ONNX / skops / framework formats | portable or safer formats for advanced use |

```python
import joblib
joblib.dump(model, "model.joblib")
model = joblib.load("model.joblib")
```

**Save more than the model — save a bundle:**
- the fitted **Pipeline** (preprocessing + model, Day 94)
- **feature names and order** the model expects
- **model version**, training date, decision threshold
- **evaluation metrics**
- **library versions** (`sklearn.__version__`, Python) — loading a model with a different scikit-learn version can fail or behave differently
- **data fingerprint** (SHA-256 of the training data) for reproducibility/lineage

⚠️ **Security:** loading a pickle/joblib file can execute arbitrary code. **Only load model files you trust** (from your own pipeline/registry), verify checksums, never load models from random downloads or user uploads.

> Install: `pip install scikit-learn pandas joblib`. Run from inside this day's folder.

## 3. Syntax

```python
import pickle, joblib
with open("model.pkl", "wb") as f: pickle.dump(model, f)       # pickle
with open("model.pkl", "rb") as f: model = pickle.load(f)
joblib.dump(bundle, "model.joblib", compress=3)                 # joblib
bundle = joblib.load("model.joblib")
```

| Part | Meaning |
|---|---|
| `"wb" / "rb"` | Pickle files are binary: write/read bytes. |
| `joblib.dump(obj, path)` | Serialise to disk (optionally compressed). |
| `joblib.load(path)` | Deserialise — only from trusted sources! |
| `bundle` | A dict holding the model plus metadata. |

## 4. Example 1 — Basic Example: Train once, save, load and predict

```python
import pickle
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

df = pd.read_csv("../../datasets/server_failures.csv")
X, y = df.drop(columns=["failure"]), df["failure"]
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X, y)

with open("model.pkl", "wb") as f:                 # pickle (standard library)
    pickle.dump(model, f)
joblib.dump(model, "model.joblib")                 # joblib (recommended for sklearn)
joblib.dump(model, "model_compressed.joblib", compress=3)
for name in ("model.pkl", "model.joblib", "model_compressed.joblib"):
    print(f"{name:<24} {Path(name).stat().st_size / 1024:6.1f} KB")

loaded = joblib.load("model.joblib")               # e.g. inside an API, hours later
sample = X.iloc[[0, 3]]
print("original predictions:", model.predict(sample).tolist())
print("loaded predictions  :", loaded.predict(sample).tolist())
print("identical probabilities:", (model.predict_proba(X) == loaded.predict_proba(X)).all())
```

## 5. Example 2 — Practical Example: A versioned model bundle with metadata and checksum

```python
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

DATA = Path("../../datasets/server_failures.csv")
FEATURES = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
VERSION = "1.2.0"

df = pd.read_csv(DATA)
X_train, X_test, y_train, y_test = train_test_split(df[FEATURES], df["failure"], test_size=0.25,
                                                    random_state=42, stratify=df["failure"])
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]

bundle = {
    "model": model,
    "version": VERSION,
    "features": FEATURES,
    "threshold": 0.3,
    "metrics": {"roc_auc": round(roc_auc_score(y_test, proba), 4),
                "recall@0.3": round(recall_score(y_test, proba >= 0.3), 4)},
    "trained_at": datetime(2026, 11, 20, tzinfo=timezone.utc).isoformat(),   # real code: datetime.now(timezone.utc)
    "sklearn_version": sklearn.__version__,
    "python_version": platform.python_version(),
    "data_sha256": hashlib.sha256(DATA.read_bytes()).hexdigest()[:16],
}
models_dir = Path("models")
models_dir.mkdir(exist_ok=True)
path = models_dir / f"failure-model-v{VERSION}.joblib"
joblib.dump(bundle, path)
checksum = hashlib.sha256(path.read_bytes()).hexdigest()
(models_dir / f"failure-model-v{VERSION}.json").write_text(json.dumps(
    {k: v for k, v in bundle.items() if k != "model"} | {"file_sha256": checksum}, indent=2))
print("Saved", path.name, "and its metadata JSON")


def load_model(path, expected_sha256):
    """Verify integrity before unpickling (never load untrusted files!)."""
    actual = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    if actual != expected_sha256:
        raise ValueError("checksum mismatch - refusing to load model")
    loaded = joblib.load(path)
    if loaded["sklearn_version"] != sklearn.__version__:
        print("WARNING: model trained with a different scikit-learn version")
    return loaded


loaded = load_model(path, checksum)
print("version:", loaded["version"], "| features:", len(loaded["features"]), "| metrics:", loaded["metrics"])
new = pd.DataFrame([{"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7, "response_time_ms": 650}])
p = loaded["model"].predict_proba(new[loaded["features"]])[0, 1]
print(f"failure probability {p:.3f} -> failure={p >= loaded['threshold']}")
try:
    load_model(path, "0" * 64)
except ValueError as error:
    print("Tampered/unknown file:", error)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The **whole pipeline** (scaler + model) is saved — loading it later gives the exact same predictions.
- `pickle` needs binary file handles (`"wb"`, `"rb"`); `joblib.dump/load` takes paths and can compress.
- The comparison proves the loaded model is identical.

**Example 2**
- The bundle stores the model plus everything needed to **use and audit** it: feature order, threshold, metrics, versions, data fingerprint.
- The file name contains the version (`failure-model-v1.2.0.joblib`) — never overwrite "model.pkl" blindly.
- A JSON sidecar with metadata (without the binary model) is human-readable and easy to diff in Git or show in a model registry.
- `load_model` verifies a SHA-256 checksum before unpickling and warns on library-version mismatch.

## 7. Expected Output

**Example 1:**

```text
model.pkl                   1.4 KB
model.joblib                1.8 KB
model_compressed.joblib     1.1 KB
original predictions: [0, 0]
loaded predictions  : [0, 0]
identical probabilities: True
```

**Example 2:**

```text
Saved failure-model-v1.2.0.joblib and its metadata JSON
version: 1.2.0 | features: 5 | metrics: {'roc_auc': 0.981, 'recall@0.3': 0.8889}
failure probability 0.998 -> failure=True
Tampered/unknown file: checksum mismatch - refusing to load model
```

## 8. Common Mistakes

**1. Saving only the estimator**

If you save the model without the scaler/encoder, predictions in production will be wrong. Save the full Pipeline.

**2. Loading untrusted pickles**

Unpickling can run arbitrary code. Load only artefacts from your own pipeline/registry and verify checksums.

**3. Mismatched library versions**

A model saved with scikit-learn X may not load in Y. Pin versions and record them in metadata (or train inside the serving image, Day 99).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Save and reload:** Train a `DecisionTreeClassifier(max_depth=3)` on Iris, save it with joblib to `iris_tree.joblib`, reload it, and print predictions for the first 3 rows from both models.
- **Task 2 (Medium) — Model registry folder:** Train two versions of a regression model on `house_prices.csv` (v1 with `size_sqft` only, v2 with all features). Save each as `registry/house-v<N>.joblib` with metrics (R² on a test split). Write `latest_best(registry)` that loads every bundle and returns the version with the best R².
- **Task 3 (Practical Challenge) — Prediction CLI:** Write a function `predict_from_file(model_path, csv_path)` that loads a saved failure-model bundle (create it in the solution), reads a CSV of new servers, validates that all required feature columns exist (raise `ValueError` otherwise), and writes `predictions.csv` with probability and failure columns. Print the result.

## 10. DevOps/MLOps Connection

- **DevOps parallel:** a serialized model is a build artefact — version it, checksum it, store it in an artefact repository (S3, a model registry like MLflow, or an OCI registry), and promote it through environments.
- **Cloud:** upload `model.joblib` to S3 (boto3, Day 82); serving containers download it at start-up.
- **MLOps:** model registries add stages (Staging/Production), lineage (data hash, code commit) and approval workflows on top of exactly this bundle idea.

## 11. Interview Questions

**Q1. What is the difference between pickle and joblib?**

<details><summary>Show answer</summary>

Both serialise Python objects; joblib is optimised for objects containing large NumPy arrays and supports compression, and is recommended by scikit-learn.

</details>

**Q2. Why is loading a pickle file a security risk?**

<details><summary>Show answer</summary>

Unpickling can execute arbitrary code embedded in the file, so untrusted files can compromise the system.

</details>

**Q3. What metadata should you save with a model?**

<details><summary>Show answer</summary>

Version, feature names/order, preprocessing, thresholds, metrics, training date, library/Python versions, data fingerprint and code commit.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 97 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 096](../../10-machine-learning/day-096/README.md) | [📚 Phase 11: MLOps Foundation](../README.md) | [🏠 Home](../../README.md) | [Day 098 ➡](../../11-mlops/day-098/README.md)
