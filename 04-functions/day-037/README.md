# Day 037 — Function Parameters and Arguments

[⬅ Day 036](../../04-functions/day-036/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 038 ➡](../../04-functions/day-038/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Pass data into functions with parameters
- Distinguish parameters (definition) from arguments (call)
- Call functions with several positional arguments

## 2. Topic Explanation

Functions become useful when they work on **different data** each time.

```python
def greet(name):          # name is a PARAMETER (a placeholder)
    print("Hello", name)

greet("Asha")             # "Asha" is an ARGUMENT (the real value)
greet("Ravi")
```

- **Parameter:** the variable name listed in the definition.
- **Argument:** the actual value passed when calling.

With several parameters, **positional arguments** are matched **by order**:
```python
def create_user(username, group):
    ...
create_user("asha", "devops")   # username="asha", group="devops"
```

Analogy: a coffee machine with slots (parameters: cup size, sugar). Each time you use it you fill the slots with real choices (arguments).

Python passes **references** to objects: if you pass a list and the function modifies it (`append`), the caller sees the change. Numbers and strings are immutable, so they cannot be changed in place.

## 3. Syntax

```python
def function_name(param1, param2):
    use(param1, param2)

function_name(arg1, arg2)
```

| Part | Meaning |
|---|---|
| `param1, param2` | Parameters: names available inside the function. |
| `arg1, arg2` | Arguments: values passed at call time. |
| `order` | Positional arguments are matched left to right. |
| `count` | Number of arguments must match (until defaults on Day 39). |

## 4. Example 1 — Basic Example: Functions with parameters

```python
def greet(name):
    print(f"Hello, {name}!")


def add(a, b):
    print(f"{a} + {b} = {a + b}")


def describe_pet(animal, name):
    print(f"I have a {animal} called {name}.")


greet("Asha")
greet("Ravi")
add(3, 4)
add(10, -2)
describe_pet("dog", "Bruno")
describe_pet("Bruno", "dog")      # wrong order -> wrong meaning!
```

## 5. Example 2 — Practical Example: Reusable checks for many servers

```python
def check_threshold(server, metric, value, limit):
    """Print an OK/ALERT line for one metric of one server."""
    status = "ALERT" if value > limit else "OK"
    print(f"{server:<8} {metric:<6} {value:>5.1f}% (limit {limit}%) -> {status}")


def tag_instance(tags, key, value):
    """Add a tag to a tags dictionary (modifies the dict in place)."""
    tags[key] = value


check_threshold("web-01", "cpu", 72.5, 80)
check_threshold("web-01", "disk", 91.0, 85)
check_threshold("db-01", "memory", 88.4, 90)

instance_tags = {"Name": "web-01"}
tag_instance(instance_tags, "Env", "prod")
tag_instance(instance_tags, "Owner", "team-web")
print("Tags after function calls:", instance_tags)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Each call fills `name`, `a`/`b` or `animal`/`name` with new values.
- The last call swaps the arguments: Python happily accepts it, but the meaning is wrong. Keyword arguments (Day 40) prevent this.

**Example 2**
- One function `check_threshold` replaces many copy-pasted `if` blocks.
- `tag_instance` receives a **reference** to the dict; adding keys inside the function changes the original `instance_tags`.

## 7. Expected Output

**Example 1:**

```text
Hello, Asha!
Hello, Ravi!
3 + 4 = 7
10 + -2 = 8
I have a dog called Bruno.
I have a Bruno called dog.
```

**Example 2:**

```text
web-01   cpu     72.5% (limit 80%) -> OK
web-01   disk    91.0% (limit 85%) -> ALERT
db-01    memory  88.4% (limit 90%) -> OK
Tags after function calls: {'Name': 'web-01', 'Env': 'prod', 'Owner': 'team-web'}
```

## 8. Common Mistakes

**1. Wrong number of arguments**

`add(1)` → `TypeError: add() missing 1 required positional argument: 'b'`.

**2. Wrong order**

Positional arguments are matched by position. Swapping them silently produces wrong results.

**3. Unexpected mutation**

Functions can modify lists/dicts you pass in. If you don't want that, pass a copy (`items.copy()`).

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Area of a rectangle:** Write `print_area(width, height)` that prints the area. Call it for 5×3 and 12×7.
- **Task 2 (Medium) — SSH command builder:** Write `print_ssh_command(user, host, port)` that prints `ssh -p <port> <user>@<host>`. Call it for three servers.
- **Task 3 (Practical Challenge) — Log line formatter:** Write `log(level, service, message)` that prints `[LEVEL] service: message` with the level upper-cased and padded to 7 characters inside the brackets. Also write `log_many(level, service, messages)` that calls `log` for each message in a list.

## 10. DevOps/MLOps Connection

- **DevOps:** parameterised functions turn one-off scripts into reusable tools: `backup_database(host, db_name)`, `restart_service(name)`.
- **Cloud:** boto3 methods are functions with parameters: `s3.upload_file(Filename, Bucket, Key)`.
- **MLOps:** `train_model(data, n_estimators, max_depth)` — parameters make experiments reproducible.

## 11. Interview Questions

**Q1. What is the difference between a parameter and an argument?**

<details><summary>Show answer</summary>

A parameter is the name in the function definition; an argument is the actual value passed when calling.

</details>

**Q2. Is Python pass-by-value or pass-by-reference?**

<details><summary>Show answer</summary>

Neither exactly — it is 'pass by object reference'. Mutable objects can be modified in place by the function; rebinding a parameter does not affect the caller.

</details>

**Q3. What error occurs if you pass too few arguments?**

<details><summary>Show answer</summary>

`TypeError: missing required positional argument`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 37 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 036](../../04-functions/day-036/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 038 ➡](../../04-functions/day-038/README.md)
