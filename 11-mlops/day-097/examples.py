"""
Day 097 — Saving and Loading ML Models using Pickle/Joblib
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Train once, save, load and predict
# ======================================================================
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

# ======================================================================
# Example 2 — A versioned model bundle with metadata and checksum
# ======================================================================
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
