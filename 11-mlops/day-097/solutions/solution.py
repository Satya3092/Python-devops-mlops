"""
Day 097 — Saving and Loading ML Models using Pickle/Joblib: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

# ===== Task 1 =====
iris = load_iris()
tree = DecisionTreeClassifier(max_depth=3, random_state=42).fit(iris.data, iris.target)
joblib.dump(tree, "iris_tree.joblib")
reloaded = joblib.load("iris_tree.joblib")
print(tree.predict(iris.data[:3]).tolist(), reloaded.predict(iris.data[:3]).tolist())

# ===== Task 2 =====
houses = pd.read_csv("../../datasets/house_prices.csv")
X_train, X_test, y_train, y_test = train_test_split(houses.drop(columns="price"), houses["price"],
                                                    test_size=0.2, random_state=42)
registry = Path("registry")
registry.mkdir(exist_ok=True)
for version, features in [(1, ["size_sqft"]), (2, list(X_train.columns))]:
    model = LinearRegression().fit(X_train[features], y_train)
    r2 = model.score(X_test[features], y_test)
    joblib.dump({"model": model, "version": version, "features": features, "r2": round(r2, 4)},
                registry / f"house-v{version}.joblib")
    print(f"saved v{version} r2={r2:.3f}")


def latest_best(folder):
    bundles = [joblib.load(p) for p in sorted(Path(folder).glob("house-v*.joblib"))]
    return max(bundles, key=lambda b: b["r2"])


best = latest_best(registry)
print("best version:", best["version"], "r2:", best["r2"])

# ===== Task 3 =====
df = pd.read_csv("../../datasets/server_failures.csv")
FEATURES = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
pipe = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000)).fit(df[FEATURES], df["failure"])
joblib.dump({"model": pipe, "features": FEATURES, "threshold": 0.3}, "failure_bundle.joblib")
pd.DataFrame([
    {"host": "web-01", "cpu_usage": 35, "memory_usage": 40, "disk_usage": 50, "error_count": 0, "response_time_ms": 150},
    {"host": "db-01", "cpu_usage": 92, "memory_usage": 95, "disk_usage": 91, "error_count": 9, "response_time_ms": 700},
    {"host": "cache-01", "cpu_usage": 70, "memory_usage": 85, "disk_usage": 60, "error_count": 4, "response_time_ms": 300},
]).to_csv("new_servers.csv", index=False)


def predict_from_file(model_path, csv_path):
    bundle = joblib.load(model_path)
    data = pd.read_csv(csv_path)
    missing = [c for c in bundle["features"] if c not in data.columns]
    if missing:
        raise ValueError(f"missing feature columns: {missing}")
    data["probability"] = bundle["model"].predict_proba(data[bundle["features"]])[:, 1].round(3)
    data["failure"] = data["probability"] >= bundle["threshold"]
    data.to_csv("predictions.csv", index=False)
    return data


print(predict_from_file("failure_bundle.joblib", "new_servers.csv")[["host", "probability", "failure"]])
