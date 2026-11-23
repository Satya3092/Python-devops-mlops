# Day 077 — REST API Concepts

[⬅ Day 076](../../08-api-cloud/day-076/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 078 ➡](../../08-api-cloud/day-078/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain REST resources, endpoints and how HTTP methods map to CRUD
- Understand idempotency, statelessness, pagination and versioning
- Perform CRUD operations against a REST API using only the standard library

## 2. Topic Explanation

**REST** (REpresentational State Transfer) is a style for designing web APIs around **resources** (nouns) addressed by URLs, manipulated with standard HTTP methods (verbs).

| Action (CRUD) | Method | Endpoint | Success code |
|---|---|---|---|
| List | GET | `/api/servers` | 200 |
| Read one | GET | `/api/servers/42` | 200 (404 if missing) |
| Create | POST | `/api/servers` | 201 + `Location` |
| Replace / update | PUT / PATCH | `/api/servers/42` | 200 |
| Delete | DELETE | `/api/servers/42` | 204 |

Key principles:
- **Resources, not actions:** `POST /api/servers` — not `/api/createServer`.
- **Stateless:** every request carries everything needed (including auth). The server doesn't remember previous requests → easy horizontal scaling.
- **Idempotency:** doing the request twice has the same effect as once. GET, PUT and DELETE are idempotent; POST usually is **not** (two POSTs = two servers). Only blindly retry idempotent requests.
- **Representations:** usually JSON, announced by `Content-Type`.
- **Filtering & pagination:** `GET /api/servers?env=prod&page=2&per_page=50`.
- **Versioning:** `/v1/...` so old clients keep working.

You already use REST APIs daily: `kubectl get pods` = `GET /api/v1/namespaces/default/pods`, `kubectl delete` = `DELETE`, GitHub's API, Docker Engine API, Jenkins API.

> These examples use [`mock_api.py`](mock_api.py), a tiny local REST API included in this folder, so everything works offline and gives the same results every time. Today uses `urllib.request` from the standard library.

## 3. Syntax

```text
GET    /api/servers            list
GET    /api/servers/{id}       read
POST   /api/servers            create   (body: JSON)
PUT    /api/servers/{id}       update   (body: JSON)
DELETE /api/servers/{id}       delete
```

| Part | Meaning |
|---|---|
| `/api/servers` | Collection resource. |
| `/api/servers/{id}` | Single item resource. |
| `GET / PUT / DELETE` | Idempotent methods — safe to retry. |
| `POST` | Not idempotent — creates a new item each time. |

## 4. Example 1 — Basic Example: A tiny REST client with urllib

```python
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
```

## 5. Example 2 — Practical Example: Full CRUD lifecycle and idempotency

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `urllib.request.Request` builds a request with any method, a JSON body and headers.
- `urlopen` raises `HTTPError` for 4xx/5xx; we catch it and still return the status and error body — so callers always get `(status, data)`.
- Reading a missing item returns **404** with an error message.

**Example 2**
- **Create** returns **201** and the new resource including its server-assigned `id`.
- **Update** with PUT twice → same result: PUT is idempotent.
- Two identical **POSTs** create two different ids — that's why automation must not blindly retry POSTs.
- A body missing required fields gets **422 Unprocessable Entity** (validation error).
- **Delete** returns **204 No Content**; deleting again returns 404, but the *state* is the same (the server is gone).
- `per_page` / `page` query parameters implement pagination.

## 7. Expected Output

**Example 1:**

```text
LIST   (200, {'items': [{'id': 1, 'name': 'web-01', 'env': 'prod', 'cpu': 4, 'status': 'running'}, {'id': 2, 'name': 'web-02', 'env': 'prod', 'cpu': 4, 'status': 'running'}, {'id': 3, 'name': 'batch-01', 'env': 'dev', 'cpu': 8, 'status': 'stopped'}], 'page': 1, 'per_page': 10, 'total': 3})
READ   (200, {'id': 1, 'name': 'web-01', 'env': 'prod', 'cpu': 4, 'status': 'running'})
MISS   (404, {'error': 'server 99 not found'})
```

**Example 2:**

```text
CREATE  201  {'id': 4, 'name': 'api-03', 'env': 'staging', 'cpu': 2, 'status': 'provisioning'}
UPDATE  200  {'id': 4, 'name': 'api-03', 'env': 'staging', 'cpu': 4, 'status': 'running'}
UPDATE  200  same result? True
Two POSTs created ids: [5, 6]
INVALID (422, {'error': 'missing fields', 'fields': ['env']})
DELETE  (204, None)
DELETE again (idempotent outcome: it's gone): 404
PAGE 1 of 5 servers -> ['web-01', 'web-02']
```

## 8. Common Mistakes

**1. Verbs in URLs**

`/api/deleteServer?id=3` isn't RESTful. Use `DELETE /api/servers/3`.

**2. Retrying POST blindly**

A timeout doesn't prove the POST failed. Retrying can create duplicates. Use idempotency keys or check before retrying.

**3. Ignoring pagination**

Many APIs return only the first page (e.g. 100 items). Loop until there are no more pages.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Map CRUD to HTTP:** Print a table mapping these operations on a Kubernetes `deployments` resource to method + path: list, get `api`, create, update `api`, delete `api` (namespace `prod`, base `/apis/apps/v1/namespaces/prod/deployments`).
- **Task 2 (Medium) — Filter via query params:** Using the mock API and `urllib`, list servers with `env=prod` and then `env=dev`, printing names and the `total` field.
- **Task 3 (Practical Challenge) — Paginate everything:** Create 5 extra servers via POST, then write `get_all(per_page=2)` that keeps requesting pages until all items (according to `total`) are collected. Print how many requests were needed and all names.

## 10. DevOps/MLOps Connection

- **DevOps:** Kubernetes, Docker Engine, Jenkins, GitHub/GitLab, Grafana, PagerDuty and Vault are all REST APIs you can automate from Python.
- **Cloud:** AWS APIs follow similar ideas (idempotency tokens like `ClientToken` in EC2 exist precisely to make POST-like calls safe to retry).
- **MLOps:** model registries and serving endpoints (`POST /predict`) are REST APIs; MLflow's tracking server is a REST API.

## 11. Interview Questions

**Q1. Which HTTP methods are idempotent?**

<details><summary>Show answer</summary>

GET, HEAD, PUT, DELETE and OPTIONS are idempotent; POST is not (PATCH may or may not be).

</details>

**Q2. What does 'stateless' mean in REST?**

<details><summary>Show answer</summary>

Each request contains all the information needed; the server stores no client session state between requests.

</details>

**Q3. How would you design an endpoint to restart a server?**

<details><summary>Show answer</summary>

Model it as a resource action, e.g. `POST /api/servers/42/restarts` (creating a restart operation), returning 202 Accepted with a status URL.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 77 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 076](../../08-api-cloud/day-076/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 078 ➡](../../08-api-cloud/day-078/README.md)
