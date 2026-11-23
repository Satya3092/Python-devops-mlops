"""
Day 078 — Working with APIs using Requests
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — First requests
# ======================================================================
import requests

import mock_api

BASE = mock_api.start()

response = requests.get(f"{BASE}/health", timeout=5)
print("Status:", response.status_code, "| ok:", response.ok)
print("Content-Type:", response.headers["content-type"])
print("JSON:", response.json())

response = requests.get(f"{BASE}/api/servers", params={"env": "prod", "per_page": 5}, timeout=5)
print("Final URL path:", response.url.replace(BASE, ""))
for server in response.json()["items"]:
    print(f"  {server['id']} {server['name']:<8} {server['status']}")

response = requests.get(f"{BASE}/api/servers/99", timeout=5)
print("Missing server:", response.status_code, response.json())
try:
    response.raise_for_status()
except requests.HTTPError as error:
    print("raise_for_status ->", type(error).__name__, error.response.status_code)

# ======================================================================
# Example 2 — A reusable API client class with a Session
# ======================================================================
import requests

import mock_api


class InventoryClient:
    """Small wrapper around the inventory REST API."""

    def __init__(self, base_url, timeout=5):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": "inventory-client/1.0", "Accept": "application/json"})

    def _get(self, path, **params):
        response = self.session.get(f"{self.base_url}{path}", params=params, timeout=self.timeout)
        response.raise_for_status()
        return response.json()

    def health(self):
        return self._get("/health")["status"]

    def servers(self, env=None):
        params = {"env": env} if env else {}
        return self._get("/api/servers", **params)["items"]

    def server(self, server_id):
        try:
            return self._get(f"/api/servers/{server_id}")
        except requests.HTTPError as error:
            if error.response.status_code == 404:
                return None
            raise


client = InventoryClient(mock_api.start())
print("API health:", client.health())
print("Prod servers:", [s["name"] for s in client.servers(env="prod")])
print("Server 3:", client.server(3))
print("Server 42:", client.server(42))

# Network-level errors are different from HTTP errors
try:
    requests.get("http://127.0.0.1:9/never-listening", timeout=2)
except requests.ConnectionError:
    print("ConnectionError: nothing is listening on that port")
try:
    requests.get(f"{client.base_url}/slow", params={"seconds": 2}, timeout=0.5)
except requests.Timeout:
    print("Timeout: the API took longer than 0.5 s")
