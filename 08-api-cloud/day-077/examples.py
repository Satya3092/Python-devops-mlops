"""
Day 077 — REST API Concepts
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — A tiny REST client with urllib
# ======================================================================
import json
import urllib.error
import urllib.request

import mock_api

BASE = mock_api.start()


def call(method, path, payload=None):
    """Send a request and return (status, parsed JSON or None)."""
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(BASE + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            body = response.read()
            return response.status, json.loads(body) if body else None
    except urllib.error.HTTPError as error:          # 4xx / 5xx responses
        return error.code, json.loads(error.read() or b"null")


print("LIST  ", call("GET", "/api/servers"))
print("READ  ", call("GET", "/api/servers/1"))
print("MISS  ", call("GET", "/api/servers/99"))

# ======================================================================
# Example 2 — Full CRUD lifecycle and idempotency
# ======================================================================
import json
import urllib.error
import urllib.request

import mock_api

BASE = mock_api.start()


def call(method, path, payload=None):
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(BASE + path, data=data, method=method,
                                     headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(request, timeout=5) as response:
            body = response.read()
            return response.status, json.loads(body) if body else None
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read() or b"null")


status, created = call("POST", "/api/servers", {"name": "api-03", "env": "staging", "cpu": 2})
print(f"CREATE  {status}  {created}")
server_id = created["id"]

status, updated = call("PUT", f"/api/servers/{server_id}", {"status": "running", "cpu": 4})
print(f"UPDATE  {status}  {updated}")

# PUT is idempotent: sending the same update again changes nothing
status, again = call("PUT", f"/api/servers/{server_id}", {"status": "running", "cpu": 4})
print(f"UPDATE  {status}  same result? {again == updated}")

# POST is NOT idempotent: two identical POSTs create two servers
ids = [call("POST", "/api/servers", {"name": "dup", "env": "dev"})[1]["id"] for _ in range(2)]
print("Two POSTs created ids:", ids)

print("INVALID", call("POST", "/api/servers", {"name": "no-env"}))
print("DELETE ", call("DELETE", f"/api/servers/{server_id}"))
print("DELETE again (idempotent outcome: it's gone):", call("DELETE", f"/api/servers/{server_id}")[0])

status, page = call("GET", "/api/servers?per_page=2&page=1")
print(f"PAGE 1 of {page['total']} servers ->", [s["name"] for s in page["items"]])
