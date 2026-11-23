# Day 044 — Lambda Functions

[⬅ Day 043](../../04-functions/day-043/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 045 ➡](../../04-functions/day-045/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Write small anonymous functions with `lambda`
- Use lambdas as `key` functions for `sorted`, `min`, `max`
- Use `map()` and `filter()` and know when a comprehension is clearer

## 2. Topic Explanation

A **lambda** is a tiny, unnamed function written in one expression:

```python
square = lambda n: n * n
square(4)   # 16
```

It is equivalent to:
```python
def square(n):
    return n * n
```

Rules: a lambda can have any number of parameters but only **one expression** (no statements, no loops, no assignments). The expression's value is returned automatically.

Where lambdas shine — as **throw-away helper functions** passed to other functions:
- `sorted(servers, key=lambda s: s["cpu"])` — sort by a field.
- `max(pods, key=lambda p: p["restarts"])` — find the pod with most restarts.
- `filter(lambda x: x > 0, numbers)` and `map(lambda x: x * 2, numbers)`.

PEP 8 tip: don't assign lambdas to names for real code (`square = lambda ...`); use `def`. Lambdas are for inline use.

## 3. Syntax

```python
lambda parameters: expression

sorted(items, key=lambda item: item["field"])
list(map(lambda x: x * 2, numbers))
list(filter(lambda x: x > 0, numbers))
```

| Part | Meaning |
|---|---|
| `lambda` | Keyword that creates an anonymous function. |
| `parameters` | Zero or more, comma-separated. |
| `expression` | Single expression whose value is returned. |
| `key=` | Function used to compute the sort/compare value. |

## 4. Example 1 — Basic Example: Lambda basics

```python
add = lambda a, b: a + b            # for demonstration only
print(add(2, 3))

numbers = [5, -3, 12, 0, -8, 7]
print("Doubled:", list(map(lambda n: n * 2, numbers)))
print("Positive:", list(filter(lambda n: n > 0, numbers)))
print("By absolute value:", sorted(numbers, key=lambda n: abs(n)))

# The same with comprehensions (often more readable)
print("Doubled:", [n * 2 for n in numbers])
print("Positive:", [n for n in numbers if n > 0])

words = ["kubernetes", "git", "docker", "ai"]
print("Shortest first:", sorted(words, key=len))
print("Longest:", max(words, key=lambda w: len(w)))
```

## 5. Example 2 — Practical Example: Sorting and ranking infrastructure data

```python
pods = [
    {"name": "api-7d9f", "restarts": 2, "cpu_m": 230, "age_h": 50},
    {"name": "worker-5c2a", "restarts": 14, "cpu_m": 480, "age_h": 3},
    {"name": "redis-0", "restarts": 0, "cpu_m": 90, "age_h": 400},
    {"name": "cron-28ab", "restarts": 5, "cpu_m": 15, "age_h": 1},
]

by_cpu = sorted(pods, key=lambda p: p["cpu_m"], reverse=True)
print("Top CPU consumers:", [p["name"] for p in by_cpu[:2]])

worst = max(pods, key=lambda p: p["restarts"])
print(f"Most restarts: {worst['name']} ({worst['restarts']})")

newest = min(pods, key=lambda p: p["age_h"])
print("Newest pod:", newest["name"])

# Multi-level sort: restarts descending, then name ascending
ranked = sorted(pods, key=lambda p: (-p["restarts"], p["name"]))
for p in ranked:
    print(f"{p['name']:<12} restarts={p['restarts']}")

# Version strings sorted numerically
releases = ["v1.10.0", "v1.2.3", "v1.9.12", "v2.0.0"]
print(sorted(releases, key=lambda v: [int(x) for x in v[1:].split(".")]))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `map` applies a function to every item; `filter` keeps items where the function returns True. Wrap them in `list()` to see the result.
- `sorted(numbers, key=lambda n: abs(n))` sorts by absolute value.
- `key=len` passes the built-in `len` function directly — no lambda needed.

**Example 2**
- `key=lambda p: p["cpu_m"]` tells `sorted` which field to compare.
- `max`/`min` with `key` find the record with the largest/smallest value.
- Returning a tuple from the key gives multi-level sorting; `-p["restarts"]` sorts that part descending.
- The version-sort lambda turns `"v1.10.0"` into `[1, 10, 0]`.

## 7. Expected Output

**Example 1:**

```text
5
Doubled: [10, -6, 24, 0, -16, 14]
Positive: [5, 12, 7]
By absolute value: [0, -3, 5, 7, -8, 12]
Doubled: [10, -6, 24, 0, -16, 14]
Positive: [5, 12, 7]
Shortest first: ['ai', 'git', 'docker', 'kubernetes']
Longest: kubernetes
```

**Example 2:**

```text
Top CPU consumers: ['worker-5c2a', 'api-7d9f']
Most restarts: worker-5c2a (14)
Newest pod: cron-28ab
worker-5c2a  restarts=14
cron-28ab    restarts=5
api-7d9f     restarts=2
redis-0      restarts=0
['v1.2.3', 'v1.9.12', 'v1.10.0', 'v2.0.0']
```

## 8. Common Mistakes

**1. Statements inside a lambda**

`lambda x: print(x); return x` is invalid. A lambda holds one expression. Use `def` for anything bigger.

**2. Forgetting `list()` around map/filter**

`print(map(...))` shows `<map object ...>`. Convert with `list()`.

**3. Unreadable lambdas**

If you can't understand a lambda at a glance, write a named function instead.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Sort students by marks:** Sort `[("Asha", 88), ("Ravi", 72), ("Meera", 95)]` by marks (highest first) using a lambda.
- **Task 2 (Medium) — Filter and transform files:** From `["app.log", "data.csv", "error.log", "model.pkl", "access.log"]`, use `filter` with a lambda to keep `.log` files and `map` to upper-case them.
- **Task 3 (Practical Challenge) — Cost optimisation report:** Given instances `(id, type, hourly_cost, avg_cpu)`: `[("i-1", "m5.xlarge", 0.192, 8), ("i-2", "t3.micro", 0.0104, 55), ("i-3", "c5.2xlarge", 0.34, 12), ("i-4", "m5.large", 0.096, 71)]`, find idle instances (avg_cpu < 15) with `filter`, sort them by monthly cost (730 h) descending with a lambda, and print the potential monthly savings.

## 10. DevOps/MLOps Connection

- **DevOps:** sorting instances, pods, log entries or alerts by a field; picking the worst offender with `max(..., key=...)`.
- **Cloud:** ranking resources by cost or age in cleanup scripts.
- **Data/ML:** `df["col"].apply(lambda x: ...)` in Pandas, sorting models by score, quick feature transformations.

## 11. Interview Questions

**Q1. What is a lambda function?**

<details><summary>Show answer</summary>

An anonymous single-expression function created with the `lambda` keyword.

</details>

**Q2. What are the limitations of a lambda?**

<details><summary>Show answer</summary>

Only one expression; no statements, annotations or docstrings; can be less readable.

</details>

**Q3. How do you sort a list of dicts by a key?**

<details><summary>Show answer</summary>

`sorted(items, key=lambda d: d["field"])` or `operator.itemgetter("field")`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 44 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 043](../../04-functions/day-043/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 045 ➡](../../04-functions/day-045/README.md)
