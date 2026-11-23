# Day 026 — Dictionaries

[⬅ Day 025](../../02-strings-collections/day-025/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 027 ➡](../../03-dictionaries-logic/day-027/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 3 — Dictionaries and Programming Logic | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create dictionaries of key → value pairs
- Read, add, update and delete entries
- Use `get()` to read keys safely and `in` to test for keys

## 2. Topic Explanation

A **dictionary** (`dict`) stores data as **key → value** pairs:

```python
server = {"name": "web-01", "cpu": 4, "env": "prod"}
```

- Look up a value by its **key**, not by position: `server["name"]`.
- Keys must be unique and immutable (strings, numbers, tuples). Values can be anything.
- Dicts keep insertion order (Python 3.7+).
- Missing key with `d["x"]` → `KeyError`. Use `d.get("x", default)` to avoid it.

Analogy: a dictionary is like a phone's contact list — you look up *by name* (the key) to get the number (the value).

Dictionaries are probably the most important data structure for DevOps: **JSON, YAML, Kubernetes manifests, API responses and environment variables all map naturally to dicts.**

## 3. Syntax

```python
my_dict = {"key1": value1, "key2": value2}
value = my_dict["key1"]               # KeyError if missing
value = my_dict.get("key3", default)  # safe
my_dict["key3"] = value3              # add or update
del my_dict["key1"]                   # delete
"key2" in my_dict                     # test for key
```

| Part | Meaning |
|---|---|
| `{key: value}` | Curly braces with colon-separated pairs. |
| `d[key]` | Read (or assign) the value for key. |
| `d.get(key, default)` | Returns default (or None) instead of raising KeyError. |
| `del d[key]` | Removes a key. |
| `key in d` | True if the key exists (checks keys, not values). |

## 4. Example 1 — Basic Example: Dictionary basics

```python
student = {"name": "Asha", "course": "Python", "day": 26}
print(student)
print("Name:", student["name"])

student["day"] = 27                 # update existing key
student["city"] = "Pune"            # add new key
print("Updated:", student)

del student["course"]
print("After delete:", student)

print("Has 'city'?", "city" in student)
print("Email:", student.get("email", "not provided"))
print("Number of keys:", len(student))
```

## 5. Example 2 — Practical Example: A Kubernetes deployment as a dictionary

```python
deployment = {
    "name": "orders-api",
    "namespace": "prod",
    "replicas": 3,
    "image": "registry.example.com/orders-api:2.4.1",
    "labels": {"app": "orders", "tier": "backend"},
}

print(f"Deployment {deployment['name']} in namespace {deployment['namespace']}")
print("Replicas:", deployment["replicas"])
print("App label:", deployment["labels"]["app"])

# Scale up
deployment["replicas"] += 2
print("Scaled to:", deployment["replicas"])

# Read optional settings safely
cpu_limit = deployment.get("cpu_limit", "500m")
print("CPU limit (default if missing):", cpu_limit)

# Image tag is the text after the last ':'
tag = deployment["image"].split(":")[-1]
print("Image tag:", tag)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `student["day"] = 27` updates; assigning to a new key (`"city"`) adds it.
- `del` removes a key; `in` checks keys.
- `get("email", "not provided")` returns the default because the key is missing — no crash.

**Example 2**
- A dict can contain another dict (`labels`). Chain lookups: `deployment["labels"]["app"]`.
- `deployment["replicas"] += 2` reads, adds and stores back.
- `.get()` with a default models optional configuration values — exactly how Helm charts use default values.

## 7. Expected Output

**Example 1:**

```text
{'name': 'Asha', 'course': 'Python', 'day': 26}
Name: Asha
Updated: {'name': 'Asha', 'course': 'Python', 'day': 27, 'city': 'Pune'}
After delete: {'name': 'Asha', 'day': 27, 'city': 'Pune'}
Has 'city'? True
Email: not provided
Number of keys: 3
```

**Example 2:**

```text
Deployment orders-api in namespace prod
Replicas: 3
App label: orders
Scaled to: 5
CPU limit (default if missing): 500m
Image tag: 2.4.1
```

## 8. Common Mistakes

**1. `KeyError` on missing keys**

`config["timeout"]` crashes if the key is absent. Use `config.get("timeout", 30)` for optional settings.

**2. Using a list as a key**

`{["a"]: 1}` → `TypeError: unhashable type: 'list'`. Use a tuple.

**3. Checking values with `in`**

`"web-01" in server` checks **keys**. To search values use `"web-01" in server.values()`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Book record:** Create a dict for a book (title, author, year). Print each field, then add `rating`, update `year` and print the dict.
- **Task 2 (Medium) — Port lookup:** Create a dict mapping service names to ports (ssh 22, http 80, https 443, postgres 5432, redis 6379). Look up `postgres` with `[]`, and `mongodb` with `.get()` returning `unknown`. Print how many services are known.
- **Task 3 (Practical Challenge) — Environment config merge:** You have `defaults = {"replicas": 1, "log_level": "INFO", "debug": False}` and `prod_overrides = {"replicas": 5, "log_level": "WARNING"}`. Create a final config where overrides win (copy defaults, then assign each override key). Print the final config and which keys were overridden.

## 10. DevOps/MLOps Connection

- **DevOps:** YAML (Ansible, Kubernetes, Docker Compose) and JSON are dictionaries once loaded into Python. Merging defaults with overrides is how Helm values and Ansible variables work.
- **Cloud:** every boto3 response is a dict (`response["Reservations"][0]["Instances"]`).
- **Data:** a row of data is naturally a dict `{"column": value}`.
- **MLOps:** model hyper-parameters, metrics and API request/response bodies are dicts.

## 11. Interview Questions

**Q1. What is the time complexity of a dict lookup?**

<details><summary>Show answer</summary>

Average O(1), because dicts are hash tables.

</details>

**Q2. How do you avoid a KeyError?**

<details><summary>Show answer</summary>

Use `d.get(key, default)`, check `key in d` first, or use `collections.defaultdict`.

</details>

**Q3. Are dictionaries ordered?**

<details><summary>Show answer</summary>

Yes, since Python 3.7 they preserve insertion order.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 26 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 025](../../02-strings-collections/day-025/README.md) | [📚 Phase 3: Dictionaries and Programming Logic](../README.md) | [🏠 Home](../../README.md) | [Day 027 ➡](../../03-dictionaries-logic/day-027/README.md)
