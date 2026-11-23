# Day 042 — Practice Tasks: Variable-Length Arguments (**kwargs)

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Print settings

**Problem statement:** Write `print_settings(**settings)` that prints each setting sorted by key as `KEY = value` (key in upper case).

**Input requirements:** No user input required.

**Expected behavior:** Sorted upper-case keys.

**Expected output:**

```text
DEBUG = False
LOG_LEVEL = INFO
TIMEOUT = 30
```

## Task 2 — Medium: Build a connection string

**Problem statement:** Write `connection_string(driver, **params)` that returns `driver://user:password@host:port/db` using values from `params` with defaults host=localhost, port=5432. Call it by unpacking a dict.

**Input requirements:** No user input required.

**Expected behavior:** `postgresql://app:secret@db.internal:5432/orders`.

**Expected output:**

```text
postgresql://app:secret@db.internal:5432/orders
```

## Task 3 — Practical Challenge: Kubernetes label selector

**Problem statement:** Write `kubectl_get(resource, *names, namespace="default", **labels)`. It returns a kubectl command with names and a `-l key=value,key2=value2` selector when labels are given. Test 3 different calls.

**Input requirements:** No user input required.

**Expected behavior:** Three kubectl commands.

**Expected output:**

```text
kubectl get pods -n default
kubectl get pods -n prod -l app=orders,tier=backend
kubectl get deployment api worker -n jobs
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
