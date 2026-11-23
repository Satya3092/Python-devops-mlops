# Day 024 — Tuples

[⬅ Day 023](../../02-strings-collections/day-023/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 025 ➡](../../02-strings-collections/day-025/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 2 — Strings and Collections | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create tuples and understand immutability
- Pack and unpack tuples (including `*rest`)
- Know when to use a tuple instead of a list

## 2. Topic Explanation

A **tuple** is like a list, but **immutable** — once created it cannot change. Tuples use parentheses:

```python
endpoint = ("api.example.com", 443)
```

Why use them?
- **Safety:** data that must not change (coordinates, a DB connection target, RGB colours).
- **Meaning:** a tuple usually represents *one record with fixed fields* (host, port), while a list represents *many similar items*.
- They can be **dictionary keys** and set members (lists cannot).
- Functions return multiple values as a tuple.

**Packing and unpacking**
```python
host, port = endpoint          # unpacking
first, *rest = (1, 2, 3, 4)    # first = 1, rest = [2, 3, 4]
```

A one-item tuple needs a trailing comma: `("web",)`. Without it, `("web")` is just a string in parentheses.

## 3. Syntax

```python
my_tuple = (item1, item2)
single = (item,)
a, b = my_tuple            # unpacking
first, *rest = my_tuple    # extended unpacking
```

| Part | Meaning |
|---|---|
| `( , )` | Parentheses and commas create a tuple; the comma is what matters. |
| `(x,)` | Single-item tuple needs a trailing comma. |
| `a, b = t` | Unpacking: number of names must match the number of items. |
| `*rest` | Collects the remaining items into a list. |

## 4. Example 1 — Basic Example: Tuple basics

```python
database = ("db.internal", 5432, "orders")
print(database)
print("Host:", database[0])
print("Length:", len(database))

host, port, name = database
print(f"Connecting to {name} on {host}:{port}")

single = ("web",)
not_a_tuple = ("web")
print(type(single).__name__, type(not_a_tuple).__name__)

try:                                   # exceptions are covered on Day 52
    database[1] = 3306
except TypeError as error:
    print("Cannot modify a tuple:", error)
```

## 5. Example 2 — Practical Example: Records, multiple return values and dictionary keys

```python
# Each tuple is one fixed-format record
deployments = [
    ("orders", "2.1.0", "success"),
    ("payments", "1.4.2", "failed"),
    ("search", "3.0.1", "success"),
]
for service, version, result in deployments:
    print(f"{service:<10} {version:<7} {result}")

# A function returning two values gives back a tuple
def min_max(values):
    return min(values), max(values)

lowest, highest = min_max([120, 98, 450, 230])
print("Lowest:", lowest, "Highest:", highest)

# Tuples can be dict keys: latency per (region, service)
latency = {("us-east-1", "orders"): 120, ("eu-west-1", "orders"): 180}
print("EU orders latency:", latency[("eu-west-1", "orders")], "ms")

# Extended unpacking: first stage and the rest
first_stage, *other_stages = ("build", "test", "scan", "deploy")
print("First:", first_stage, "| Others:", other_stages)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Tuples are indexed like lists. Unpacking assigns each item to a name in one line.
- `("web",)` is a tuple; `("web")` is just a string.
- Assigning to an index raises `TypeError` — tuples are immutable (we catch the error to show the message).

**Example 2**
- Looping over a list of tuples and unpacking each one is very common.
- `return min(values), max(values)` returns a tuple; the caller unpacks it.
- Tuples can be dictionary keys because they are immutable (hashable).
- `*other_stages` collects the remaining items.

## 7. Expected Output

**Example 1:**

```text
('db.internal', 5432, 'orders')
Host: db.internal
Length: 3
Connecting to orders on db.internal:5432
tuple str
Cannot modify a tuple: 'tuple' object does not support item assignment
```

**Example 2:**

```text
orders     2.1.0   success
payments   1.4.2   failed
search     3.0.1   success
Lowest: 98 Highest: 450
EU orders latency: 180 ms
First: build | Others: ['test', 'scan', 'deploy']
```

## 8. Common Mistakes

**1. Forgetting the comma in a single-item tuple**

`ports = (80)` is the integer 80. Write `(80,)`.

**2. Wrong number of names when unpacking**

`a, b = (1, 2, 3)` → `ValueError: too many values to unpack`. Use `a, b, c` or `a, *rest`.

**3. Trying to append to a tuple**

Tuples have no `append`. Convert: `lst = list(t)`, change it, then `tuple(lst)` if needed.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Coordinates:** Store the latitude and longitude of a data centre `(19.07, 72.87)` in a tuple, unpack it and print a sentence with both values.
- **Task 2 (Medium) — Version tuple comparison:** Convert version strings `"1.10.2"` and `"1.9.8"` to tuples of ints and compare them. Print which is newer.
- **Task 3 (Practical Challenge) — Server inventory report:** Given inventory records `(hostname, ip, cpu_cores, memory_gb, role)` for 4 servers, print a table, the total CPU cores and memory, and the hostnames of all `db` servers. Use unpacking in the loop and `*_` to ignore fields you do not need in the second loop.

## 10. DevOps/MLOps Connection

- **DevOps:** fixed records like `(host, port)`, rows from a database query, or version numbers `(1, 10, 2)` that compare correctly.
- **Cloud:** multiple return values `(success, message)` from helper functions.
- **ML:** array shapes are tuples — `X.shape` returns `(rows, columns)`; `train_test_split` returns a tuple you unpack into `X_train, X_test, y_train, y_test`.

## 11. Interview Questions

**Q1. When would you use a tuple over a list?**

<details><summary>Show answer</summary>

For fixed collections that should not change, records with a fixed structure, dict keys, and returning multiple values.

</details>

**Q2. Why can tuples be dictionary keys but lists cannot?**

<details><summary>Show answer</summary>

Keys must be hashable; tuples (of immutable items) are immutable and hashable, lists are mutable and unhashable.

</details>

**Q3. What does `a, *b = (1, 2, 3)` do?**

<details><summary>Show answer</summary>

`a = 1`, `b = [2, 3]`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 24 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 023](../../02-strings-collections/day-023/README.md) | [📚 Phase 2: Strings and Collections](../README.md) | [🏠 Home](../../README.md) | [Day 025 ➡](../../02-strings-collections/day-025/README.md)
