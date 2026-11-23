# Day 076 — Practice Tasks: HTTP and HTTPS Fundamentals

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: URL inspector

**Problem statement:** Write `describe_url(url)` that prints scheme, host, port (default 443 for https / 80 for http when missing), path and query dict. Test it on two URLs.

**Input requirements:** No user input required.

**Expected behavior:** Two descriptions with default ports filled in.

**Expected output:**

```text
https | registry.example.com | 443 | /v2/orders/tags/list | {'n': ['5']}
http | 10.0.0.5 | 9100 | /metrics | {}
```

## Task 2 — Medium: Status classifier

**Problem statement:** Write `classify_status(code)` returning `success`, `redirect`, `client error`, `server error` or `informational`, plus `retry` advice for 429/502/503/504. Print a table for 200, 204, 302, 404, 429, 500, 503.

**Input requirements:** No user input required.

**Expected behavior:** Seven classified codes, retry advice for 429 and 503.

**Expected output:**

```text
200 success
204 success
302 redirect
404 client error
429 client error (retry later)
500 server error
503 server error (retry later)
```

## Task 3 — Practical Challenge: Raw client

**Problem statement:** Using `http.client` and the mock API, GET `/api/servers?env=prod` and print each server name, then GET `/status/503` and print the status and reason. Close the connection at the end.

**Input requirements:** No user input required.

**Expected behavior:** `web-01`, `web-02` and `503 Service Unavailable`.

**Expected output:**

```text
web-01
web-02
503 Service Unavailable
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
