"""
Day 075 — DevOps Automation Project: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import csv
import json
import subprocess
import sys
from pathlib import Path

import server_monitor as sm

# ===== Task 1 =====
subprocess.run([sys.executable, "server_monitor.py", "--interval", "0.2", "--output-dir", "task_reports",
                "--log-file", "task.log"], capture_output=True, text=True, timeout=60)
folder = Path("task_reports")
json_files = list(folder.glob("*.json"))
print(f"Reports in folder: {len(json_files)} JSON, {len(list(folder.glob('*.txt')))} TXT")
print("Overall status:", json.loads(json_files[0].read_text())["overall"])

# ===== Task 2 =====
base = [sys.executable, "server_monitor.py", "--interval", "0.2", "--output-dir", "task_reports2", "--log-file", "task2.log"]
low = subprocess.run(base + ["--cpu-warn", "1", "--cpu-crit", "2"], capture_output=True, text=True, timeout=60)
high = subprocess.run(base + ["--cpu-warn", "100", "--cpu-crit", "101", "--mem-warn", "100", "--mem-crit", "101",
                              "--disk-warn", "100", "--disk-crit", "101"], capture_output=True, text=True, timeout=60)
print(f"Run with --cpu-warn 1 --cpu-crit 2: exit code {low.returncode} (CRITICAL expected on a busy CPU)")
print(f"Run with very high thresholds: exit code {high.returncode}")

# ===== Task 3 =====
report = sm.collect(sm.parse_args(["--interval", "0.2"]))
path = Path("history.csv")
new_file = not path.exists()
with path.open("a", newline="") as f:
    writer = csv.writer(f)
    if new_file:
        writer.writerow(["timestamp", "hostname", "metric", "value", "status"])
    for metric, check in report["checks"].items():
        writer.writerow([report["timestamp"], report["hostname"], metric, check["value"], check["status"]])
        print(f"{report['hostname']} {metric:<8}{check['value']:>6.1f}% {check['status']}")
print("history.csv rows:", len(path.read_text().splitlines()) - 1)
