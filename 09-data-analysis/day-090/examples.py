"""
Day 090 — Data Cleaning and Handling Missing Values
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Finding the dirt
# ======================================================================
import pandas as pd

pd.set_option("display.width", 120)
df = pd.read_csv("../../datasets/server_metrics.csv")

print("shape:", df.shape)
print("missing per column:", df.isna().sum().to_dict())
print("duplicate rows:", df.duplicated().sum())
print("server labels:", df["server"].value_counts().to_dict())
print()
print("Rows with any missing value:")
print(df[df.isna().any(axis=1)])
print()
print(df.describe().round(1))

# ======================================================================
# Example 2 — A reusable cleaning pipeline with validation
# ======================================================================
import pandas as pd

pd.set_option("display.width", 120)


def clean_metrics(raw):
    """Return (clean DataFrame, list of log messages). Never modifies the input."""
    df = raw.copy()
    log = []

    before = len(df)
    df = df.drop_duplicates()
    log.append(f"dropped {before - len(df)} duplicate row(s)")

    fixed = (df["server"] != df["server"].str.strip().str.lower()).sum()
    df["server"] = df["server"].str.strip().str.lower()
    log.append(f"normalised {fixed} server label(s)")

    df["timestamp"] = pd.to_datetime(df["timestamp"])
    df = df.sort_values(["server", "timestamp"])

    for col in ["cpu", "memory"]:
        missing = df[col].isna().sum()
        df[col] = df.groupby("server")[col].transform(lambda s: s.interpolate().bfill().ffill())
        log.append(f"interpolated {missing} missing {col} value(s) per server")

    missing = df["response_ms"].isna().sum()
    df["response_ms"] = df["response_ms"].fillna(df["response_ms"].median())
    log.append(f"filled {missing} missing response_ms with the median")

    df[["cpu", "memory", "disk"]] = df[["cpu", "memory", "disk"]].clip(0, 100)
    df["response_ms"] = df["response_ms"].astype(int)
    return df.reset_index(drop=True), log


def validate(df):
    assert df.isna().sum().sum() == 0, "still missing values"
    assert not df.duplicated().any(), "duplicates remain"
    assert set(df["server"]) == {"web-01", "web-02", "db-01"}, "unexpected server names"
    assert df[["cpu", "memory", "disk"]].le(100).all().all(), "percentages above 100"
    return True


raw = pd.read_csv("../../datasets/server_metrics.csv")
clean, steps = clean_metrics(raw)
for step in steps:
    print("-", step)
print("validation passed:", validate(clean))
print("shape before/after:", raw.shape, clean.shape)
print(clean.groupby("server")[["cpu", "memory", "response_ms"]].mean().round(1))
clean.to_csv("server_metrics_clean.csv", index=False)
print("saved server_metrics_clean.csv")
