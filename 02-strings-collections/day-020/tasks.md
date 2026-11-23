# Day 020 — Practice Tasks: String Formatting (f-strings)

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Introduce a service

**Problem statement:** With `service = "orders"`, `replicas = 3`, `version = "2.1.0"`, print `orders v2.1.0 running with 3 replicas` using one f-string.

**Input requirements:** No user input required.

**Expected behavior:** Exactly that sentence.

**Expected output:**

```text
orders v2.1.0 running with 3 replicas
```

## Task 2 — Medium: Format metrics

**Problem statement:** Print `request_count = 1532874` with separators, `latency = 0.234567` seconds as milliseconds with 1 decimal, and `success_ratio = 0.98765` as a percentage with 2 decimals.

**Input requirements:** No user input required.

**Expected behavior:** Prints `1,532,874`, `234.6 ms`, `98.77%`.

**Expected output:**

```text
Requests: 1,532,874
Latency: 234.6 ms
Success: 98.77%
```

## Task 3 — Practical Challenge: Pod status table

**Problem statement:** Given a list of pods `[("api-7d9f", "Running", 0, 12.3), ("worker-5c2a", "CrashLoopBackOff", 14, 0.0), ("redis-0", "Running", 1, 3.75)]` (name, status, restarts, age in hours), print an aligned table like `kubectl get pods` with columns NAME, STATUS, RESTARTS, AGE (age with 1 decimal + `h`).

**Input requirements:** No user input required.

**Expected behavior:** A header and three aligned rows.

**Expected output:**

```text
NAME          STATUS              RESTARTS     AGE
api-7d9f      Running                    0   12.3h
worker-5c2a   CrashLoopBackOff          14    0.0h
redis-0       Running                    1    3.8h
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
