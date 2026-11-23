"""
Day 049 — Append Mode
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Appending vs overwriting
# ======================================================================
with open("visits.txt", "w", encoding="utf-8") as f:
    f.write("visit 1\n")

with open("visits.txt", "a", encoding="utf-8") as f:
    f.write("visit 2\n")
    f.write("visit 3\n")

with open("visits.txt", encoding="utf-8") as f:
    print(f.read(), end="")

with open("visits.txt", "a", encoding="utf-8") as f:
    f.write("visit 4\n")

with open("visits.txt", encoding="utf-8") as f:
    print("Total visits recorded:", len(f.readlines()))

# ======================================================================
# Example 2 — A tiny logger and a metrics history CSV
# ======================================================================
from datetime import datetime, timedelta

LOG_FILE = "deploy.log"
start = datetime(2026, 11, 20, 10, 0, 0)        # fixed time so output is reproducible


def log(level, message, when):
    """Append one timestamped line to the log file."""
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{when:%Y-%m-%d %H:%M:%S} [{level}] {message}\n")


steps = ["Pulling image", "Stopping old container", "Starting new container", "Health check passed"]
for i, step in enumerate(steps):
    log("INFO", step, start + timedelta(seconds=i * 5))
log("INFO", "Deployment finished", start + timedelta(seconds=20))

with open(LOG_FILE, encoding="utf-8") as f:
    print(f.read(), end="")

# Append metrics rows; write the header only if the file is new
import os
METRICS = "cpu_history.csv"
for minute, cpu in enumerate([35.2, 41.8, 77.5]):
    new_file = not os.path.exists(METRICS)
    with open(METRICS, "a", encoding="utf-8") as f:
        if new_file:
            f.write("timestamp,cpu_percent\n")
        f.write(f"{start + timedelta(minutes=minute):%H:%M},{cpu}\n")

with open(METRICS, encoding="utf-8") as f:
    print(f.read(), end="")
