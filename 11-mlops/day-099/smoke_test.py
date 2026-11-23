"""smoke_test.py - test a RUNNING service (local uvicorn or Docker container).

Usage:  BASE_URL=http://127.0.0.1:8000 python smoke_test.py
Exit code 0 = all checks passed (use it in CI after 'docker run').
"""
import os
import sys
import time

import requests

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
RISKY = {"cpu_usage": 93, "memory_usage": 91, "disk_usage": 88, "error_count": 7, "response_time_ms": 650}


def wait_until_healthy(timeout=30):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            if requests.get(f"{BASE_URL}/health", timeout=2).json().get("model_loaded"):
                return True
        except requests.RequestException:
            pass
        time.sleep(1)
    return False


def main():
    checks = []
    checks.append(("service healthy", wait_until_healthy()))
    r = requests.post(f"{BASE_URL}/predict", json=RISKY, timeout=5)
    checks.append(("predict returns 200", r.status_code == 200))
    checks.append(("risky server flagged", r.ok and r.json()["failure"] is True))
    bad = requests.post(f"{BASE_URL}/predict", json={**RISKY, "cpu_usage": -5}, timeout=5)
    checks.append(("invalid input rejected (422)", bad.status_code == 422))
    for name, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {name}")
    return 0 if all(ok for _, ok in checks) else 1


if __name__ == "__main__":
    sys.exit(main())
