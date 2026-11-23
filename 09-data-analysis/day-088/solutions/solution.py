"""
Day 088 — Reading CSV and Excel Data: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
from pathlib import Path

import pandas as pd

pd.set_option("display.width", 120)

# ===== Task 1 =====
Path("ports.csv").write_text("# generated\nservice;port;protocol\nssh;22;tcp\ndns;53;udp\nhttps;443;tcp\n")
print(pd.read_csv("ports.csv", sep=";", comment="#"))

# ===== Task 2 =====
sales = pd.read_excel("../../datasets/sales.xlsx")
laptops = sales[sales["product"] == "Laptop"]
laptops.to_excel("laptops.xlsx", sheet_name="laptops", index=False)
back = pd.read_excel("laptops.xlsx", sheet_name="laptops")
print("rows:", len(back), "| units:", back["units"].sum())

# ===== Task 3 =====
metrics = pd.read_csv("../../datasets/server_metrics.csv", parse_dates=["timestamp"])
summary = metrics.groupby("server").agg(mean_cpu=("cpu", "mean"), max_response_ms=("response_ms", "max")).round(1).reset_index()
print(summary)
summary.to_csv("metrics_summary.csv", index=False)
summary.to_json("metrics_summary.json", orient="records")
with pd.ExcelWriter("metrics_report.xlsx") as writer:
    metrics.to_excel(writer, sheet_name="raw", index=False)
    summary.to_excel(writer, sheet_name="summary", index=False)
print(list(pd.read_excel("metrics_report.xlsx", sheet_name=None)))
