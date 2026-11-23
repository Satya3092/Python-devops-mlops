"""
Day 075 — DevOps Automation Project
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Testing the tool's logic with fake metrics
# ======================================================================
import argparse
import server_monitor as sm

# Replace the real metric readers with fakes - the rest of the tool runs unchanged
sm.get_hostname = lambda: "test-host"
sm.get_ip_address = lambda: "10.0.0.42"
sm.get_cpu_percent = lambda interval: 93.5
sm.get_memory = lambda: {"total_gb": 16, "used_percent": 81.0}


def broken_disk(path):
    raise PermissionError(f"cannot read {path}")


sm.get_disk = broken_disk

args = sm.parse_args(["--interval", "0"])
report = sm.collect(args)
print(sm.to_text(report).replace(report["timestamp"], "<time>").replace(report["os"], "<os>"))
print("exit code would be:", sm.STATUS_ORDER.get(report["overall"], 3))

# ======================================================================
# Example 2 — Running the real tool
# ======================================================================
import json
import subprocess
import sys
from pathlib import Path

result = subprocess.run(
    [sys.executable, "server_monitor.py", "--interval", "0.5", "--output-dir", "reports",
     "--log-file", "server_monitor.log"],
    capture_output=True, text=True, timeout=60,
)
print(result.stdout)
print("Exit code:", result.returncode)

latest = sorted(Path("reports").glob("*.json"))[-1]
data = json.loads(latest.read_text())
print("JSON keys:", list(data))
print("Log file lines:", len(Path("server_monitor.log").read_text().splitlines()))
