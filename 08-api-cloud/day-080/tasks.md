# Day 080 — Practice Tasks: API Authentication and Tokens

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Mask a secret

**Problem statement:** Write `mask(secret, visible=4)` that shows only the first `visible` characters followed by `****`. Use it to print an API key read from `os.environ` (set a demo value in the solution).

**Input requirements:** No user input required.

**Expected behavior:** `demo****`.

**Expected output:**

```text
demo****
```

## Task 2 — Medium: Auth header builder

**Problem statement:** Write `auth_headers(kind, value)` returning the right header dict for `api_key`, `bearer` and `basic` (value is a `(user, password)` tuple; build the base64 header yourself). Verify the basic header via the `/echo` endpoint matches what requests generates with `auth=`.

**Input requirements:** No user input required.

**Expected behavior:** Three header dicts and `match: True`.

**Expected output:**

```text
{'X-API-Key': 'k-123'}
{'Authorization': 'Bearer tok-0001'}
{'Authorization': 'Basic Ym90OnB3'}
match: True
```

## Task 3 — Practical Challenge: Secure metrics poller

**Problem statement:** Using a token client (copy the class), poll `/api/secure/metrics` 3 times with a 1-second token TTL and 0.6 s between polls, printing the CPU value each time and the number of tokens fetched. Read the client credentials from env vars and fail with a clear message if they are missing.

**Input requirements:** No user input required.

**Expected behavior:** Three CPU values, 2 tokens fetched; plus a clear error when env vars are missing.

**Expected output:**

```text
Error: set these environment variables first: ['API_CLIENT_ID', 'API_CLIENT_SECRET']
poll 1: cpu=41.5
poll 2: cpu=41.5
poll 3: cpu=41.5
Tokens fetched: 2
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
