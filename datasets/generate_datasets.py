"""Re-create every sample dataset used in the course.

The CSV/XLSX/LOG files are already committed, so you do NOT need to run this.
It exists so the data is reproducible (a good MLOps habit!).

Run:  python generate_datasets.py      (needs numpy, pandas, openpyxl)
"""
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
rng = np.random.default_rng(42)


def servers():
    rows = []
    envs = ["prod", "staging", "dev"]
    regions = ["us-east-1", "us-west-2", "ap-south-1", "eu-west-1"]
    for i in range(1, 21):
        env = envs[i % 3]
        cpu = int(rng.integers(5, 98))
        mem = int(rng.integers(20, 95))
        disk = int(rng.integers(15, 97))
        status = "critical" if max(cpu, mem, disk) >= 90 else "warning" if max(cpu, mem, disk) >= 75 else "healthy"
        rows.append({
            "hostname": f"{env}-web-{i:02d}", "environment": env, "region": regions[i % 4],
            "cpu_cores": int(rng.choice([2, 4, 8, 16])), "memory_gb": int(rng.choice([4, 8, 16, 32])),
            "cpu_usage": cpu, "memory_usage": mem, "disk_usage": disk, "status": status,
        })
    pd.DataFrame(rows).to_csv(HERE / "servers.csv", index=False)


def app_log():
    levels = ["INFO"] * 6 + ["WARNING"] * 3 + ["ERROR"] * 2
    msgs = {
        "INFO": ["User login successful user={u}", "GET /api/orders 200 {ms}ms", "Health check passed",
                 "Deployment v1.{v} started", "Cache refreshed in {ms}ms"],
        "WARNING": ["High memory usage {p}%", "Slow response GET /api/products {ms}ms", "Disk usage at {p}%"],
        "ERROR": ["Database connection timeout after {ms}ms", "GET /api/payments 500 {ms}ms",
                  "Failed login user={u}"],
    }
    users = ["alice", "bob", "carol", "dave"]
    ips = ["10.0.0.5", "10.0.0.7", "10.0.1.12", "192.168.1.20"]
    lines = []
    for i in range(60):
        lvl = levels[int(rng.integers(0, len(levels)))]
        msg = msgs[lvl][int(rng.integers(0, len(msgs[lvl])))].format(
            u=users[i % 4], ms=int(rng.integers(20, 3000)), v=i % 9, p=int(rng.integers(76, 99)))
        lines.append(f"2026-11-20 10:{i // 2:02d}:{(i * 7) % 60:02d} {lvl} [{ips[i % 4]}] {msg}")
    (HERE / "app.log").write_text("\n".join(lines) + "\n")


def server_metrics():
    rows = []
    for i in range(60):
        server = ["web-01", "web-02", "db-01"][i % 3]
        rows.append({
            "timestamp": f"2026-11-20 {9 + i // 12:02d}:{(i % 12) * 5:02d}",
            "server": server,
            "cpu": round(float(rng.normal(55, 18)), 1),
            "memory": round(float(rng.normal(65, 12)), 1),
            "disk": round(float(rng.normal(70, 8)), 1),
            "response_ms": int(rng.normal(250, 90)),
        })
    df = pd.DataFrame(rows)
    df[["cpu", "memory", "disk"]] = df[["cpu", "memory", "disk"]].clip(1, 99.9)
    df["response_ms"] = df["response_ms"].clip(lower=40)
    # inject realistic dirt for the data-cleaning lesson
    for col, idx in [("cpu", [4, 17, 33]), ("memory", [8, 41]), ("response_ms", [12, 50])]:
        df[col] = df[col].astype("float")
        df.loc[idx, col] = np.nan
    df.loc[25, "server"] = " WEB-01 "
    df = pd.concat([df, df.iloc[[10]]], ignore_index=True)  # one duplicate row
    df.to_csv(HERE / "server_metrics.csv", index=False)


def sales():
    regions = ["North", "South", "East", "West"]
    products = ["Laptop", "Monitor", "Keyboard", "Mouse"]
    prices = {"Laptop": 900, "Monitor": 220, "Keyboard": 45, "Mouse": 25}
    rows = []
    for i in range(48):
        p = products[int(rng.integers(0, 4))]
        rows.append({"date": f"2026-{1 + i // 4:02d}-{1 + (i * 3) % 28:02d}", "region": regions[i % 4],
                     "product": p, "units": int(rng.integers(1, 30)), "unit_price": prices[p]})
    df = pd.DataFrame(rows)
    df.to_csv(HERE / "sales.csv", index=False)
    df.to_excel(HERE / "sales.xlsx", index=False, sheet_name="sales")


def house_prices():
    n = 200
    size = rng.integers(500, 3500, n)
    bedrooms = np.clip((size / 700).round() + rng.integers(-1, 2, n), 1, 6).astype(int)
    age = rng.integers(0, 40, n)
    distance = np.round(rng.uniform(1, 30, n), 1)
    price = 50000 + size * 150 + bedrooms * 10000 - age * 1200 - distance * 2500 + rng.normal(0, 20000, n)
    pd.DataFrame({"size_sqft": size, "bedrooms": bedrooms, "age_years": age, "distance_km": distance,
                  "price": price.round(-2).astype(int)}).to_csv(HERE / "house_prices.csv", index=False)


def server_failures():
    n = 400
    cpu = np.round(rng.uniform(5, 100, n), 1)
    mem = np.round(rng.uniform(10, 100, n), 1)
    disk = np.round(rng.uniform(10, 100, n), 1)
    errors = rng.poisson(3, n)
    resp = np.round(rng.normal(300, 120, n).clip(30), 0).astype(int)
    score = 0.05 * (cpu - 70) + 0.06 * (mem - 75) + 0.04 * (disk - 80) + 0.35 * (errors - 3) + 0.004 * (resp - 300)
    prob = 1 / (1 + np.exp(-score))
    failure = (rng.uniform(0, 1, n) < prob).astype(int)
    pd.DataFrame({"cpu_usage": cpu, "memory_usage": mem, "disk_usage": disk, "error_count": errors,
                  "response_time_ms": resp, "failure": failure}).to_csv(HERE / "server_failures.csv", index=False)


if __name__ == "__main__":
    servers()
    app_log()
    server_metrics()
    sales()
    house_prices()
    server_failures()
    print("Datasets written to", HERE)
