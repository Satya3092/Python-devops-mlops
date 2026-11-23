"""
Project 8 - config-driven training with quality gates and champion/challenger promotion.

Usage: python train.py [--config config.yaml]
Exit codes: 0 promoted, 0 (kept champion), 1 quality gate failed, 2 bad config/data.
"""
import argparse
import hashlib
import json
import logging
import platform
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import joblib
import pandas as pd
import sklearn
import yaml
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

HERE = Path(__file__).resolve().parent
LOG = logging.getLogger("train")
MODELS = {"logistic_regression": LogisticRegression, "random_forest": RandomForestClassifier}


class DataValidationError(ValueError):
    """The dataset does not match the expected schema."""


def load_config(path):
    config = yaml.safe_load(Path(path).read_text())
    if config["model"]["type"] not in MODELS:
        raise ValueError(f"unknown model type {config['model']['type']!r}")
    return config


def load_data(config):
    path = HERE / config["data"]["path"]
    df = pd.read_csv(path)
    columns = config["data"]["features"] + [config["data"]["target"]]
    missing = [c for c in columns if c not in df.columns]
    if missing:
        raise DataValidationError(f"missing columns: {missing}")
    df = df[columns].drop_duplicates().dropna()
    if not df[config["data"]["target"]].isin([0, 1]).all():
        raise DataValidationError("target must be 0/1")
    for col in ("cpu_usage", "memory_usage", "disk_usage"):
        if col in df and not df[col].between(0, 100).all():
            raise DataValidationError(f"{col} outside 0-100")
    LOG.info("data %s: %d rows, failure rate %.1f%%", path.name, len(df), df[config["data"]["target"]].mean() * 100)
    return df, hashlib.sha256(path.read_bytes()).hexdigest()


def build_pipeline(config):
    kind = config["model"]["type"]
    model = MODELS[kind](**config["model"]["params"][kind])
    steps = [("scaler", StandardScaler())] if kind == "logistic_regression" else []
    return Pipeline(steps + [("model", model)])


def evaluate(pipeline, X_test, y_test, threshold):
    proba = pipeline.predict_proba(X_test)[:, 1]
    pred = (proba >= threshold).astype(int)
    return {
        "precision": round(float(precision_score(y_test, pred)), 4),
        "recall": round(float(recall_score(y_test, pred)), 4),
        "f1": round(float(f1_score(y_test, pred)), 4),
        "roc_auc": round(float(roc_auc_score(y_test, proba)), 4),
        "threshold": threshold,
    }


def passes_gate(metrics, gate):
    failures = []
    if metrics["recall"] < gate["min_recall"]:
        failures.append(f"recall {metrics['recall']} < {gate['min_recall']}")
    if metrics["roc_auc"] < gate["min_roc_auc"]:
        failures.append(f"roc_auc {metrics['roc_auc']} < {gate['min_roc_auc']}")
    return failures


def train(config):
    df, data_hash = load_data(config)
    features, target = config["data"]["features"], config["data"]["target"]
    X_train, X_test, y_train, y_test = train_test_split(
        df[features], df[target], test_size=config["data"]["test_size"],
        random_state=config["data"]["random_state"], stratify=df[target])
    pipeline = build_pipeline(config).fit(X_train, y_train)
    metrics = evaluate(pipeline, X_test, y_test, config["decision"]["threshold"])
    LOG.info("metrics %s", metrics)
    bundle = {
        "model": pipeline,
        "version": config["model"]["version"],
        "model_type": config["model"]["type"],
        "features": features,
        "threshold": config["decision"]["threshold"],
        "metrics": metrics,
        "data_sha256": data_hash,
        "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "sklearn_version": sklearn.__version__,
        "python_version": platform.python_version(),
    }
    return bundle


def promote(bundle, out_dir):
    """Save the challenger; make it champion only if it is at least as good."""
    out_dir.mkdir(parents=True, exist_ok=True)
    challenger = out_dir / f"model-v{bundle['version']}.joblib"
    joblib.dump(bundle, challenger)
    champion_path = out_dir / "champion.joblib"
    if champion_path.exists():
        champion = joblib.load(champion_path)
        if champion["metrics"]["roc_auc"] > bundle["metrics"]["roc_auc"]:
            print(f"[promote] kept champion v{champion['version']} "
                  f"(auc {champion['metrics']['roc_auc']} > {bundle['metrics']['roc_auc']})")
            return False
    shutil.copyfile(challenger, champion_path)
    (out_dir / "metrics.json").write_text(json.dumps(bundle["metrics"] | {"version": bundle["version"]}, indent=2))
    print(f"[promote] v{bundle['version']} is now champion -> {champion_path.relative_to(HERE)}")
    return True


def main(argv=None):
    parser = argparse.ArgumentParser(description="Train the server-failure model")
    parser.add_argument("--config", default=HERE / "config.yaml")
    args = parser.parse_args(argv)
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    try:
        config = load_config(args.config)
        bundle = train(config)
    except (DataValidationError, ValueError, KeyError, FileNotFoundError) as error:
        print(f"[error] {error}")
        return 2
    m = bundle["metrics"]
    print(f"[eval] {bundle['model_type']} v{bundle['version']}: precision={m['precision']} "
          f"recall={m['recall']} f1={m['f1']} roc_auc={m['roc_auc']}")
    failures = passes_gate(m, config["quality_gate"])
    if failures:
        print("[gate] FAILED: " + "; ".join(failures))
        return 1
    print("[gate] passed")
    promote(bundle, HERE / config["output"]["dir"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
