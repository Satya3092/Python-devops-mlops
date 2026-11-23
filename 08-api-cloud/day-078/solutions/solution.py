"""
Day 078 — Working with APIs using Requests: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from collections import Counter

import requests

import mock_api

BASE = mock_api.start()

# ===== Task 1 =====
def is_healthy(base_url):
    try:
        r = requests.get(f"{base_url}/health", timeout=2)
        return r.status_code == 200 and r.json().get("status") == "ok"
    except requests.RequestException:
        return False


print(is_healthy(BASE), is_healthy("http://127.0.0.1:9"))

# ===== Task 2 =====
items = requests.get(f"{BASE}/api/servers", timeout=5).json()["items"]
print(dict(Counter(s["env"] for s in items)))
print("Running CPU:", sum(s["cpu"] for s in items if s["status"] == "running"))

# ===== Task 3 =====
class InventoryClient:
    def __init__(self, base_url, timeout=5):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def server(self, server_id):
        r = self.session.get(f"{self.base_url}/api/servers/{server_id}", timeout=self.timeout)
        if r.status_code == 404:
            return None
        r.raise_for_status()
        return r.json()

    def create_server(self, name, env, cpu=2):
        r = self.session.post(f"{self.base_url}/api/servers", json={"name": name, "env": env, "cpu": cpu},
                              timeout=self.timeout)
        r.raise_for_status()
        return r.json()

    def delete_server(self, server_id):
        r = self.session.delete(f"{self.base_url}/api/servers/{server_id}", timeout=self.timeout)
        r.raise_for_status()
        return r.status_code


client = InventoryClient(BASE)
new = client.create_server("ml-gpu-01", "dev", cpu=16)
print("Created:", new)
print("Read back:", client.server(new["id"]))
print("Delete status:", client.delete_server(new["id"]))
print("After delete:", client.server(new["id"]))
