# Day 078 — Working with APIs using Requests

[⬅ Day 077](../../08-api-cloud/day-077/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 079 ➡](../../08-api-cloud/day-079/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Install and use the `requests` library for HTTP calls
- Use params, headers, timeouts, `raise_for_status()` and `response.json()`
- Reuse connections and defaults with `requests.Session`

## 2. Topic Explanation

`requests` is the most popular Python HTTP library — "HTTP for Humans". Compared with `urllib`, it handles JSON, query parameters, sessions, redirects and errors with far less code.

```bash
pip install requests
```

```python
import requests
response = requests.get("https://api.github.com/repos/python/cpython", timeout=10)
response.raise_for_status()      # raise an exception for 4xx/5xx
data = response.json()           # parse JSON body into dicts/lists
```

The `Response` object:

| Attribute | Meaning |
|---|---|
| `.status_code` | 200, 404, ... |
| `.ok` | True for status < 400 |
| `.json()` | parsed JSON body |
| `.text` / `.content` | body as str / bytes |
| `.headers` | case-insensitive dict |
| `.elapsed` | how long the request took |
| `.url` | final URL (after params/redirects) |

Rules for production code:
1. **Always set `timeout=`** — requests waits forever by default!
2. Call `raise_for_status()` (or check `status_code`).
3. Catch `requests.exceptions.RequestException` (base of `ConnectionError`, `Timeout`, `HTTPError`).
4. Use a `Session` for many calls to the same API: it keeps TCP connections open (faster) and shares headers/auth.

Public practice APIs you can try at home: `https://api.github.com`, `https://jsonplaceholder.typicode.com`, `https://httpbin.org`.

> These examples use [`mock_api.py`](mock_api.py), a tiny local REST API included in this folder, so everything works offline and gives the same results every time. Install requests first: `pip install requests`.

## 3. Syntax

```python
import requests
r = requests.get(url, params={"k": "v"}, headers={"Accept": "application/json"}, timeout=5)
r.raise_for_status()
data = r.json()

with requests.Session() as s:
    s.headers.update({"User-Agent": "my-tool/1.0"})
    s.get(url, timeout=5)
```

| Part | Meaning |
|---|---|
| `params=` | Dict converted into a safely-encoded query string. |
| `headers=` | Extra request headers. |
| `timeout=` | Seconds to wait (connect + read). Always set it. |
| `raise_for_status()` | Raises `HTTPError` for 4xx/5xx. |
| `Session` | Connection pooling + shared settings. |

## 4. Example 1 — Basic Example: First requests

```python
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
```

## 5. Example 2 — Practical Example: A reusable API client class with a Session

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `requests.get(..., timeout=5)` returns a `Response`; `.json()` parses the body.
- `params=` builds `?env=prod&per_page=5` for you (`response.url` shows the final URL).
- A 404 does **not** raise automatically — `raise_for_status()` turns it into an `HTTPError` whose `.response` you can inspect.

**Example 2**
- `InventoryClient` hides HTTP details behind meaningful methods (`servers()`, `server(id)`): the rest of your automation never deals with URLs or status codes.
- A `Session` reuses connections and sends the same headers with every request.
- `server()` converts "404" into `None` but re-raises other HTTP errors (`raise` keeps the original exception).
- `ConnectionError` (nobody listening) and `Timeout` (too slow) are network problems, separate from HTTP status errors.

## 7. Expected Output

**Example 1:**

```text
Status: 200 | ok: True
Content-Type: application/json
JSON: {'status': 'ok', 'version': '1.0.0'}
Final URL path: /api/servers?env=prod&per_page=5
  1 web-01   running
  2 web-02   running
Missing server: 404 {'error': 'server 99 not found'}
raise_for_status -> HTTPError 404
```

**Example 2:**

```text
API health: ok
Prod servers: ['web-01', 'web-02']
Server 3: {'id': 3, 'name': 'batch-01', 'env': 'dev', 'cpu': 8, 'status': 'stopped'}
Server 42: None
ConnectionError: nothing is listening on that port
Timeout: the API took longer than 0.5 s
```

## 8. Common Mistakes

**1. No timeout**

`requests.get(url)` can hang forever and freeze your cron job. Always pass `timeout=`.

**2. Calling `.json()` on non-JSON**

An HTML error page raises a JSON decode error. Check `status_code`/`content-type` first.

**3. `verify=False`**

Disables certificate checks and invites man-in-the-middle attacks. Point `verify=` at the right CA bundle instead.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Health checker:** Write `is_healthy(base_url)` that returns True only if `/health` answers 200 with `{"status": "ok"}` within 2 seconds, and False for any exception. Test it on the mock API and on `http://127.0.0.1:9`.
- **Task 2 (Medium) — Server summary:** Fetch all servers and print the count per environment and the total CPU of running servers.
- **Task 3 (Practical Challenge) — Extend the client:** Add `create_server(name, env, cpu=2)` and `delete_server(id)` methods to a copy of `InventoryClient` (using `session.post(json=...)` and `session.delete`). Create a server, read it back, delete it, and confirm `server(id)` returns None afterwards.

## 10. DevOps/MLOps Connection

- **DevOps:** trigger Jenkins jobs, create GitHub releases, post Slack messages, query Prometheus (`/api/v1/query`), manage Grafana dashboards — all with `requests`.
- **Cloud:** call cloud provider REST endpoints directly when no SDK exists; check public endpoints after deployment (smoke tests).
- **MLOps:** test model APIs, call feature stores and model registries, and run load tests against prediction endpoints.

## 11. Interview Questions

**Q1. Why should you always set a timeout in requests?**

<details><summary>Show answer</summary>

By default requests waits indefinitely; a stalled server would hang the script/worker forever.

</details>

**Q2. What is the advantage of `requests.Session`?**

<details><summary>Show answer</summary>

Connection pooling (keep-alive), shared headers/auth/cookies and configuration across requests.

</details>

**Q3. Does requests raise an exception for a 404?**

<details><summary>Show answer</summary>

No. Only network errors raise automatically; call `raise_for_status()` to raise for 4xx/5xx.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 78 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 077](../../08-api-cloud/day-077/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 079 ➡](../../08-api-cloud/day-079/README.md)
