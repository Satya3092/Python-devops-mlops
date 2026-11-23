"""
train.py - data preparation, training, evaluation and serialization.

Usage:  python train.py [--data data/server_failures.csv] [--out models] [--threshold 0.3]
Produces:
    models/model.joblib     the fitted scikit-learn Pipeline + metadata (one "bundle")
    models/metrics.json     evaluation metrics, used as a CI quality gate
"""
import argparse
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
FEATURES = ["cpu_usage", "memory_usage", "disk_usage", "error_count", "response_time_ms"]
TARGET = "failure"
MODEL_VERSION = "1.0.0"


def load_and_prepare(path):
    """Load the CSV, validate the schema and clean obvious problems."""
    df = pd.read_csv(path)
    missing = [c for c in FEATURES + [TARGET] if c not in df.columns]
    if missing:
        raise ValueError(f"dataset is missing columns: {missing}")
    before = len(df)
    df = df.drop_duplicates().dropna(subset=FEATURES + [TARGET])
    for col in ("cpu_usage", "memory_usage", "disk_usage"):
        df[col] = df[col].clip(0, 100)
    print(f"[data] {path.name}: {before} rows -> {len(df)} after cleaning, failure rate {df[TARGET].mean():.1%}")
    return df


def train(df, threshold):
    X, y = df[FEATURES], df[TARGET]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)
    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", LogisticRegression(max_iter=1000)),
    ])
    pipeline.fit(X_train, y_train)
    proba = pipeline.predict_proba(X_test)[:, 1]
    pred = (proba >= threshold).astype(int)
    metrics = {
        "accuracy": round(accuracy_score(y_test, pred), 4),
        "precision": round(precision_score(y_test, pred), 4),
        "recall": round(recall_score(y_test, pred), 4),
        "f1": round(f1_score(y_test, pred), 4),
        "roc_auc": round(roc_auc_score(y_test, proba), 4),
        "threshold": threshold,
        "train_rows": len(X_train),
        "test_rows": len(X_test),
    }
    print("[eval] " + " ".join(f"{k}={v}" for k, v in metrics.items() if k in ("accuracy", "precision", "recall", "f1", "roc_auc")))
    return pipeline, metrics


def save(pipeline, metrics, data_path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)
    bundle = {
        "model": pipeline,
        "features": FEATURES,
        "threshold": metrics["threshold"],
        "version": MODEL_VERSION,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "data_sha256": hashlib.sha256(data_path.read_bytes()).hexdigest(),
        "sklearn_version": sklearn.__version__,
        "python_version": platform.python_version(),
        "metrics": metrics,
    }
    model_path = out_dir / "model.joblib"
    joblib.dump(bundle, model_path)
    (out_dir / "metrics.json").write_text(json.dumps(metrics, indent=2))
    model_path = model_path.resolve()
    shown = model_path.relative_to(HERE) if model_path.is_relative_to(HERE) else model_path
    print(f"[save] {shown} ({model_path.stat().st_size / 1024:.1f} KB), metrics.json")
    return model_path


def main(argv=None):
    parser = argparse.ArgumentParser(description="Train the server-failure model")
    parser.add_argument("--data", type=Path, default=HERE / "data" / "server_failures.csv")
    parser.add_argument("--out", type=Path, default=HERE / "models")
    parser.add_argument("--threshold", type=float, default=0.3)
    parser.add_argument("--min-recall", type=float, default=0.8, help="quality gate")
    args = parser.parse_args(argv)

    df = load_and_prepare(args.data)
    pipeline, metrics = train(df, args.threshold)
    if metrics["recall"] < args.min_recall:
        print(f"[gate] FAILED: recall {metrics['recall']} < {args.min_recall}; model not saved")
        return 1
    print(f"[gate] passed: recall {metrics['recall']} >= {args.min_recall}")
    save(pipeline, metrics, args.data, args.out)
    return 0


if __name__ == "__main__":
    sys.exit(main())
