# Day 079 — Practice Tasks: GET and POST Requests

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Query builder

**Problem statement:** GET `/api/servers` with `env=dev`, `per_page=1` and print the final URL path and the returned item names.

**Input requirements:** No user input required.

**Expected behavior:** Path with both parameters and `['batch-01']`.

**Expected output:**

```text
/api/servers?env=dev&per_page=1
['batch-01']
```

## Task 2 — Medium: Bulk create with validation

**Problem statement:** POST three servers from a list where one is missing `env`. Print `created <id>` for successes and the API's validation message for the failure, then print how many were created.

**Input requirements:** No user input required.

**Expected behavior:** Two created, one 422 message.

**Expected output:**

```text
created 4
failed orphan: 422 {'error': 'missing fields', 'fields': ['env']}
created 5
Created: 2
```

## Task 3 — Practical Challenge: Resilient fetch

**Problem statement:** Write `resilient_get(url, max_attempts=5)` that retries on 503 and on `requests.Timeout`, with exponential backoff (start 0.1 s), and returns the parsed JSON or raises `RuntimeError` after the last attempt. Test it against `/flaky` (succeeds) and `/status/503` with `max_attempts=3` (fails).

**Input requirements:** No user input required.

**Expected behavior:** Success after retries, then a RuntimeError message.

**Expected output:**

```text
  attempt 1 failed (503)
  attempt 2 failed (503)
  success on attempt 3
{'status': 'ok', 'attempt': 3}
  attempt 1 failed (503)
  attempt 2 failed (503)
  attempt 3 failed (503)
RuntimeError: gave up after 3 attempts: /status/503
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
