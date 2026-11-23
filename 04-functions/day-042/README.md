# Day 042 — Variable-Length Arguments (**kwargs)

[⬅ Day 041](../../04-functions/day-041/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 043 ➡](../../04-functions/day-043/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Accept any number of keyword arguments with `**kwargs`
- Unpack dictionaries into keyword arguments with `**`
- Combine `*args` and `**kwargs` in one signature

## 2. Topic Explanation

`**kwargs` collects **extra keyword arguments into a dictionary**:

```python
def create_tags(**tags):
    print(tags)

create_tags(Env="prod", Owner="team-web")   # {'Env': 'prod', 'Owner': 'team-web'}
```

At call time, `**some_dict` **unpacks** a dict into keyword arguments:
```python
settings = {"region": "ap-south-1", "env": "prod"}
create_instance("web-01", **settings)
```

The full order of a signature is:
```python
def f(required, default=1, *args, keyword_only=2, **kwargs):
```

This is extremely common in real code:
- Passing configuration loaded from YAML/JSON (a dict) straight into a function.
- Wrapper functions that forward options: `def wrapper(*args, **kwargs): return real(*args, **kwargs)`.

Analogy: `**kwargs` is a form with an "any other details" section — the function accepts extra labelled fields it didn't know about in advance.

## 3. Syntax

```python
def function_name(**kwargs):
    for key, value in kwargs.items():
        ...

function_name(a=1, b=2)
function_name(**my_dict)

def flexible(*args, **kwargs):
    ...
```

| Part | Meaning |
|---|---|
| `**kwargs` | Collects extra keyword arguments into a dict. |
| `**my_dict (in a call)` | Spreads a dict into keyword arguments. |
| `*args, **kwargs` | Accept anything — common in wrappers. |

## 4. Example 1 — Basic Example: Collecting keyword arguments

```python
def show_profile(name, **details):
    print("Name:", name)
    for key, value in details.items():
        print(f"  {key}: {value}")


show_profile("Asha", city="Pune", role="DevOps Engineer", years=6)
show_profile("Ravi")

extra = {"language": "Python", "level": "beginner"}
show_profile("Meera", **extra)


def everything(*args, **kwargs):
    print("args:", args)
    print("kwargs:", kwargs)


everything(1, 2, mode="fast", retries=3)
```

## 5. Example 2 — Practical Example: Configuration-driven resource creation

```python
def create_bucket(name, region="us-east-1", **tags):
    """Simulate creating an S3 bucket with any number of tags."""
    tag_text = ", ".join(f"{k}={v}" for k, v in sorted(tags.items())) or "no tags"
    return f"Bucket '{name}' in {region} [{tag_text}]"


# Config as it might be loaded from a YAML file
buckets_config = [
    {"name": "app-logs", "region": "ap-south-1", "Env": "prod", "Owner": "platform"},
    {"name": "ml-datasets", "Project": "churn-model", "Env": "dev"},
    {"name": "tmp-scratch"},
]
for config in buckets_config:
    print(create_bucket(**config))


def with_logging(func, *args, **kwargs):
    """Call any function, logging its arguments first (a simple wrapper)."""
    print(f"-> calling {func.__name__} args={args} kwargs={kwargs}")
    result = func(*args, **kwargs)
    print(f"<- {func.__name__} returned: {result}")
    return result


with_logging(create_bucket, "audit-trail", region="eu-west-1", Compliance="SOC2")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `details` is a dict containing every extra keyword argument.
- `**extra` unpacks a dict into `language="Python", level="beginner"`.
- `everything` shows `*args` (tuple) and `**kwargs` (dict) together.

**Example 2**
- Each config dict is unpacked with `**config`: `name` and `region` match real parameters, and everything else lands in `**tags`.
- This "config dict → function call" pattern is how tools apply YAML settings to code.
- `with_logging` forwards whatever it receives to another function — the idea behind **decorators** used by Flask, FastAPI and pytest.

## 7. Expected Output

**Example 1:**

```text
Name: Asha
  city: Pune
  role: DevOps Engineer
  years: 6
Name: Ravi
Name: Meera
  language: Python
  level: beginner
args: (1, 2)
kwargs: {'mode': 'fast', 'retries': 3}
```

**Example 2:**

```text
Bucket 'app-logs' in ap-south-1 [Env=prod, Owner=platform]
Bucket 'ml-datasets' in us-east-1 [Env=dev, Project=churn-model]
Bucket 'tmp-scratch' in us-east-1 [no tags]
-> calling create_bucket args=('audit-trail',) kwargs={'region': 'eu-west-1', 'Compliance': 'SOC2'}
<- create_bucket returned: Bucket 'audit-trail' in eu-west-1 [Compliance=SOC2]
```

## 8. Common Mistakes

**1. Unpacking keys that don't match**

`create_bucket(**{"nme": "x"})` → `TypeError: missing required argument 'name'` (typo in key).

**2. Non-string keys**

`f(**{1: "a"})` fails — keyword names must be strings.

**3. Hiding mistakes with **kwargs**

Accepting `**kwargs` means typos like `regoin=` are silently accepted. Validate keys when it matters.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Print settings:** Write `print_settings(**settings)` that prints each setting sorted by key as `KEY = value` (key in upper case).
- **Task 2 (Medium) — Build a connection string:** Write `connection_string(driver, **params)` that returns `driver://user:password@host:port/db` using values from `params` with defaults host=localhost, port=5432. Call it by unpacking a dict.
- **Task 3 (Practical Challenge) — Kubernetes label selector:** Write `kubectl_get(resource, *names, namespace="default", **labels)`. It returns a kubectl command with names and a `-l key=value,key2=value2` selector when labels are given. Test 3 different calls.

## 10. DevOps/MLOps Connection

- **DevOps:** loading YAML/JSON config into dicts and passing them with `**config` keeps scripts configurable without code changes.
- **Cloud:** boto3 calls are often built as dicts (`params = {...}`) and then called with `client.run_instances(**params)`.
- **MLOps:** hyper-parameters stored in a config file are passed straight to a model: `RandomForestClassifier(**params)`.

## 11. Interview Questions

**Q1. What type is `kwargs`?**

<details><summary>Show answer</summary>

A dict mapping parameter names (strings) to values.

</details>

**Q2. What is the correct order of parameter kinds in a signature?**

<details><summary>Show answer</summary>

Positional, defaults, `*args`, keyword-only, `**kwargs`.

</details>

**Q3. Give a practical use of `**` unpacking.**

<details><summary>Show answer</summary>

Passing a config dictionary loaded from YAML into a function or constructor, e.g. `client.create_bucket(**bucket_config)`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 42 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 041](../../04-functions/day-041/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 043 ➡](../../04-functions/day-043/README.md)
