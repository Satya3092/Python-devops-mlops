"""
Project 7 - prediction CLI.

Single:  python predict.py --size 1800 --bedrooms 3 --age 5 --distance 8
Batch:   python predict.py --csv new_houses.csv [--out predictions.csv]
"""
import argparse
import sys
from pathlib import Path

import joblib
import pandas as pd

HERE = Path(__file__).resolve().parent


def load_bundle(path):
    if not path.exists():
        sys.exit(f"Model not found at {path}. Run 'python train_model.py' first.")
    return joblib.load(path)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Predict house prices")
    parser.add_argument("--model", type=Path, default=HERE / "models" / "house_model.joblib")
    parser.add_argument("--csv", type=Path, help="CSV with size_sqft,bedrooms,age_years,distance_km")
    parser.add_argument("--out", type=Path, default=Path("predictions.csv"))
    parser.add_argument("--size", type=float)
    parser.add_argument("--bedrooms", type=int)
    parser.add_argument("--age", type=float)
    parser.add_argument("--distance", type=float)
    args = parser.parse_args(argv)

    bundle = load_bundle(args.model)
    if args.csv:
        data = pd.read_csv(args.csv)
        missing = set(bundle["features"]) - set(data.columns)
        if missing:
            sys.exit(f"CSV is missing columns: {sorted(missing)}")
        data["predicted_price"] = bundle["model"].predict(data[bundle["features"]]).round(-2)
        data.to_csv(args.out, index=False)
        print(data.to_string(index=False))
        print(f"Saved {args.out}")
        return 0
    values = [args.size, args.bedrooms, args.age, args.distance]
    if any(v is None for v in values):
        parser.error("give --size, --bedrooms, --age and --distance, or --csv")
    row = pd.DataFrame([values], columns=bundle["features"])
    price = bundle["model"].predict(row)[0]
    print(f"Predicted price: {price:,.0f}  (model: {bundle['model_name']}, test MAE ±{bundle['metrics']['mae']:,.0f})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
