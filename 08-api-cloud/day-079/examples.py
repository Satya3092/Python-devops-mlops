"""
Day 079 — GET and POST Requests
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — GET with params, POST with JSON and form data
# ======================================================================
import requests

import mock_api

BASE = mock_api.start()

r = requests.get(f"{BASE}/api/servers", params={"env": "prod"}, timeout=5)
print("GET  ", r.status_code, [s["name"] for s in r.json()["items"]])

payload = {"name": "cache-01", "env": "prod", "cpu": 2}
r = requests.post(f"{BASE}/api/servers", json=payload, timeout=5)
print("POST ", r.status_code, r.json(), "| Location:", r.headers["Location"])

r = requests.post(f"{BASE}/api/servers", json={"env": "prod"}, timeout=5)
print("POST (invalid)", r.status_code, r.json())

r = requests.post(f"{BASE}/api/servers", data="{not valid json", timeout=5,
                  headers={"Content-Type": "application/json"})
print("POST (bad JSON)", r.status_code, r.json())

r = requests.post(f"{BASE}/echo", json={"msg": "hi"}, headers={"X-Request-ID": "req-123"}, timeout=5)
print("JSON body sent :", r.json())
r = requests.post(f"{BASE}/echo", data={"user": "asha", "role": "admin"}, timeout=5)
print("Form body sent :", r.json()["body"], "|", r.json()["headers"]["Content-Type"])

# ======================================================================
# Example 2 — Pagination and retries with backoff
# ======================================================================
import time

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

import mock_api

BASE = mock_api.start()


def fetch_all(session, path, per_page=2):
    """Follow page numbers until every item is collected."""
    items, page = [], 1
    while True:
        data = session.get(f"{BASE}{path}", params={"page": page, "per_page": per_page}, timeout=5).json()
        items += data["items"]
        print(f"  page {page}: got {len(data['items'])} item(s)")
        if page * per_page >= data["total"]:
            return items
        page += 1


def get_with_backoff(session, url, attempts=4, base_delay=0.2):
    """Manual retry loop: retry 429/5xx with exponential backoff."""
    for attempt in range(1, attempts + 1):
        response = session.get(url, timeout=5)
        if response.status_code not in (429, 502, 503, 504):
            return response
        delay = base_delay * 2 ** (attempt - 1)
        print(f"  attempt {attempt}: {response.status_code}, retrying in {delay:.1f}s")
        time.sleep(delay)
    response.raise_for_status()


with requests.Session() as session:
    print("Pagination:")
    servers = fetch_all(session, "/api/servers")
    print("  all names:", [s["name"] for s in servers])

    print("Manual backoff on /flaky:")
    response = get_with_backoff(session, f"{BASE}/flaky")
    print("  final:", response.status_code, response.json())

    print("Automatic retries via urllib3 Retry:")
    retry = Retry(total=3, backoff_factor=0.1, status_forcelist=[429, 502, 503, 504],
                  allowed_methods=["GET"], respect_retry_after_header=False)
    session.mount("http://", HTTPAdapter(max_retries=retry))
    response = session.get(f"{BASE}/flaky", timeout=5)
    print("  final:", response.status_code, response.json())
