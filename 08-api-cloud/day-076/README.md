# Day 076 — HTTP and HTTPS Fundamentals

[⬅ Day 075](../../07-devops-automation/day-075/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 077 ➡](../../08-api-cloud/day-077/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain how an HTTP request/response works (methods, URLs, headers, body, status codes)
- Break a URL into its parts and build query strings safely
- Explain what HTTPS adds (TLS) and make a raw HTTP request with the standard library

## 2. Topic Explanation

**HTTP** (HyperText Transfer Protocol) is how clients (browsers, `curl`, Python scripts) talk to servers (websites, APIs, Kubernetes API server, AWS). It is a simple **request → response** conversation.

**A request** has:
- a **method**: `GET` (read), `POST` (create), `PUT`/`PATCH` (update), `DELETE`
- a **URL**: `https://api.example.com:443/v1/servers?env=prod`
- **headers**: metadata like `Content-Type: application/json`, `Authorization: Bearer ...`
- an optional **body** (e.g. JSON for POST)

**A response** has:
- a **status code**: `2xx` success, `3xx` redirect, `4xx` client error, `5xx` server error
- headers and a body

| Code | Meaning | Typical cause |
|---|---|---|
| 200 OK / 201 Created / 204 No Content | success | |
| 301 / 302 | redirect | moved URL, HTTP → HTTPS |
| 400 Bad Request | invalid input | malformed JSON |
| 401 Unauthorized | not authenticated | missing/expired token |
| 403 Forbidden | authenticated but not allowed | IAM/RBAC |
| 404 Not Found | wrong URL/resource | |
| 429 Too Many Requests | rate limited | slow down, retry later |
| 500 / 502 / 503 / 504 | server-side problems | bug, bad gateway, overloaded, timeout |

**URL anatomy:** `scheme://host:port/path?query#fragment`.

**HTTPS** = HTTP inside **TLS** encryption. TLS gives *confidentiality* (nobody can read the traffic), *integrity* (nobody can change it) and *authentication* (the certificate proves you're talking to the real server). Default ports: 80 for HTTP, 443 for HTTPS. Never disable certificate verification in production.

Analogy: HTTP is sending a postcard; HTTPS is sending the same letter in a sealed, tamper-proof envelope with an ID check at the door.

> These examples use [`mock_api.py`](mock_api.py), a tiny local REST API included in this folder, so everything works offline and gives the same results every time. Today uses only the standard library.

## 3. Syntax

```http
GET /api/servers?env=prod HTTP/1.1          <- request line: METHOD PATH VERSION
Host: api.example.com                       <- headers
Accept: application/json

HTTP/1.1 200 OK                             <- status line
Content-Type: application/json              <- headers
                                            <- blank line
{"items": [...]}                            <- body
```

| Part | Meaning |
|---|---|
| `method` | What you want to do: GET, POST, PUT, PATCH, DELETE. |
| `path + query` | Which resource, with filters after `?`. |
| `headers` | Key: value metadata (content type, auth, caching...). |
| `status code` | 3-digit result; first digit is the class. |
| `body` | The data (often JSON). |

## 4. Example 1 — Basic Example: Dissecting URLs and status codes

```python
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
```

## 5. Example 2 — Practical Example: A raw HTTP conversation with http.client

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `urlparse` splits a URL into scheme, host, port, path, query and fragment; `parse_qs` turns the query into a dict.
- `urlencode` builds a query string and **escapes** special characters (`space` → `+`, `&` → `%26`) — never glue user input into URLs by hand.
- `HTTPStatus(code).phrase` gives the official name for any status code.

**Example 2**
- `mock_api.start()` launches the local API in a background thread and returns its URL.
- `http.client` is the low-level HTTP client in the standard library. You can see each part of the conversation: method + path + headers → status line + headers + body.
- The POST sends a JSON body with `Content-Type: application/json`; the API answers **201 Created** plus a `Location` header pointing to the new resource.
- An unknown path returns **404**. (Tomorrow you'll see how this maps to REST design; Day 78 replaces `http.client` with the much friendlier `requests`.)

## 7. Expected Output

**Example 1:**

```text
scheme  : https
host    : api.example.com
port    : 8443
path    : /v1/servers
query   : {'env': ['prod'], 'limit': ['10']}
fragment: results
Safe query string: env=prod&owner=team+web&tag=a%26b
Quoted path part : reports/2026%20Q4.pdf
Joined URL       : https://api.example.com/v1/servers/42
200 OK                     class 2xx
201 Created                class 2xx
301 Moved Permanently      class 3xx
401 Unauthorized           class 4xx
403 Forbidden              class 4xx
404 Not Found              class 4xx
429 Too Many Requests      class 4xx
500 Internal Server Error  class 5xx
503 Service Unavailable    class 5xx
```

**Example 2:**

```text
Status line : 200 OK
Content-Type: application/json
Server      : MockAPI/1.0
Body        : {'status': 'ok', 'version': '1.0.0'}
POST status : 201 Created | Location: /api/servers/4
Created     : {'id': 4, 'name': 'web-09', 'env': 'staging', 'cpu': 2, 'status': 'provisioning'}
Missing page: 404 Not Found {'error': 'no route for GET /does-not-exist'}
```

## 8. Common Mistakes

**1. Treating every non-200 as an exception**

201, 202 and 204 are successes too. Check the status *class* (`200 <= code < 300`).

**2. Building URLs with string concatenation**

Spaces and `&` in values break the URL or change its meaning. Use `urlencode` / `params=`.

**3. Disabling TLS verification**

`verify=False` (requests) or ignoring certificate errors removes HTTPS's protection. Fix the CA bundle instead.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — URL inspector:** Write `describe_url(url)` that prints scheme, host, port (default 443 for https / 80 for http when missing), path and query dict. Test it on two URLs.
- **Task 2 (Medium) — Status classifier:** Write `classify_status(code)` returning `success`, `redirect`, `client error`, `server error` or `informational`, plus `retry` advice for 429/502/503/504. Print a table for 200, 204, 302, 404, 429, 500, 503.
- **Task 3 (Practical Challenge) — Raw client:** Using `http.client` and the mock API, GET `/api/servers?env=prod` and print each server name, then GET `/status/503` and print the status and reason. Close the connection at the end.

## 10. DevOps/MLOps Connection

- **DevOps:** health checks, load balancer probes, webhooks (GitHub → Jenkins), container registries and the Kubernetes API are all HTTP. Reading status codes quickly is a core troubleshooting skill (502 = upstream down, 504 = upstream slow).
- **Cloud:** every AWS API call is an HTTPS request signed with your credentials.
- **MLOps:** models are served over HTTP (Day 98); clients send JSON features and receive predictions.

## 11. Interview Questions

**Q1. What is the difference between 401 and 403?**

<details><summary>Show answer</summary>

401 means not authenticated (no/invalid credentials); 403 means authenticated but not authorised for that resource.

</details>

**Q2. What does TLS provide in HTTPS?**

<details><summary>Show answer</summary>

Encryption (confidentiality), integrity protection and server authentication via certificates.

</details>

**Q3. Which status codes are usually safe to retry?**

<details><summary>Show answer</summary>

429 (after Retry-After), 502, 503, 504 and network timeouts — for idempotent requests.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 76 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 075](../../07-devops-automation/day-075/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 077 ➡](../../08-api-cloud/day-077/README.md)
