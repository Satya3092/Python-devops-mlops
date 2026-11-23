# Day 039 — Default Arguments

[⬅ Day 038](../../04-functions/day-038/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 040 ➡](../../04-functions/day-040/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Give parameters default values
- Order required and default parameters correctly
- Avoid the mutable-default-argument trap

## 2. Topic Explanation

A **default argument** is used when the caller does not supply a value:

```python
def connect(host, port=22, timeout=10):
    ...

connect("web-01")              # port=22, timeout=10
connect("web-01", 2222)        # port=2222, timeout=10
```

Defaults make functions convenient: common cases need fewer arguments, special cases can still override.

Rules:
- Parameters **with** defaults must come **after** parameters without defaults.
- Default values are evaluated **once**, when the function is defined.

**The mutable default trap:** never use a list or dict as a default (`def f(items=[])`). The same list is shared between calls! Use `None` and create the list inside:

```python
def add_tag(tag, tags=None):
    if tags is None:
        tags = []
```

## 3. Syntax

```python
def function_name(required, optional=default_value):
    ...

def safe(items=None):
    if items is None:
        items = []
```

| Part | Meaning |
|---|---|
| `param=value` | Default used when the argument is omitted. |
| `order` | Required parameters first, then those with defaults. |
| `None default` | Safe pattern for mutable defaults. |

## 4. Example 1 — Basic Example: Defaults in action

```python
def greet(name, greeting="Hello", punctuation="!"):
    return f"{greeting}, {name}{punctuation}"


print(greet("Asha"))
print(greet("Ravi", "Good morning"))
print(greet("Meera", "Hi", "?"))


# The mutable default trap
def add_item_buggy(item, items=[]):
    items.append(item)
    return items


print(add_item_buggy("a"))
print(add_item_buggy("b"))       # surprise: 'a' is still there!


def add_item_safe(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items


print(add_item_safe("a"))
print(add_item_safe("b"))
```

## 5. Example 2 — Practical Example: A docker run command builder with sensible defaults

```python
def docker_run(image, tag="latest", name=None, ports=None, detach=True, restart="unless-stopped"):
    """Build a docker run command; only the image is required."""
    parts = ["docker run"]
    if detach:
        parts.append("-d")
    if name:
        parts.append(f"--name {name}")
    for host_port, container_port in (ports or {}).items():
        parts.append(f"-p {host_port}:{container_port}")
    parts.append(f"--restart {restart}")
    parts.append(f"{image}:{tag}")
    return " ".join(parts)


print(docker_run("redis"))
print(docker_run("nginx", "1.27", name="web", ports={8080: 80}))
print(docker_run("python", "3.12", detach=False, restart="no"))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `greet("Asha")` uses both defaults; later calls override them from left to right.
- `add_item_buggy` shares ONE list across calls because the default `[]` was created once. The second call returns `['a', 'b']`.
- `add_item_safe` creates a fresh list each call.

**Example 2**
- Only `image` is required; everything else has a sensible default — just like real CLIs.
- `ports=None` plus `(ports or {})` avoids the mutable default trap.
- The command is built as a list of parts and joined with spaces.

## 7. Expected Output

**Example 1:**

```text
Hello, Asha!
Good morning, Ravi!
Hi, Meera?
['a']
['a', 'b']
['a']
['b']
```

**Example 2:**

```text
docker run -d --restart unless-stopped redis:latest
docker run -d --name web -p 8080:80 --restart unless-stopped nginx:1.27
docker run --restart no python:3.12
```

## 8. Common Mistakes

**1. Default before required**

`def f(a=1, b):` → `SyntaxError: non-default argument follows default argument`.

**2. Mutable defaults**

`def f(x=[])` shares state across calls. Use `None`.

**3. Defaults computed at definition time**

`def log(ts=datetime.now())` freezes the timestamp at import time. Use `None` and compute inside.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Power function:** Write `power(base, exponent=2)` and print `power(5)`, `power(2, 10)`.
- **Task 2 (Medium) — Backup filename:** Write `backup_name(db, date="2026-11-20", ext="sql.gz")` that returns `<db>-<date>.<ext>`. Call it with only the db, with a custom date, and with a custom extension.
- **Task 3 (Practical Challenge) — HTTP request description:** Write `describe_request(url, method="GET", headers=None, timeout=5, retries=3)` that returns a multi-line description. Merge any given headers with a default `User-Agent: devops-script/1.0` header without modifying the caller's dict. Show the caller's dict is unchanged.

## 10. DevOps/MLOps Connection

- **DevOps:** CLI tools and helper libraries use defaults everywhere: `timeout=30`, `region="us-east-1"`, `retries=3`.
- **Cloud:** boto3 client options such as `region_name` and retry configs have defaults you override when needed.
- **ML:** scikit-learn estimators are full of defaults: `RandomForestClassifier(n_estimators=100, max_depth=None)`.

## 11. Interview Questions

**Q1. Why should you not use a list as a default argument?**

<details><summary>Show answer</summary>

Defaults are evaluated once; the same list object is shared between calls, so modifications persist across calls.

</details>

**Q2. Can a required parameter come after a default parameter?**

<details><summary>Show answer</summary>

No, it is a SyntaxError (except keyword-only parameters after `*`).

</details>

**Q3. What is the idiomatic replacement for a mutable default?**

<details><summary>Show answer</summary>

Use `None` as default and create the object inside the function.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 39 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 038](../../04-functions/day-038/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 040 ➡](../../04-functions/day-040/README.md)
