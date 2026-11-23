"""
Day 076 — HTTP and HTTPS Fundamentals: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import sys
from pathlib import Path

# Let this file import helper modules that live in the day folder (one level up)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import http.client
import json
from urllib.parse import parse_qs, urlparse

import mock_api

# ===== Task 1 =====
def describe_url(url):
    p = urlparse(url)
    port = p.port or (443 if p.scheme == "https" else 80)
    print(f"{p.scheme} | {p.hostname} | {port} | {p.path or '/'} | {parse_qs(p.query)}")


describe_url("https://registry.example.com/v2/orders/tags/list?n=5")
describe_url("http://10.0.0.5:9100/metrics")

# ===== Task 2 =====
def classify_status(code):
    kind = {1: "informational", 2: "success", 3: "redirect", 4: "client error", 5: "server error"}[code // 100]
    if code in (429, 502, 503, 504):
        kind += " (retry later)"
    return kind


for code in (200, 204, 302, 404, 429, 500, 503):
    print(code, classify_status(code))

# ===== Task 3 =====
base = urlparse(mock_api.start())
conn = http.client.HTTPConnection(base.hostname, base.port, timeout=5)
conn.request("GET", "/api/servers?env=prod")
for server in json.loads(conn.getresponse().read())["items"]:
    print(server["name"])
conn.request("GET", "/status/503")
response = conn.getresponse()
response.read()
print(response.status, response.reason)
conn.close()
