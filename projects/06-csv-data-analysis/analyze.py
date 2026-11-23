"""
Project 6 - CSV Data Analysis with NumPy and pandas.

Usage: python analyze.py [--data-dir ../../datasets] [--out-dir output]
"""
import argparse
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent


def load(data_dir):
    sales = pd.read_csv(data_dir / "sales.csv", parse_dates=["date"])
    metrics = pd.read_csv(data_dir / "server_metrics.csv", parse_dates=["timestamp"])
    print(f"[load] sales: {len(sales)} rows | metrics: {len(metrics)} rows")
    return sales, metrics


def clean_metrics(raw):
    df = raw.copy()
    duplicates = int(df.duplicated().sum())
    df = df.drop_duplicates()
    fixed = int((df["server"] != df["server"].str.strip().str.lower()).sum())
    df["server"] = df["server"].str.strip().str.lower()
    missing = int(df[["cpu", "memory", "response_ms"]].isna().sum().sum())
    df = df.sort_values(["server", "timestamp"])
    for col in ["cpu", "memory", "response_ms"]:
        df[col] = df.groupby("server")[col].transform(lambda s: s.interpolate().bfill().ffill())
    df[["cpu", "memory", "disk"]] = df[["cpu", "memory", "disk"]].clip(0, 100)
    print(f"[clean] metrics: removed {duplicates} duplicate, fixed {fixed} label, filled {missing} missing values")
    return df.reset_index(drop=True)


def analyse_sales(sales):
    sales = sales.assign(revenue=sales["units"] * sales["unit_price"], month=sales["date"].dt.to_period("M"))
    by_region = sales.groupby("region")["revenue"].sum().sort_values(ascending=False)
    by_product = sales.groupby("product").agg(units=("units", "sum"), revenue=("revenue", "sum")) \
                      .sort_values("revenue", ascending=False)
    monthly = sales.groupby("month")["revenue"].sum()
    growth = (monthly.pct_change() * 100).round(1)
    pivot = sales.pivot_table(index="region", columns="product", values="revenue", aggfunc="sum", fill_value=0)
    print(f"[sales] total revenue {sales['revenue'].sum():,} | best region {by_region.index[0]} "
          f"| best product {by_product.index[0]}")
    return {"by_region": by_region, "by_product": by_product, "monthly": monthly, "growth": growth, "pivot": pivot}


def analyse_servers(metrics):
    summary = metrics.groupby("server").agg(
        avg_cpu=("cpu", "mean"), max_cpu=("cpu", "max"), avg_memory=("memory", "mean"),
        p95_response_ms=("response_ms", lambda s: np.percentile(s, 95)),
    ).round(1)
    hourly = metrics.set_index("timestamp").groupby("server")["cpu"].resample("1h").mean().unstack(0).round(1)
    z = (metrics["response_ms"] - metrics["response_ms"].mean()) / metrics["response_ms"].std()
    anomalies = metrics.loc[z.abs() > 2, ["timestamp", "server", "response_ms"]]
    worst = summary["p95_response_ms"].idxmax()
    print(f"[servers] highest p95 latency: {worst} {summary.loc[worst, 'p95_response_ms']} ms "
          f"| anomalies: {len(anomalies)}")
    return {"summary": summary, "hourly": hourly, "anomalies": anomalies}


def make_charts(sales_result, server_result, out_dir):
    charts = []
    ax = sales_result["by_region"].plot(kind="bar", title="Revenue by region", figsize=(6, 4), color="#4C72B0")
    ax.set_ylabel("revenue")
    plt.tight_layout(); plt.savefig(out_dir / "revenue_by_region.png", dpi=100); plt.close()
    charts.append("revenue_by_region.png")

    ax = sales_result["monthly"].plot(marker="o", title="Monthly revenue", figsize=(7, 4))
    ax.set_ylabel("revenue")
    plt.tight_layout(); plt.savefig(out_dir / "monthly_revenue.png", dpi=100); plt.close()
    charts.append("monthly_revenue.png")

    ax = server_result["hourly"].plot(marker="o", title="Hourly average CPU per server", figsize=(7, 4))
    ax.axhline(75, linestyle="--", color="gray")
    ax.set_ylabel("CPU %")
    plt.tight_layout(); plt.savefig(out_dir / "hourly_cpu.png", dpi=100); plt.close()
    charts.append("hourly_cpu.png")
    return charts


def write_report(sales_result, server_result, charts, out_dir):
    def table(frame):
        try:
            return frame.to_markdown()
        except ImportError:                     # 'tabulate' not installed
            return "```\n" + frame.to_string() + "\n```"

    lines = [
        "# Weekly Data Report", "",
        "## Sales", "", "### Revenue by region", table(sales_result["by_region"].to_frame("revenue")), "",
        "### Products", table(sales_result["by_product"]), "",
        "### Month-over-month growth (%)", table(sales_result["growth"].to_frame("growth_%")), "",
        "### Region x product revenue", table(sales_result["pivot"]), "",
        "## Servers", "", table(server_result["summary"]), "",
        f"### Response-time anomalies (|z| > 2): {len(server_result['anomalies'])}",
        table(server_result["anomalies"].set_index("timestamp")), "",
        "## Charts", "", *[f"![{c}]({c})" for c in charts],
    ]
    (out_dir / "report.md").write_text("\n".join(lines) + "\n")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Analyse sales and server-metric CSV exports")
    parser.add_argument("--data-dir", type=Path, default=HERE.parent.parent / "datasets")
    parser.add_argument("--out-dir", type=Path, default=HERE / "output")
    args = parser.parse_args(argv)
    args.out_dir.mkdir(parents=True, exist_ok=True)

    sales, raw_metrics = load(args.data_dir)
    metrics = clean_metrics(raw_metrics)
    sales_result = analyse_sales(sales)
    server_result = analyse_servers(metrics)
    charts = make_charts(sales_result, server_result, args.out_dir)
    write_report(sales_result, server_result, charts, args.out_dir)
    metrics.to_csv(args.out_dir / "server_metrics_clean.csv", index=False)
    sales_result["by_product"].to_csv(args.out_dir / "product_summary.csv")
    print(f"[report] {(args.out_dir / 'report.md').relative_to(args.out_dir.parent)}, "
          f"{len(charts)} charts, 2 CSV files")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
