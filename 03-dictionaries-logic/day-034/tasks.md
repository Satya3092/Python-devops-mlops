# Day 034 — Practice Tasks: List Comprehension

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Uppercase names

**Problem statement:** Convert `["asha", "ravi", "meera"]` to title case with a list comprehension, and make a list of name lengths.

**Input requirements:** No user input required.

**Expected behavior:** `['Asha', 'Ravi', 'Meera']` and `[4, 4, 5]`.

**Expected output:**

```text
['Asha', 'Ravi', 'Meera']
[4, 4, 5]
```

## Task 2 — Medium: Filter log levels

**Problem statement:** From `logs = ["INFO ok", "ERROR db", "WARNING cpu", "ERROR disk", "INFO done"]`, build a list of error messages only (without the `ERROR ` prefix), and a dict comprehension counting each level.

**Input requirements:** No user input required.

**Expected behavior:** `['db', 'disk']` and `{'INFO': 2, 'ERROR': 2, 'WARNING': 1}`.

**Expected output:**

```text
['db', 'disk']
{'INFO': 2, 'ERROR': 2, 'WARNING': 1}
```

## Task 3 — Practical Challenge: Kubernetes resource summary

**Problem statement:** Given pods `[{"name": "api-1", "cpu_m": 250, "ready": True}, {"name": "api-2", "cpu_m": 250, "ready": False}, {"name": "worker-1", "cpu_m": 500, "ready": True}, {"name": "cron-1", "cpu_m": 100, "ready": True}]`, use comprehensions to get: names of not-ready pods, total CPU of ready pods in cores, a dict name → CPU in cores, and the set of app prefixes (text before `-`).

**Input requirements:** No user input required.

**Expected behavior:** `['api-2']`, `0.85` cores, the mapping and `['api', 'cron', 'worker']`.

**Expected output:**

```text
Not ready: ['api-2']
Ready CPU (cores): 0.85
CPU map: {'api-1': 0.25, 'api-2': 0.25, 'worker-1': 0.5, 'cron-1': 0.1}
Apps: ['api', 'cron', 'worker']
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
