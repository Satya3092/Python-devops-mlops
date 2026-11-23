"""
Day 088 — Reading CSV and Excel Data
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — read_csv options on a messy export
# ======================================================================
from pathlib import Path

import pandas as pd

pd.set_option("display.width", 120)

messy = """# exported from CMDB on 2026-11-20
asset_id;hostname;owner;purchase_date;cost_usd;status
00123;web-01;team-web;2024-03-15;1200;active
00124;web-02;team-web;2024-03-15;N/A;active
00987;db-01;-;2023-11-02;5400;active
01001;old-ftp;team-legacy;2019-07-30;800;retired
"""
Path("cmdb_export.csv").write_text(messy)

df = pd.read_csv(
    "cmdb_export.csv",
    sep=";",
    skiprows=1,                       # skip the comment line
    dtype={"asset_id": "string"},     # keep leading zeros
    parse_dates=["purchase_date"],
    na_values=["N/A", "-"],
)
print(df)
print(df.dtypes)
print("Missing values per column:", df.isna().sum().to_dict())
print("Age in years:", ((pd.Timestamp("2026-11-20") - df["purchase_date"]).dt.days / 365).round(1).tolist())

subset = pd.read_csv("../../datasets/servers.csv", usecols=["hostname", "cpu_usage"], nrows=3)
print(subset)

# ======================================================================
# Example 2 — Excel in, multi-sheet Excel/CSV/JSON out, chunked processing
# ======================================================================
import json

import pandas as pd

pd.set_option("display.width", 120)

sales = pd.read_excel("../../datasets/sales.xlsx", sheet_name="sales")
print("Excel rows:", len(sales), "| columns:", list(sales.columns))
sales["revenue"] = sales["units"] * sales["unit_price"]

by_region = sales.groupby("region", as_index=False)["revenue"].sum()     # Day 89 explains groupby
by_product = sales.groupby("product", as_index=False)["revenue"].sum()

with pd.ExcelWriter("sales_report.xlsx") as writer:
    sales.to_excel(writer, sheet_name="raw", index=False)
    by_region.to_excel(writer, sheet_name="by_region", index=False)
    by_product.to_excel(writer, sheet_name="by_product", index=False)

sheets = pd.read_excel("sales_report.xlsx", sheet_name=None)       # dict of all sheets
print("Workbook sheets:", {name: frame.shape for name, frame in sheets.items()})

by_region.to_csv("by_region.csv", index=False)
by_region.to_json("by_region.json", orient="records")
print("CSV :", open("by_region.csv").read().strip().splitlines()[:2])
print("JSON:", json.load(open("by_region.json"))[:2])

# Processing a 'big' file in chunks keeps memory low
total_units = 0
for chunk in pd.read_csv("../../datasets/sales.csv", chunksize=10):
    total_units += chunk["units"].sum()
print("Units counted chunk by chunk:", total_units, "| check:", pd.read_csv("../../datasets/sales.csv")["units"].sum())
