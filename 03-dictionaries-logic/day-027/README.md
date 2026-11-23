# Day 027 — Dictionary Methods

[⬅ Day 026](../../03-dictionaries-logic/day-026/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 028 ➡](../../03-dictionaries-logic/day-028/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Loop through dicts with `keys()`, `values()` and `items()`
- Use `update`, `pop`, `setdefault`, `copy`, `clear`
- Count things with a dictionary

## 2. Topic Explanation

Key dictionary methods:

| Method | Does |
|---|---|
| `keys()` | View of all keys |
| `values()` | View of all values |
| `items()` | View of `(key, value)` pairs — the most used in loops |
| `get(k, default)` | Safe read |
| `update(other)` | Merge another dict in (overwrites duplicates) |
| `pop(k, default)` | Remove a key and return its value |
| `setdefault(k, default)` | Return value; if key missing, insert default first |
| `copy()` | Shallow copy |
| `clear()` | Remove all items |

Python 3.9+ also supports merging with `|`: `merged = defaults | overrides`.

**Counting pattern** (super common when analysing logs):
```python
counts = {}
for level in levels:
    counts[level] = counts.get(level, 0) + 1
```

## 3. Syntax

```python
for key, value in my_dict.items():
    ...
my_dict.update({"k": v})
value = my_dict.pop("k", None)
merged = dict_a | dict_b
counts[k] = counts.get(k, 0) + 1
```

| Part | Meaning |
|---|---|
| `items()` | Yields `(key, value)` tuples for unpacking in a loop. |
| `update()` | Adds/overwrites keys from another dict. |
| `pop(k, default)` | Removes key and returns its value (default if missing). |
| `a \| b` | New dict; keys from `b` win on conflict (3.9+). |

## 4. Example 1 — Basic Example: Looping and modifying

```python
ports = {"ssh": 22, "http": 80, "https": 443}

print("Keys:", list(ports.keys()))
print("Values:", list(ports.values()))
for service, port in ports.items():
    print(f"  {service:<6} -> {port}")

ports.update({"postgres": 5432, "http": 8080})
print("After update:", ports)

removed = ports.pop("ssh")
print("Removed ssh port:", removed)

ports.setdefault("redis", 6379)
print("After setdefault:", ports)

defaults = {"timeout": 30, "retries": 3}
custom = {"retries": 5}
print("Merged with |:", defaults | custom)
```

## 5. Example 2 — Practical Example: Counting log levels and grouping by host

```python
log_lines = [
    "web-01 INFO Request served",
    "web-02 ERROR Connection refused",
    "web-01 WARNING Slow response",
    "web-03 INFO Request served",
    "web-02 ERROR Timeout",
    "web-01 INFO Health check ok",
    "web-02 INFO Request served",
]

level_counts = {}
errors_by_host = {}
for line in log_lines:
    host, level, message = line.split(" ", 2)
    level_counts[level] = level_counts.get(level, 0) + 1
    if level == "ERROR":
        errors_by_host.setdefault(host, []).append(message)

print("Log level counts:")
for level, count in level_counts.items():
    print(f"  {level:<8}{count}")

print("Errors grouped by host:")
for host, messages in errors_by_host.items():
    print(f"  {host}: {messages}")

most_common = max(level_counts, key=level_counts.get)
print("Most common level:", most_common)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `items()` gives pairs so we can unpack `service, port` in the loop.
- `update` overwrote `http` and added `postgres`.
- `pop("ssh")` removed the key and returned 22.
- `setdefault` added `redis` because it was missing.
- `defaults | custom` creates a merged copy where `custom` wins.

**Example 2**
- `split(" ", 2)` splits only twice so the message keeps its spaces.
- `level_counts.get(level, 0) + 1` is the counting pattern.
- `setdefault(host, [])` returns the existing list or creates an empty one, then `.append` adds the message — a grouping pattern.
- `max(level_counts, key=level_counts.get)` finds the key with the largest value.

## 7. Expected Output

**Example 1:**

```text
Keys: ['ssh', 'http', 'https']
Values: [22, 80, 443]
  ssh    -> 22
  http   -> 80
  https  -> 443
After update: {'ssh': 22, 'http': 8080, 'https': 443, 'postgres': 5432}
Removed ssh port: 22
After setdefault: {'http': 8080, 'https': 443, 'postgres': 5432, 'redis': 6379}
Merged with |: {'timeout': 30, 'retries': 5}
```

**Example 2:**

```text
Log level counts:
  INFO    4
  ERROR   2
  WARNING 1
Errors grouped by host:
  web-02: ['Connection refused', 'Timeout']
Most common level: INFO
```

## 8. Common Mistakes

**1. Changing dict size while looping**

Deleting keys inside `for k in d:` raises `RuntimeError`. Loop over `list(d)` instead.

**2. Forgetting `.items()`**

`for k, v in d:` fails — iterating a dict gives keys only.

**3. Shallow copy surprises**

`d.copy()` does not copy nested dicts/lists. Use `copy.deepcopy(d)` for nested data.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Print a dictionary nicely:** Given `capitals = {"India": "New Delhi", "Japan": "Tokyo", "France": "Paris"}`, print each pair as `Country: Capital` and then all capitals in alphabetical order.
- **Task 2 (Medium) — Word frequency:** Count how many times each word appears in `"deploy test deploy build test deploy"` and print words with counts, most frequent first.
- **Task 3 (Practical Challenge) — HTTP status report:** Given status codes from an access log `[200, 200, 404, 500, 200, 301, 404, 200, 503, 200]`, count each code, then group counts by class (2xx, 3xx, 4xx, 5xx) into another dict. Print both and the error percentage (4xx + 5xx).

## 10. DevOps/MLOps Connection

- **DevOps / Monitoring:** counting log levels, status codes, errors per host — the core of every log-analysis script (Project 3).
- **Cloud:** grouping EC2 instances by tag or state; merging tag dicts.
- **Data engineering:** "group by" in plain Python before you learn Pandas `groupby` (Day 89).
- **ML:** counting class labels to detect imbalanced datasets.

## 11. Interview Questions

**Q1. What does `dict.items()` return?**

<details><summary>Show answer</summary>

A view of `(key, value)` tuples, which reflects later changes to the dict.

</details>

**Q2. How do you merge two dictionaries?**

<details><summary>Show answer</summary>

`a | b` (3.9+), `{**a, **b}`, or `a.update(b)` in place.

</details>

**Q3. What does `setdefault` do?**

<details><summary>Show answer</summary>

Returns the value for a key; if the key is missing it inserts the default value first and returns it.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 27 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 026](../../03-dictionaries-logic/day-026/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 028 ➡](../../03-dictionaries-logic/day-028/README.md)
