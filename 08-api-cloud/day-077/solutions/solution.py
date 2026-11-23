"""
Day 077 — REST API Concepts: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
import urllib.error
import urllib.request

import mock_api

BASE = mock_api.start()


def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=5) as r:
            body = r.read()
            return r.status, json.loads(body) if body else None
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")

# ===== Task 1 =====
base = "/apis/apps/v1/namespaces/prod/deployments"
for op, method, path in [("list", "GET", base), ("get", "GET", f"{base}/api"), ("create", "POST", base),
                         ("update", "PUT", f"{base}/api"), ("delete", "DELETE", f"{base}/api")]:
    print(f"{op:<7}{method:<7}{path}")

# ===== Task 2 =====
for env in ("prod", "dev"):
    status, data = call("GET", f"/api/servers?env={env}")
    print(env, [s["name"] for s in data["items"]], "total:", data["total"])

# ===== Task 3 =====
for i in range(5):
    call("POST", "/api/servers", {"name": f"extra-{i}", "env": "dev"})


def get_all(per_page=2):
    items, page, requests_made = [], 1, 0
    while True:
        _, data = call("GET", f"/api/servers?per_page={per_page}&page={page}")
        requests_made += 1
        items.extend(data["items"])
        if len(items) >= data["total"]:
            return items, requests_made
        page += 1


servers, n = get_all()
print(f"{len(servers)} servers collected in {n} requests")
print([s["name"] for s in servers])
