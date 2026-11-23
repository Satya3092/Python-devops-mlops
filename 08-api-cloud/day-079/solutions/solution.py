"""
Day 079 — GET and POST Requests: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import time

import requests

import mock_api

BASE = mock_api.start()

# ===== Task 1 =====
r = requests.get(f"{BASE}/api/servers", params={"env": "dev", "per_page": 1}, timeout=5)
print(r.url.replace(BASE, ""))
print([s["name"] for s in r.json()["items"]])

# ===== Task 2 =====
new_servers = [{"name": "etl-01", "env": "dev"}, {"name": "orphan"}, {"name": "etl-02", "env": "dev", "cpu": 8}]
created = 0
for payload in new_servers:
    r = requests.post(f"{BASE}/api/servers", json=payload, timeout=5)
    if r.status_code == 201:
        created += 1
        print("created", r.json()["id"])
    else:
        print(f"failed {payload['name']}: {r.status_code} {r.json()}")
print("Created:", created)

# ===== Task 3 =====
def resilient_get(url, max_attempts=5):
    delay = 0.1
    for attempt in range(1, max_attempts + 1):
        try:
            r = requests.get(url, timeout=2)
            if r.status_code != 503:
                r.raise_for_status()
                print(f"  success on attempt {attempt}")
                return r.json()
            reason = "503"
        except requests.Timeout:
            reason = "timeout"
        print(f"  attempt {attempt} failed ({reason})")
        time.sleep(delay)
        delay *= 2
    raise RuntimeError(f"gave up after {max_attempts} attempts: {url.replace(BASE, '')}")


print(resilient_get(f"{BASE}/flaky"))
try:
    resilient_get(f"{BASE}/status/503", max_attempts=3)
except RuntimeError as error:
    print("RuntimeError:", error)
