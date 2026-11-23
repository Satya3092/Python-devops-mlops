# Day 098 — Practice Tasks: Building an ML API using FastAPI

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Pydantic model

**Problem statement:** Create a Pydantic model `Deployment` with `service` (str, min length 3), `replicas` (int 1–50) and `env` (one of dev/staging/prod using `Literal`). Validate one good and one bad payload and print the errors.

**Input requirements:** No user input required.

**Expected behavior:** One valid object and a list of validation errors.

**Expected output:**

```text
service='orders' replicas=3 env='prod'
service -> String should have at least 3 characters
replicas -> Input should be greater than or equal to 1
env -> Input should be 'dev', 'staging' or 'prod'
```

## Task 2 — Medium: Your first FastAPI app

**Problem statement:** Write a small FastAPI app with `GET /ping`, `GET /servers/{name}` (404 via `HTTPException` when unknown) and `GET /servers?env=...` (query parameter). Test all routes with `TestClient`.

**Input requirements:** No user input required.

**Expected behavior:** Responses for each route including a 404.

**Expected output:**

```text
GET  /ping            -> {'pong': True}
GET  /servers/web-01  -> {'name': 'web-01', 'env': 'prod'}
GET  /servers/nope    -> 404 {'detail': 'server nope not found'}
GET  /servers?env=dev -> ['batch-01']
```

## Task 3 — Practical Challenge: Run the test suite

**Problem statement:** Run `pytest -q test_app.py` from Python with `subprocess` and print the summary line. Then add (in your own copy) a test that `/model-info` returns the five feature names.

**Input requirements:** No user input required.

**Expected behavior:** `5 passed`.

**Expected output:**

```text
5 passed
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
