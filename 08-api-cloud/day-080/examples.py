"""
Day 080 — API Authentication and Tokens
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — API keys from the environment and what Basic auth really sends
# ======================================================================
import base64
import os

import requests

import mock_api

BASE = mock_api.start()

# Simulate what CI/Kubernetes would inject. In real life: export REPORT_API_KEY=... (never in code!)
os.environ.setdefault("REPORT_API_KEY", "demo-api-key")
api_key = os.environ["REPORT_API_KEY"]
print("Using key:", api_key[:4] + "*" * (len(api_key) - 4))

r = requests.get(f"{BASE}/api/keyed/report", headers={"X-API-Key": api_key}, timeout=5)
print("With key   :", r.status_code, r.json())
r = requests.get(f"{BASE}/api/keyed/report", headers={"X-API-Key": "wrong"}, timeout=5)
print("Wrong key  :", r.status_code, r.json())

r = requests.post(f"{BASE}/echo", auth=("jenkins-bot", "s3cr3t"), timeout=5)
header = r.json()["headers"]["Authorization"]
print("Basic header sent:", header)
print("Decoded (anyone can do this!):", base64.b64decode(header.split()[1]).decode())

# ======================================================================
# Example 2 — A token-aware client that refreshes automatically
# ======================================================================
import os
import time

import requests

import mock_api

BASE = mock_api.start()
os.environ.setdefault("API_CLIENT_ID", "demo-client")
os.environ.setdefault("API_CLIENT_SECRET", "demo-secret")


class TokenClient:
    """Gets a bearer token, caches it until expiry, refreshes on 401."""

    def __init__(self, base_url, token_ttl=60):
        self.base_url = base_url
        self.token_ttl = token_ttl
        self.session = requests.Session()
        self._token = None
        self._expires_at = 0
        self.tokens_fetched = 0

    def _fetch_token(self):
        response = self.session.post(f"{self.base_url}/api/token", timeout=5, json={
            "client_id": os.environ["API_CLIENT_ID"],
            "client_secret": os.environ["API_CLIENT_SECRET"],
            "ttl": self.token_ttl,
        })
        response.raise_for_status()
        data = response.json()
        self._token = data["access_token"]
        self._expires_at = time.time() + data["expires_in"] - 0.2     # small safety margin
        self.tokens_fetched += 1
        print(f"  (fetched token {self._token[:4]}****, valid {data['expires_in']}s)")

    def _headers(self):
        if self._token is None or time.time() >= self._expires_at:
            self._fetch_token()
        return {"Authorization": f"Bearer {self._token}"}

    def get(self, path):
        response = self.session.get(f"{self.base_url}{path}", headers=self._headers(), timeout=5)
        if response.status_code == 401:                 # expired/revoked -> refresh once
            print("  got 401, refreshing token and retrying once")
            self._token = None
            response = self.session.get(f"{self.base_url}{path}", headers=self._headers(), timeout=5)
        response.raise_for_status()
        return response.json()


r = requests.get(f"{BASE}/api/secure/metrics", timeout=5)
print("No token      :", r.status_code, r.json(), "| WWW-Authenticate:", r.headers.get("WWW-Authenticate"))

client = TokenClient(BASE, token_ttl=1)
print("Call 1:", client.get("/api/secure/metrics"))
print("Call 2:", client.get("/api/secure/metrics"))          # cached token reused
time.sleep(1.2)                                              # let the token expire
print("Call 3:", client.get("/api/secure/metrics"))          # refreshed automatically
print("Tokens fetched:", client.tokens_fetched)

os.environ["API_CLIENT_SECRET"] = "wrong-secret"
try:
    TokenClient(BASE).get("/api/secure/metrics")
except requests.HTTPError as error:
    print("Bad credentials ->", error.response.status_code, error.response.json())
