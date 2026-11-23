# Day 003 — Practice Tasks: Python Data Types

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Type detective

**Problem statement:** Create one variable of each type: int, float, str, bool, list, tuple, set, dict, None. Print each value with its type name.

**Input requirements:** No user input required.

**Expected behavior:** Nine lines like `8080 -> int`.

**Expected output:**

```text
8080 -> int
99.9 -> float
nginx -> str
True -> bool
['a', 'b'] -> list
(1, 2) -> tuple
{'y', 'x'} -> set
{'k': 'v'} -> dict
None -> NoneType
```

## Task 2 — Medium: Pick the right type

**Problem statement:** For each piece of Kubernetes pod data choose the best type and store it: pod name, replica count, CPU limit in cores (0.5), is ready, container ports 80 and 443 (fixed), labels (app=web, tier=frontend). Print each with its type.

**Input requirements:** No user input required.

**Expected behavior:** Name → str, replicas → int, cpu → float, ready → bool, ports → tuple, labels → dict.

**Expected output:**

```text
web-7d9f8 -> str
3 -> int
0.5 -> float
True -> bool
(80, 443) -> tuple
{'app': 'web', 'tier': 'frontend'} -> dict
```

## Task 3 — Practical Challenge: Type validation

**Problem statement:** Given `config = {"port": "8080", "debug": True, "workers": 4, "timeout": 2.5}`, check with `isinstance` whether `port` and `workers` are integers and print which settings are invalid.

**Input requirements:** No user input required.

**Expected behavior:** Reports that `port` is a `str` and should be an `int`.

**Expected output:**

```text
port is INVALID: got str but expected int
workers is valid (int)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
