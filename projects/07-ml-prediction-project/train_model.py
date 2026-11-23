"""
Project 7 - House price prediction: compare models, evaluate, save.

Usage: python train_model.py [--data ../../datasets/house_prices.csv]
"""
import argparse
import json
from datetime import datetime, timezone
from pathlib import Path

import joblib
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn
from sklearn.dummy import DummyRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import KFold, cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeRegressor

HERE = Path(__file__).resolve().parent
FEATURES = ["size_sqft", "bedrooms", "age_years", "distance_km"]
TARGET = "price"

CANDIDATES = {
    "baseline_mean": DummyRegressor(strategy="mean"),
    "linear_regression": make_pipeline(StandardScaler(), LinearRegression()),
    "ridge": make_pipeline(StandardScaler(), Ridge(alpha=1.0)),
    "decision_tree": DecisionTreeRegressor(max_depth=5, random_state=42),
    "random_forest": RandomForestRegressor(n_estimators=200, max_depth=8, random_state=42),
}


def load(path):
    df = pd.read_csv(path)
    missing = set(FEATURES + [TARGET]) - set(df.columns)
    if missing:
        raise ValueError(f"missing columns: {missing}")
    df = df.dropna(subset=[TARGET]).drop_duplicates()
    print(f"Dataset: {len(df)} rows, {len(FEATURES)} features, "
          f"price range {df[TARGET].min():,} - {df[TARGET].max():,}")
    return df


def compare(X_train, y_train):
    cv = KFold(n_splits=5, shuffle=True, random_state=42)
    print("Cross-validation (5-fold MAE on training data, lower is better):")
    scores = {}
    for name, model in CANDIDATES.items():
        mae = -cross_val_score(model, X_train, y_train, cv=cv, scoring="neg_mean_absolute_error").mean()
        scores[name] = mae
        print(f"  {name:<20} {mae:>10,.0f}")
    best = min(scores, key=scores.get)
    print(f"Best model: {best}")
    return best, scores


def evaluate(model, X_test, y_test, out_dir):
    pred = model.predict(X_test)
    metrics = {
        "mae": round(float(mean_absolute_error(y_test, pred)), 1),
        "rmse": round(float(mean_squared_error(y_test, pred) ** 0.5), 1),
        "r2": round(float(r2_score(y_test, pred)), 4),
    }
    print(f"Test set -> MAE {metrics['mae']:,.0f} | RMSE {metrics['rmse']:,.0f} | R² {metrics['r2']}")
    errors = X_test.assign(actual=y_test, predicted=pred.round(-2), abs_error=np.abs(y_test - pred).round(-2))
    by_bedrooms = errors.groupby("bedrooms")["abs_error"].mean().round(0)
    print("Mean absolute error by bedrooms:", by_bedrooms.to_dict())
    print("Largest errors:")
    print(errors.nlargest(3, "abs_error")[FEATURES + ["actual", "predicted"]].to_string(index=False))

    plt.figure(figsize=(5, 5))
    plt.scatter(y_test, pred, alpha=0.7)
    lims = [min(y_test.min(), pred.min()), max(y_test.max(), pred.max())]
    plt.plot(lims, lims, "r--")
    plt.xlabel("actual"); plt.ylabel("predicted"); plt.title("House price predictions")
    plt.tight_layout(); plt.savefig(out_dir / "actual_vs_predicted.png", dpi=100); plt.close()
    return metrics


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=HERE.parent.parent / "datasets" / "house_prices.csv")
    parser.add_argument("--out", type=Path, default=HERE / "models")
    args = parser.parse_args(argv)
    args.out.mkdir(parents=True, exist_ok=True)

    df = load(args.data)
    X_train, X_test, y_train, y_test = train_test_split(df[FEATURES], df[TARGET], test_size=0.2, random_state=42)
    best_name, cv_scores = compare(X_train, y_train)
    model = CANDIDATES[best_name].fit(X_train, y_train)
    metrics = evaluate(model, X_test, y_test, args.out)

    bundle = {"model": model, "model_name": best_name, "features": FEATURES, "metrics": metrics,
              "cv_mae": {k: round(v, 1) for k, v in cv_scores.items()},
              "sklearn_version": sklearn.__version__,
              "trained_at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    joblib.dump(bundle, args.out / "house_model.joblib")
    (args.out / "metrics.json").write_text(json.dumps({"model": best_name, **metrics}, indent=2))
    print(f"Saved {(args.out / 'house_model.joblib').relative_to(HERE)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
