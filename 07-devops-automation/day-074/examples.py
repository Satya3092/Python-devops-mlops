"""
Day 074 — Python Script for Server Health Monitoring
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Testable evaluation logic with fake metrics
# ======================================================================
STATUS_CODE = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}
THRESHOLDS = {"cpu": (75, 90), "memory": (80, 90), "disk": (80, 90), "load_per_core": (1.0, 2.0)}


def evaluate(metric, value):
    warning, critical = THRESHOLDS[metric]
    if value is None:
        return "UNKNOWN"
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "OK"


def overall(statuses):
    return max(statuses, key=STATUS_CODE.get)


fake_servers = {
    "web-01": {"cpu": 35.0, "memory": 61.2, "disk": 54.0, "load_per_core": 0.4},
    "web-02": {"cpu": 82.5, "memory": 71.0, "disk": 66.3, "load_per_core": 1.3},
    "db-01": {"cpu": 47.0, "memory": 93.4, "disk": 91.0, "load_per_core": 0.9},
    "new-vm": {"cpu": None, "memory": 20.0, "disk": 10.0, "load_per_core": 0.1},
}
for host, metrics in fake_servers.items():
    statuses = {m: evaluate(m, v) for m, v in metrics.items()}
    result = overall(statuses.values())
    problems = {m: s for m, s in statuses.items() if s != "OK"}
    print(f"{host:<7} {result:<9} exit={STATUS_CODE[result]}  {problems}")

# ======================================================================
# Example 2 — Live health check: system metrics + ports + HTTP endpoint
# ======================================================================
import json
import os
import socket
import sys
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

import psutil

STATUS_CODE = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}


def level(value, warning, critical):
    return "CRITICAL" if value >= critical else "WARNING" if value >= warning else "OK"


def port_open(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def http_ok(url, timeout=2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except OSError:
        return False


# A tiny local web server so the HTTP check has something to talk to
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200 if self.path == "/health" else 404)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 0), Health)
threading.Thread(target=server.serve_forever, daemon=True).start()
app_port = server.server_address[1]

load_per_core = os.getloadavg()[0] / psutil.cpu_count() if hasattr(os, "getloadavg") else 0.0
checks = {
    "cpu": level(psutil.cpu_percent(interval=0.5), 75, 90),
    "memory": level(psutil.virtual_memory().percent, 80, 90),
    "disk": level(psutil.disk_usage("/").percent, 80, 90),
    "load": level(load_per_core, 1.0, 2.0),
    "app_port": "OK" if port_open("127.0.0.1", app_port) else "CRITICAL",
    "app_http": "OK" if http_ok(f"http://127.0.0.1:{app_port}/health") else "CRITICAL",
    "postgres_port": "OK" if port_open("127.0.0.1", 5432) else "WARNING",
}
server.shutdown()

worst = max(checks.values(), key=STATUS_CODE.get)
print(json.dumps({"host": socket.gethostname(), "status": worst, "checks": checks}, indent=2))
print("Nagios-style line:", f"{worst} - " + ", ".join(f"{k}={v}" for k, v in checks.items() if v != "OK"))
print("Would exit with code", STATUS_CODE[worst])   # real script: sys.exit(STATUS_CODE[worst])
