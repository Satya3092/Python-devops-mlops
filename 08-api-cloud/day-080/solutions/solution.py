"""
Day 080 — API Authentication and Tokens: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import base64
import os
import time

import requests

import mock_api

BASE = mock_api.start()

# ===== Task 1 =====
def mask(secret, visible=4):
    return secret[:visible] + "****"


os.environ.setdefault("MY_API_KEY", "demo-api-key")
print(mask(os.environ["MY_API_KEY"]))

# ===== Task 2 =====
def auth_headers(kind, value):
    if kind == "api_key":
        return {"X-API-Key": value}
    if kind == "bearer":
        return {"Authorization": f"Bearer {value}"}
    if kind == "basic":
        encoded = base64.b64encode(f"{value[0]}:{value[1]}".encode()).decode()
        return {"Authorization": f"Basic {encoded}"}
    raise ValueError(kind)


print(auth_headers("api_key", "k-123"))
print(auth_headers("bearer", "tok-0001"))
mine = auth_headers("basic", ("bot", "pw"))
print(mine)
theirs = requests.post(f"{BASE}/echo", auth=("bot", "pw"), timeout=5).json()["headers"]["Authorization"]
print("match:", mine["Authorization"] == theirs)

# ===== Task 3 =====
class TokenClient:
    def __init__(self, base_url, ttl):
        missing = [v for v in ("API_CLIENT_ID", "API_CLIENT_SECRET") if v not in os.environ]
        if missing:
            raise RuntimeError(f"set these environment variables first: {missing}")
        self.base_url, self.ttl = base_url, ttl
        self.token, self.expires_at, self.fetched = None, 0, 0

    def get(self, path):
        if self.token is None or time.time() >= self.expires_at:
            r = requests.post(f"{self.base_url}/api/token", timeout=5, json={
                "client_id": os.environ["API_CLIENT_ID"], "client_secret": os.environ["API_CLIENT_SECRET"],
                "ttl": self.ttl})
            r.raise_for_status()
            self.token = r.json()["access_token"]
            self.expires_at = time.time() + self.ttl - 0.1
            self.fetched += 1
        r = requests.get(f"{self.base_url}{path}", headers={"Authorization": f"Bearer {self.token}"}, timeout=5)
        r.raise_for_status()
        return r.json()


for var in ("API_CLIENT_ID", "API_CLIENT_SECRET"):
    os.environ.pop(var, None)
try:
    TokenClient(BASE, ttl=1)
except RuntimeError as error:
    print("Error:", error)
os.environ.update({"API_CLIENT_ID": "demo-client", "API_CLIENT_SECRET": "demo-secret"})
client = TokenClient(BASE, ttl=1)
for poll in range(1, 4):
    print(f"poll {poll}: cpu={client.get('/api/secure/metrics')['cpu']}")
    time.sleep(0.6)
print("Tokens fetched:", client.fetched)
