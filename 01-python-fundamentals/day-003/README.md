# Day 003 — Python Data Types

[⬅ Day 002](../../01-python-fundamentals/day-002/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 004 ➡](../../01-python-fundamentals/day-004/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Name Python's core built-in data types
- Use `type()` to inspect the type of any value
- Choose the right type for a piece of data

## 2. Topic Explanation

Every value in Python has a **data type**. The type decides what you can do with the value — you can add two numbers, but you cannot meaningfully add a number to a list.

| Type | Meaning | Example |
|---|---|---|
| `int` | Whole numbers | `8080`, `-3` |
| `float` | Decimal numbers | `99.5`, `0.75` |
| `str` | Text (string) | `"nginx"` |
| `bool` | True / False | `True` |
| `list` | Ordered, changeable collection | `["web-01", "web-02"]` |
| `tuple` | Ordered, unchangeable collection | `(80, 443)` |
| `set` | Unordered collection of unique items | `{"prod", "dev"}` |
| `dict` | Key → value pairs | `{"cpu": 70, "mem": 40}` |
| `NoneType` | "No value yet" | `None` |

Python is **dynamically typed**: you never declare the type. Python figures it out from the value. Use `type(value)` to ask what something is.

Analogy: data types are like file formats. A `.png` and a `.csv` are both files, but you open them with different tools. Likewise `"80"` (a string) and `80` (an integer) look similar but behave differently.

You will learn each collection type deeply in later days — today is about recognising them.

## 3. Syntax

```python
type(value)                 # returns the type of value
isinstance(value, int)      # True if value is an int
```

| Part | Meaning |
|---|---|
| `type()` | Built-in function that returns the data type of a value. |
| `isinstance(v, T)` | Returns `True` if `v` is of type `T`. Preferred for checks in real code. |
| `None` | Special value meaning 'nothing / unknown yet'. |

## 4. Example 1 — Basic Example: Inspecting types

```python
port = 8080
cpu_load = 0.75
hostname = "web-01"
is_healthy = True
nothing_yet = None

print(port, type(port))
print(cpu_load, type(cpu_load))
print(hostname, type(hostname))
print(is_healthy, type(is_healthy))
print(nothing_yet, type(nothing_yet))
```

## 5. Example 2 — Practical Example: One server described with every type

```python
server = {                                   # dict: key -> value
    "name": "prod-web-01",                   # str
    "cpu_cores": 4,                          # int
    "load_average": 1.85,                    # float
    "in_maintenance": False,                 # bool
    "ports": (80, 443),                      # tuple (fixed)
    "tags": ["web", "nginx"],                # list (changeable)
    "environments": {"prod", "prod"},        # set (duplicates removed)
    "owner": None,                           # NoneType (unknown)
}

for key in server:                           # loop over keys (you'll learn loops on Day 29)
    value = server[key]
    print(key, "=", value, "->", type(value).__name__)

print("Is cpu_cores an int?", isinstance(server["cpu_cores"], int))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Each variable gets a different kind of value; `type()` reports `int`, `float`, `str`, `bool` and `NoneType`.
- `0.75` has a decimal point, so it is a `float`. `True` (capital T) is a `bool`.

**Example 2**
- The whole server is a `dict` — curly braces with `key: value` pairs.
- `{"prod", "prod"}` becomes `{'prod'}` because a `set` keeps only unique values.
- `type(value).__name__` gives just the name of the type (e.g. `int`) instead of `<class 'int'>`.
- `isinstance(..., int)` is the recommended way to test a type.

## 7. Expected Output

**Example 1:**

```text
8080 <class 'int'>
0.75 <class 'float'>
web-01 <class 'str'>
True <class 'bool'>
None <class 'NoneType'>
```

**Example 2:**

```text
name = prod-web-01 -> str
cpu_cores = 4 -> int
load_average = 1.85 -> float
in_maintenance = False -> bool
ports = (80, 443) -> tuple
tags = ['web', 'nginx'] -> list
environments = {'prod'} -> set
owner = None -> NoneType
Is cpu_cores an int? True
```

## 8. Common Mistakes

**1. Confusing `"80"` with `80`**

`"80"` is a string (text). `"80" + 1` raises `TypeError`. Convert first with `int("80")` (Day 6).

**2. Lower-case booleans**

`true` / `false` are not valid. Python uses `True` and `False` with a capital letter.

**3. Thinking `{}` is an empty set**

`{}` creates an empty **dict**. An empty set is `set()`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Type detective:** Create one variable of each type: int, float, str, bool, list, tuple, set, dict, None. Print each value with its type name.
- **Task 2 (Medium) — Pick the right type:** For each piece of Kubernetes pod data choose the best type and store it: pod name, replica count, CPU limit in cores (0.5), is ready, container ports 80 and 443 (fixed), labels (app=web, tier=frontend). Print each with its type.
- **Task 3 (Practical Challenge) — Type validation:** Given `config = {"port": "8080", "debug": True, "workers": 4, "timeout": 2.5}`, check with `isinstance` whether `port` and `workers` are integers and print which settings are invalid.

## 10. DevOps/MLOps Connection

- **DevOps:** YAML/JSON configs are loaded into Python as `dict`, `list`, `str`, `int` and `bool`. Bugs often come from `"8080"` vs `8080` — exactly today's lesson.
- **Cloud automation:** boto3 returns AWS responses as nested dicts and lists.
- **Data engineering:** Columns in a dataset have types; wrong types break joins and aggregations.
- **ML/MLOps:** Models need numeric features (`int`/`float`). Validating input types is the first job of a prediction API.

## 11. Interview Questions

**Q1. What does 'dynamically typed' mean?**

<details><summary>Show answer</summary>

Types belong to values, not variable names, and are determined at run time. The same name can later refer to a value of a different type.

</details>

**Q2. Which built-in types are mutable and which are immutable?**

<details><summary>Show answer</summary>

Mutable: list, dict, set. Immutable: int, float, str, bool, tuple, frozenset, None.

</details>

**Q3. Why prefer `isinstance()` over `type(x) == int`?**

<details><summary>Show answer</summary>

`isinstance` also accepts subclasses and can check several types at once, e.g. `isinstance(x, (int, float))`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 3 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 002](../../01-python-fundamentals/day-002/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 004 ➡](../../01-python-fundamentals/day-004/README.md)
