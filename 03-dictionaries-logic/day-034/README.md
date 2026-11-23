# Day 034 — List Comprehension

[⬅ Day 033](../../03-dictionaries-logic/day-033/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 035 ➡](../../03-dictionaries-logic/day-035/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Build lists in one line with list comprehensions
- Filter items with an `if` clause
- Use dict and set comprehensions

## 2. Topic Explanation

A **list comprehension** builds a new list from an existing iterable in one readable line:

```python
squares = [n * n for n in range(5)]          # [0, 1, 4, 9, 16]
```

It is a compact version of:
```python
squares = []
for n in range(5):
    squares.append(n * n)
```

Read it as English: "**n × n for each n in range(5)**".

Add a filter: `[n for n in numbers if n > 0]`.
Transform conditionally: `["even" if n % 2 == 0 else "odd" for n in numbers]` (note: the `if/else` goes **before** `for`).

The same syntax builds:
- **dicts:** `{host: len(host) for host in hosts}`
- **sets:** `{ip for ip in ip_list}`

Rule of thumb: if a comprehension no longer fits comfortably on one or two lines, use a normal loop.

## 3. Syntax

```python
[expression for item in iterable]
[expression for item in iterable if condition]
[a if condition else b for item in iterable]
{key_expr: value_expr for item in iterable}
{expression for item in iterable}
```

| Part | Meaning |
|---|---|
| `expression` | What to put in the new list for each item. |
| `for item in iterable` | The loop part. |
| `if condition (end)` | Filter: keep only matching items. |
| `a if c else b (start)` | Choose a value for every item. |
| `{k: v for ...}` | Dict comprehension. |

## 4. Example 1 — Basic Example: Comprehension basics

```python
numbers = [3, -1, 8, 0, -5, 12]

squares = [n ** 2 for n in numbers]
positives = [n for n in numbers if n > 0]
labels = ["pos" if n > 0 else "non-pos" for n in numbers]
print("Squares:", squares)
print("Positives:", positives)
print("Labels:", labels)

words = ["Docker", "Kubernetes", "Git"]
lengths = {word: len(word) for word in words}
first_letters = {word[0].lower() for word in words + ["Grafana"]}
print("Lengths:", lengths)
print("First letters:", sorted(first_letters))
```

## 5. Example 2 — Practical Example: Transforming infrastructure data

```python
instances = [
    {"id": "i-01", "state": "running", "type": "t3.micro", "env": "prod"},
    {"id": "i-02", "state": "stopped", "type": "t3.large", "env": "dev"},
    {"id": "i-03", "state": "running", "type": "m5.large", "env": "prod"},
    {"id": "i-04", "state": "running", "type": "t3.micro", "env": "dev"},
]

running_ids = [i["id"] for i in instances if i["state"] == "running"]
prod_types = [i["type"] for i in instances if i["env"] == "prod"]
id_to_state = {i["id"]: i["state"] for i in instances}
unique_types = sorted({i["type"] for i in instances})

print("Running:", running_ids)
print("Prod instance types:", prod_types)
print("State map:", id_to_state)
print("Unique types:", unique_types)

# Clean a list of raw lines from a config file
raw_lines = ["  nginx ", "", "# comment", "redis", "  postgres"]
packages = [line.strip() for line in raw_lines if line.strip() and not line.strip().startswith("#")]
print("Packages to install:", packages)

# Build docker commands
commands = [f"docker pull {image}:latest" for image in packages]
print(commands)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `[n ** 2 for n in numbers]` transforms every item.
- `[n for n in numbers if n > 0]` filters.
- `["pos" if n > 0 else "non-pos" for n in numbers]` maps every item to one of two values.
- `{word: len(word) ...}` is a dict comprehension; `{... for ...}` without colons is a set comprehension.

**Example 2**
- Filtering a list of dicts by a field is one line — the same as `jq '.[] | select(.state=="running") | .id'`.
- `id_to_state` converts a list into a lookup dict.
- The package example combines cleaning (`strip`) and filtering (skip empty lines and comments).

## 7. Expected Output

**Example 1:**

```text
Squares: [9, 1, 64, 0, 25, 144]
Positives: [3, 8, 12]
Labels: ['pos', 'non-pos', 'pos', 'non-pos', 'non-pos', 'pos']
Lengths: {'Docker': 6, 'Kubernetes': 10, 'Git': 3}
First letters: ['d', 'g', 'k']
```

**Example 2:**

```text
Running: ['i-01', 'i-03', 'i-04']
Prod instance types: ['t3.micro', 'm5.large']
State map: {'i-01': 'running', 'i-02': 'stopped', 'i-03': 'running', 'i-04': 'running'}
Unique types: ['m5.large', 't3.large', 't3.micro']
Packages to install: ['nginx', 'redis', 'postgres']
['docker pull nginx:latest', 'docker pull redis:latest', 'docker pull postgres:latest']
```

## 8. Common Mistakes

**1. Putting `if/else` at the end**

`[x for x in nums if x > 0 else 0]` is a `SyntaxError`. A filter `if` goes at the end; a conditional value `a if c else b` goes at the start.

**2. Overly complex comprehensions**

Nested comprehensions with multiple conditions are hard to read. Use a regular loop.

**3. Using a comprehension for side effects**

`[print(x) for x in items]` builds a useless list. Use a normal `for` loop for actions.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Uppercase names:** Convert `["asha", "ravi", "meera"]` to title case with a list comprehension, and make a list of name lengths.
- **Task 2 (Medium) — Filter log levels:** From `logs = ["INFO ok", "ERROR db", "WARNING cpu", "ERROR disk", "INFO done"]`, build a list of error messages only (without the `ERROR ` prefix), and a dict comprehension counting each level.
- **Task 3 (Practical Challenge) — Kubernetes resource summary:** Given pods `[{"name": "api-1", "cpu_m": 250, "ready": True}, {"name": "api-2", "cpu_m": 250, "ready": False}, {"name": "worker-1", "cpu_m": 500, "ready": True}, {"name": "cron-1", "cpu_m": 100, "ready": True}]`, use comprehensions to get: names of not-ready pods, total CPU of ready pods in cores, a dict name → CPU in cores, and the set of app prefixes (text before `-`).

## 10. DevOps/MLOps Connection

- **DevOps:** filtering instances/pods/files, extracting IDs, cleaning config lines — the Python equivalent of `grep | awk | jq` one-liners.
- **Cloud:** `[b["Name"] for b in response["Buckets"]]` is how you list S3 bucket names with boto3.
- **Data/ML:** building feature lists (`[c for c in df.columns if c != "label"]`) and preprocessing text.

## 11. Interview Questions

**Q1. What is a list comprehension?**

<details><summary>Show answer</summary>

A concise syntax to create a list by applying an expression to each item of an iterable, optionally filtering: `[f(x) for x in xs if cond]`.

</details>

**Q2. Where does the filter `if` go versus a conditional `if/else`?**

<details><summary>Show answer</summary>

Filter `if` goes at the end; `a if cond else b` goes before the `for`.

</details>

**Q3. Are comprehensions faster than loops?**

<details><summary>Show answer</summary>

Usually slightly faster than an equivalent `for` + `append`, but readability should be the main reason to use them.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 34 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 033](../../03-dictionaries-logic/day-033/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 035 ➡](../../03-dictionaries-logic/day-035/README.md)
