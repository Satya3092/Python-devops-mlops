# Day 072 — Practice Tasks: Regular Expressions

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Find all hashtags

**Problem statement:** Extract all hashtags from `"Learning #Python for #DevOps and #MLOps #100DaysOfCode"`.

**Input requirements:** No user input required.

**Expected behavior:** `['#Python', '#DevOps', '#MLOps', '#100DaysOfCode']`.

**Expected output:**

```text
['#Python', '#DevOps', '#MLOps', '#100DaysOfCode']
```

## Task 2 — Medium: Validate hostnames

**Problem statement:** Write `is_valid_hostname(name)` that accepts lowercase names like `web-01` or `db-prod-3` (letters, digits, hyphens, 3–20 chars, not starting/ending with a hyphen). Test 5 names.

**Input requirements:** No user input required.

**Expected behavior:** True/False for each name.

**Expected output:**

```text
web-01     True
db-prod-3  True
-bad       False
UPPER      False
ab         False
```

## Task 3 — Practical Challenge: Kubernetes event parser

**Problem statement:** Parse these event lines with one compiled regex into dicts (age, type, reason, object, message): `5m Warning BackOff pod/api-7d9f Back-off restarting failed container`, `2m Normal Pulled pod/api-7d9f Successfully pulled image`, `30s Warning FailedScheduling pod/worker-1 0/3 nodes are available`. Print only Warning events and count reasons.

**Input requirements:** No user input required.

**Expected behavior:** Two warning events and reason counts.

**Expected output:**

```text
{'age': '5m', 'type': 'Warning', 'reason': 'BackOff', 'object': 'pod/api-7d9f', 'message': 'Back-off restarting failed container'}
{'age': '30s', 'type': 'Warning', 'reason': 'FailedScheduling', 'object': 'pod/worker-1', 'message': '0/3 nodes are available'}
{'BackOff': 1, 'Pulled': 1, 'FailedScheduling': 1}
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
