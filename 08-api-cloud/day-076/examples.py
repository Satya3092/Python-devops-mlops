"""
Day 076 — HTTP and HTTPS Fundamentals
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Dissecting URLs and status codes
# ======================================================================
from http import HTTPStatus
from urllib.parse import urlencode, urljoin, urlparse, parse_qs, quote

url = "https://api.example.com:8443/v1/servers?env=prod&limit=10#results"
parts = urlparse(url)
print("scheme  :", parts.scheme)
print("host    :", parts.hostname)
print("port    :", parts.port)
print("path    :", parts.path)
print("query   :", parse_qs(parts.query))
print("fragment:", parts.fragment)

params = {"env": "prod", "owner": "team web", "tag": "a&b"}
print("Safe query string:", urlencode(params))
print("Quoted path part :", quote("reports/2026 Q4.pdf"))
print("Joined URL       :", urljoin("https://api.example.com/v1/", "servers/42"))

for code in (200, 201, 301, 401, 403, 404, 429, 500, 503):
    status = HTTPStatus(code)
    print(f"{code} {status.phrase:<22} class {code // 100}xx")

# ======================================================================
# Example 2 — A raw HTTP conversation with http.client
# ======================================================================
import http.client
import json
from urllib.parse import urlparse

import mock_api

base = urlparse(mock_api.start())                 # local API, no internet needed
conn = http.client.HTTPConnection(base.hostname, base.port, timeout=5)

conn.request("GET", "/health", headers={"Accept": "application/json", "User-Agent": "day76-demo"})
response = conn.getresponse()
print("Status line :", response.status, response.reason)
print("Content-Type:", response.getheader("Content-Type"))
print("Server      :", response.getheader("Server").split()[0])
print("Body        :", json.loads(response.read()))

body = json.dumps({"name": "web-09", "env": "staging"})
conn.request("POST", "/api/servers", body=body, headers={"Content-Type": "application/json"})
response = conn.getresponse()
print("POST status :", response.status, response.reason, "| Location:", response.getheader("Location"))
print("Created     :", json.loads(response.read()))

conn.request("GET", "/does-not-exist")
response = conn.getresponse()
print("Missing page:", response.status, response.reason, json.loads(response.read()))
conn.close()
