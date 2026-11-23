# Day 051 — Working with JSON

[⬅ Day 050](../../05-files-exceptions/day-050/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 052 ➡](../../05-files-exceptions/day-052/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Convert between Python objects and JSON with `json.dumps/loads`
- Read and write JSON files with `json.load/dump`
- Pretty-print and navigate JSON data

## 2. Topic Explanation

**JSON** (JavaScript Object Notation) is the language of APIs and modern configuration. It maps almost 1-to-1 to Python:

| JSON | Python |
|---|---|
| object `{}` | `dict` |
| array `[]` | `list` |
| string | `str` |
| number | `int` / `float` |
| `true` / `false` | `True` / `False` |
| `null` | `None` |

The `json` module (built in):
- `json.dumps(obj)` → Python object **to JSON string** ("dump string").
- `json.loads(text)` → JSON string **to Python object** ("load string").
- `json.dump(obj, file)` / `json.load(file)` → the same with files.
- `indent=2` pretty-prints; `sort_keys=True` sorts keys (nice for diffs in Git).

JSON keys must be strings and tuples become lists. Sets, dates and custom objects are not JSON-serialisable without conversion.

> Run the examples from inside this day's folder (`cd` into it first) so the relative file paths work.

## 3. Syntax

```python
import json

text = json.dumps(python_obj, indent=2)
obj = json.loads(text)

with open("data.json", "w", encoding="utf-8") as f:
    json.dump(python_obj, f, indent=2)
with open("data.json", encoding="utf-8") as f:
    obj = json.load(f)
```

| Part | Meaning |
|---|---|
| `dumps / loads` | Work with JSON **strings**. |
| `dump / load` | Work with JSON **files**. |
| `indent=2` | Pretty-print with 2-space indentation. |
| `sort_keys=True` | Output keys alphabetically. |

## 4. Example 1 — Basic Example: Python ↔ JSON

```python
import json

server = {"name": "web-01", "ports": [80, 443], "healthy": True, "owner": None, "cpu": 0.75}
text = json.dumps(server)
print("JSON string:", text)
print("Type:", type(text).__name__)

print("Pretty:")
print(json.dumps(server, indent=2, sort_keys=True))

api_response = '{"status": "ok", "count": 2, "items": [{"id": 1}, {"id": 2}], "next": null}'
data = json.loads(api_response)
print("Parsed type:", type(data).__name__)
print("Count:", data["count"], "| First id:", data["items"][0]["id"], "| Next:", data["next"])
```

## 5. Example 2 — Practical Example: Reading, updating and saving a JSON config file

```python
import json

config = {
    "service": "orders-api",
    "version": "2.4.1",
    "replicas": 3,
    "env": {"LOG_LEVEL": "INFO", "FEATURE_NEW_CHECKOUT": False},
    "healthcheck": {"path": "/health", "interval_seconds": 10},
}

with open("service_config.json", "w", encoding="utf-8") as f:
    json.dump(config, f, indent=2)
print("Saved config")

# Later (another script / another day): load, modify, save
with open("service_config.json", encoding="utf-8") as f:
    loaded = json.load(f)

loaded["version"] = "2.5.0"
loaded["replicas"] += 2
loaded["env"]["FEATURE_NEW_CHECKOUT"] = True
loaded["env"]["LOG_LEVEL"] = "DEBUG"

with open("service_config.json", "w", encoding="utf-8") as f:
    json.dump(loaded, f, indent=2)

with open("service_config.json", encoding="utf-8") as f:
    print(f.read())

# Sets are not JSON serialisable - convert them first
tags = {"prod", "web"}
try:
    json.dumps({"tags": tags})
except TypeError as error:
    print("TypeError:", error)
print(json.dumps({"tags": sorted(tags)}))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `dumps` converts `True` → `true` and `None` → `null`.
- `indent=2, sort_keys=True` produces readable, diff-friendly output.
- `loads` turns the API response text into dicts and lists you can navigate.

**Example 2**
- `json.dump` writes the dict to a file; `json.load` reads it back.
- Nested values are modified like any dict, then saved again — the typical "update a config" job.
- A `set` cannot be serialised; convert it to a (sorted) list first.

## 7. Expected Output

**Example 1:**

```text
JSON string: {"name": "web-01", "ports": [80, 443], "healthy": true, "owner": null, "cpu": 0.75}
Type: str
Pretty:
{
  "cpu": 0.75,
  "healthy": true,
  "name": "web-01",
  "owner": null,
  "ports": [
    80,
    443
  ]
}
Parsed type: dict
Count: 2 | First id: 1 | Next: None
```

**Example 2:**

```text
Saved config
{
  "service": "orders-api",
  "version": "2.5.0",
  "replicas": 5,
  "env": {
    "LOG_LEVEL": "DEBUG",
    "FEATURE_NEW_CHECKOUT": true
  },
  "healthcheck": {
    "path": "/health",
    "interval_seconds": 10
  }
}
TypeError: Object of type set is not JSON serializable
{"tags": ["prod", "web"]}
```

## 8. Common Mistakes

**1. Confusing `load` and `loads`**

`json.load(text)` fails — `load` expects a **file**. Use `loads` for strings.

**2. Single quotes in JSON**

`{'a': 1}` is not valid JSON. JSON requires double quotes. Use `json.dumps` instead of `str(dict)`.

**3. Trailing commas**

`{"a": 1,}` is invalid JSON and raises `json.JSONDecodeError`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Dict to JSON:** Convert a dict describing yourself (name, skills list, years, learning_python=True) to a pretty JSON string and print it.
- **Task 2 (Medium) — Parse an API response:** Parse this JSON string: `{"pods": [{"name": "api-1", "status": "Running"}, {"name": "api-2", "status": "Pending"}, {"name": "db-0", "status": "Running"}]}` and print the names of running pods and the count of non-running pods.
- **Task 3 (Practical Challenge) — Feature-flag manager:** Create `flags.json` with flags `{"dark_mode": false, "new_checkout": true, "beta_search": false}`. Write functions `load_flags(path)`, `save_flags(path, flags)` and `toggle(path, name)` (which loads, flips one flag, saves, and returns the new value; unknown flags raise `KeyError`). Toggle two flags and print the final file.

## 10. DevOps/MLOps Connection

- **DevOps:** `kubectl get pods -o json`, `terraform show -json`, `docker inspect` and most CLIs output JSON that Python can parse.
- **Cloud:** every AWS API speaks JSON; IAM policies are JSON documents.
- **Data engineering:** JSON lines (`.jsonl`) logs and event streams.
- **MLOps:** prediction API requests/responses (FastAPI, Day 98) and metrics files are JSON.

## 11. Interview Questions

**Q1. What is the difference between `json.load` and `json.loads`?**

<details><summary>Show answer</summary>

`load` reads from a file object; `loads` parses a string.

</details>

**Q2. Which Python types can't be serialised to JSON by default?**

<details><summary>Show answer</summary>

Sets, tuples (become lists), datetime, bytes, custom objects and non-string dict keys (converted to strings for int/float/bool).

</details>

**Q3. How do you pretty-print JSON?**

<details><summary>Show answer</summary>

`json.dumps(obj, indent=2)` (optionally `sort_keys=True`) or `python -m json.tool file.json` on the command line.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 51 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 050](../../05-files-exceptions/day-050/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 052 ➡](../../05-files-exceptions/day-052/README.md)
