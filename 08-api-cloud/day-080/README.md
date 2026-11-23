# Day 080 — API Authentication and Tokens

[⬅ Day 079](../../08-api-cloud/day-079/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 081 ➡](../../08-api-cloud/day-081/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 8 — API, Cloud and DevOps Integration | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use API keys, Basic auth and Bearer tokens correctly
- Load credentials from environment variables, never from source code
- Obtain, cache and refresh access tokens automatically

## 2. Topic Explanation

Most APIs need to know **who** is calling (authentication) and **what** they may do (authorisation).

| Method | How it's sent | Typical use |
|---|---|---|
| **API key** | header like `X-API-Key: <key>` | SaaS APIs, internal services |
| **Basic auth** | `Authorization: Basic base64(user:password)` | Jenkins, registries, simple tools — HTTPS only! |
| **Bearer token** | `Authorization: Bearer <token>` | OAuth2, GitHub PATs, Kubernetes service accounts |
| **Signed requests** | signature computed from secret key | AWS SigV4 (boto3 does it for you) |

**Token flow (OAuth2 client-credentials style):**
1. Send `client_id` + `client_secret` to a token endpoint.
2. Receive an `access_token` with an `expires_in` lifetime.
3. Send `Authorization: Bearer <token>` on each request.
4. On expiry (or a 401), get a new token and retry once.

**Secret hygiene — non-negotiable:**
- Never hard-code secrets or commit them to Git (`git log` remembers forever). Use environment variables, CI secret stores, Vault or AWS Secrets Manager.
- Never print or log tokens. Mask them (`tok-****`).
- Use least-privilege, short-lived tokens; rotate them.
- Basic auth and tokens are only safe over **HTTPS**.

`base64` is an **encoding**, not encryption — anyone can decode a Basic auth header.

> These examples use [`mock_api.py`](mock_api.py), a tiny local REST API included in this folder, so everything works offline and gives the same results every time. Install requests first: `pip install requests`. The credentials used (`demo-client`, `demo-secret`, `demo-api-key`) are fake values that only work with the local mock API.

## 3. Syntax

```python
import os, requests
api_key = os.environ["API_KEY"]                      # never hard-code
requests.get(url, headers={"X-API-Key": api_key}, timeout=5)
requests.get(url, auth=("user", os.environ["PASSWORD"]), timeout=5)       # Basic
requests.get(url, headers={"Authorization": f"Bearer {token}"}, timeout=5)
```

| Part | Meaning |
|---|---|
| `os.environ[...]` | Read secrets from the environment. |
| `X-API-Key header` | Typical API-key placement (name varies per API). |
| `auth=(user, pw)` | requests builds the Basic auth header. |
| `Bearer token` | `Authorization: Bearer <token>`. |

## 4. Example 1 — Basic Example: API keys from the environment and what Basic auth really sends

```python
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
```

## 5. Example 2 — Practical Example: A token-aware client that refreshes automatically

```python
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
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- The API key comes from an environment variable; we print only a masked version.
- Wrong key → **403**.
- `auth=("user", "password")` makes requests send a Basic auth header. Decoding it with `base64` shows the password in clear text — Basic auth is only acceptable over HTTPS.

**Example 2**
- Without a token the API answers **401** with `WWW-Authenticate: Bearer`.
- `TokenClient` fetches a token using client credentials from the environment, caches it, and fetches a new one when it expires (`time.time() >= self._expires_at`).
- If the API still says 401 (e.g. token revoked), it refreshes and **retries once** — never loop forever on auth errors.
- Wrong client credentials → **401** from the token endpoint, surfaced as an `HTTPError`.

## 7. Expected Output

**Example 1:**

```text
Using key: demo********
With key   : 200 {'report': 'daily-costs', 'total_usd': 123.45}
Wrong key  : 403 {'error': 'invalid API key'}
Basic header sent: Basic amVua2lucy1ib3Q6czNjcjN0
Decoded (anyone can do this!): jenkins-bot:s3cr3t
```

**Example 2:**

```text
No token      : 401 {'error': 'missing or invalid token'} | WWW-Authenticate: Bearer
  (fetched token tok-****, valid 1s)
Call 1: {'cpu': 41.5, 'memory': 63.2, 'requests_per_minute': 1280}
Call 2: {'cpu': 41.5, 'memory': 63.2, 'requests_per_minute': 1280}
  (fetched token tok-****, valid 1s)
Call 3: {'cpu': 41.5, 'memory': 63.2, 'requests_per_minute': 1280}
Tokens fetched: 2
Bad credentials -> 401 {'error': 'invalid client credentials'}
```

## 8. Common Mistakes

**1. Committing secrets**

Hard-coded keys leak through Git history, forks and logs. Use env vars/secret stores and scanners like gitleaks in CI.

**2. Logging Authorization headers**

Debug logs that dump headers leak tokens. Mask or drop sensitive headers before logging.

**3. Fetching a new token for every request**

Slow and may hit rate limits. Cache tokens until shortly before expiry.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Mask a secret:** Write `mask(secret, visible=4)` that shows only the first `visible` characters followed by `****`. Use it to print an API key read from `os.environ` (set a demo value in the solution).
- **Task 2 (Medium) — Auth header builder:** Write `auth_headers(kind, value)` returning the right header dict for `api_key`, `bearer` and `basic` (value is a `(user, password)` tuple; build the base64 header yourself). Verify the basic header via the `/echo` endpoint matches what requests generates with `auth=`.
- **Task 3 (Practical Challenge) — Secure metrics poller:** Using a token client (copy the class), poll `/api/secure/metrics` 3 times with a 1-second token TTL and 0.6 s between polls, printing the CPU value each time and the number of tokens fetched. Read the client credentials from env vars and fail with a clear message if they are missing.

## 10. DevOps/MLOps Connection

- **DevOps:** GitHub/GitLab tokens in CI, Jenkins API tokens, Docker registry credentials, Vault tokens, Kubernetes service-account tokens — same patterns.
- **Cloud:** prefer **IAM roles** (EC2 instance profiles, IRSA on EKS, GitHub OIDC) over long-lived access keys; boto3 picks them up automatically (Day 82).
- **MLOps:** model APIs must be authenticated (API gateway keys, OAuth); training jobs read data-store credentials from secrets, never from notebooks.

## 11. Interview Questions

**Q1. Is Basic authentication secure?**

<details><summary>Show answer</summary>

Only over HTTPS: the credentials are just base64-encoded, which anyone can decode.

</details>

**Q2. Where should API secrets be stored for a CI pipeline?**

<details><summary>Show answer</summary>

In the CI system's encrypted secret store or a secret manager (Vault, AWS Secrets Manager), injected as environment variables at runtime — never in the repo.

</details>

**Q3. How should a client handle an expired access token?**

<details><summary>Show answer</summary>

Refresh it before expiry (cache with expiry time) and, on a 401, refresh once and retry the request once.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 80 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 079](../../08-api-cloud/day-079/README.md) | [📚 Phase 8: API, Cloud and DevOps Integration](../README.md) | [🏠 Home](../../README.md) | [Day 081 ➡](../../08-api-cloud/day-081/README.md)
