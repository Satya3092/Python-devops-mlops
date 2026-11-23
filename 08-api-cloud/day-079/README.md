# Day 079 — GET and POST Requests

[⬅ Day 078](../../08-api-cloud/day-078/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 080 ➡](../../08-api-cloud/day-080/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Send query parameters, JSON bodies, form data and custom headers
- Handle pagination and validation errors from POST
- Retry transient failures (503/429) with backoff — safely

## 2. Topic Explanation

**GET** reads data. Inputs travel in the **URL query string** (`params=`). GET must not change server state, so it's safe to repeat and cache.

**POST** sends data to create something (or trigger an action). Inputs travel in the **body**:
- `json=payload` → JSON body + `Content-Type: application/json` (most APIs).
- `data=payload` → HTML-form encoding (`application/x-www-form-urlencoded`) — older APIs, login forms.
- `files=` → multipart uploads.

Robust API automation also needs:
- **Pagination loops** — keep requesting `page=2, 3, ...` (or follow a `next` link / cursor) until done.
- **Validation errors** — a 400/422 response body usually explains *what* is wrong; show it.
- **Retries with exponential backoff** for transient errors (`429`, `502`, `503`, `504`, timeouts). Respect the `Retry-After` header. Retry **only idempotent** requests (GET/PUT/DELETE) automatically; for POST, use idempotency keys if the API supports them.

`requests` can do retries for you through `urllib3`'s `Retry` mounted on an `HTTPAdapter` — the same mechanism the AWS SDK and many tools use.

> These examples use [`mock_api.py`](mock_api.py), a tiny local REST API included in this folder, so everything works offline and gives the same results every time. Install requests first: `pip install requests`.

## 3. Syntax

```python
requests.get(url, params={"page": 2}, timeout=5)
requests.post(url, json={"name": "web-05"}, headers={"X-Request-ID": "abc"}, timeout=5)
requests.post(url, data={"user": "a"}, timeout=5)        # form encoding

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
retry = Retry(total=3, backoff_factor=0.5, status_forcelist=[429, 502, 503, 504], allowed_methods=["GET"])
session.mount("http://", HTTPAdapter(max_retries=retry))
```

| Part | Meaning |
|---|---|
| `params=` | Query string for GET. |
| `json=` | JSON body; sets Content-Type automatically. |
| `data=` | Form-encoded body. |
| `Retry(...)` | Automatic retries with backoff for selected status codes and methods. |

## 4. Example 1 — Basic Example: GET with params, POST with JSON and form data

```python
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
```

## 5. Example 2 — Practical Example: Pagination and retries with backoff

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `params=` filters the GET; `json=` serialises the body and sets the content type.
- The API returns **201** with a `Location` header for the new resource.
- Missing fields → **422** with a helpful message; broken JSON → **400**.
- The `/echo` endpoint shows exactly what was sent: `json=` sends JSON, `data=` sends form-encoded `user=asha&role=admin`.

**Example 2**
- `fetch_all` loops through pages until `page * per_page >= total`.
- `/flaky` fails twice with 503 before succeeding. `get_with_backoff` waits 0.2 s, 0.4 s, ... between attempts (exponential backoff).
- The same behaviour can be configured declaratively with `urllib3.Retry` mounted on the session; `allowed_methods=["GET"]` prevents automatic retries of non-idempotent POSTs.

## 7. Expected Output

**Example 1:**

```text
GET   200 ['web-01', 'web-02']
POST  201 {'id': 4, 'name': 'cache-01', 'env': 'prod', 'cpu': 2, 'status': 'provisioning'} | Location: /api/servers/4
POST (invalid) 422 {'error': 'missing fields', 'fields': ['name']}
POST (bad JSON) 400 {'error': 'request body is not valid JSON'}
JSON body sent : {'headers': {'User-Agent': 'python-requests/2.34.2', 'X-Request-ID': 'req-123', 'Content-Type': 'application/json'}, 'body': '{"msg": "hi"}'}
Form body sent : user=asha&role=admin | application/x-www-form-urlencoded
```

**Example 2:**

```text
Pagination:
  page 1: got 2 item(s)
  page 2: got 1 item(s)
  all names: ['web-01', 'web-02', 'batch-01']
Manual backoff on /flaky:
  attempt 1: 503, retrying in 0.2s
  attempt 2: 503, retrying in 0.4s
  final: 200 {'status': 'ok', 'attempt': 3}
Automatic retries via urllib3 Retry:
  final: 200 {'status': 'ok', 'attempt': 6}
```

## 8. Common Mistakes

**1. Sending JSON with `data=`**

`data=dict` sends form encoding, not JSON. Use `json=dict` for JSON APIs.

**2. Retrying forever**

Unlimited retries can hammer an already struggling service. Cap attempts and use backoff with jitter.

**3. Retrying POST automatically**

Could create duplicates (two orders, two servers). Retry only idempotent requests, or use idempotency keys.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Query builder:** GET `/api/servers` with `env=dev`, `per_page=1` and print the final URL path and the returned item names.
- **Task 2 (Medium) — Bulk create with validation:** POST three servers from a list where one is missing `env`. Print `created <id>` for successes and the API's validation message for the failure, then print how many were created.
- **Task 3 (Practical Challenge) — Resilient fetch:** Write `resilient_get(url, max_attempts=5)` that retries on 503 and on `requests.Timeout`, with exponential backoff (start 0.1 s), and returns the parsed JSON or raises `RuntimeError` after the last attempt. Test it against `/flaky` (succeeds) and `/status/503` with `max_attempts=3` (fails).

## 10. DevOps/MLOps Connection

- **DevOps:** GET Prometheus metrics, POST deployment events to Grafana/Datadog, POST alerts to Slack/Teams webhooks, page through GitHub API results.
- **Cloud:** AWS SDKs implement exactly this retry-with-backoff logic internally (throttling = 429-like errors).
- **MLOps:** `POST /predict` with a JSON body is how clients call a model service; batch-scoring scripts page through input records and must retry gracefully.

## 11. Interview Questions

**Q1. When should you use `json=` vs `data=` in requests?**

<details><summary>Show answer</summary>

`json=` for JSON APIs (serialises and sets Content-Type); `data=` for form-encoded bodies or raw bytes/strings.

</details>

**Q2. What is exponential backoff with jitter?**

<details><summary>Show answer</summary>

Waiting progressively longer between retries (e.g. 0.5, 1, 2, 4 s) plus randomness to avoid many clients retrying simultaneously.

</details>

**Q3. How do you implement automatic retries in requests?**

<details><summary>Show answer</summary>

Mount an `HTTPAdapter` with a `urllib3.util.Retry` configuration on a Session.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 79 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 078](../../08-api-cloud/day-078/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 080 ➡](../../08-api-cloud/day-080/README.md)
