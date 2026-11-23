"""
Day 074 — Python Script for Server Health Monitoring: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import json
import socket

import psutil

# ===== Task 1 =====
def check_ports(host, ports):
    result = {}
    for port in ports:
        try:
            with socket.create_connection((host, port), timeout=0.5):
                result[port] = "open"
        except OSError:
            result[port] = "closed"
    return result


listener = socket.socket()
listener.bind(("127.0.0.1", 0))
listener.listen()
open_port = listener.getsockname()[1]
status = check_ports("127.0.0.1", [open_port, 1])
print("listening port:", status[open_port], "| port 1:", status[1])
listener.close()

# ===== Task 2 =====
def classify(value, warning, critical):
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "OK"


assert classify(10, 75, 90) == "OK"
assert classify(75, 75, 90) == "WARNING"
assert classify(80, 75, 90) == "WARNING"
assert classify(90, 75, 90) == "CRITICAL"
assert classify(99, 75, 90) == "CRITICAL"
print("all tests passed")

# ===== Task 3 =====
def classify(value, warning, critical):          # same helper as Task 2
    return "CRITICAL" if value >= critical else "WARNING" if value >= warning else "OK"


CODES = {"OK": 0, "WARNING": 1, "CRITICAL": 2}
THRESHOLDS = {"cpu": (75, 90), "memory": (80, 90), "disk": (80, 90)}


def health_check(metrics, thresholds=THRESHOLDS):
    statuses = {m: classify(v, *thresholds[m]) for m, v in metrics.items()}
    worst = max(statuses.values(), key=CODES.get)
    problems = ", ".join(f"{m}={s}" for m, s in statuses.items() if s != "OK")
    return worst, CODES[worst], problems


for name, metrics in [("web-01", {"cpu": 40, "memory": 50, "disk": 60}),
                      ("db-01", {"cpu": 40, "memory": 70, "disk": 95})]:
    status, code, problems = health_check(metrics)
    print(f"{name}: {status} (exit {code})" + (f" -> {problems}" if problems else ""))
live = {"cpu": psutil.cpu_percent(interval=0.5), "memory": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("/").percent}
print(json.dumps(live))
status, code, _ = health_check(live)
print(f"Local check: {status} (exit {code})")
