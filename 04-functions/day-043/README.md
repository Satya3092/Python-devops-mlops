# Day 043 — Scope and Local/Global Variables

[⬅ Day 042](../../04-functions/day-042/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 044 ➡](../../04-functions/day-044/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain local, enclosing, global and built-in scope (LEGB)
- Understand why variables created inside functions disappear afterwards
- Use `global` (sparingly) and prefer passing values in and returning them out

## 2. Topic Explanation

**Scope** is *where* a variable name is visible.

- **Local:** created inside a function; exists only while the function runs.
- **Enclosing:** variables of an outer function (when functions are nested).
- **Global:** created at the top level of a file (module).
- **Built-in:** names Python provides (`print`, `len`).

Python looks names up in this order: **L → E → G → B** (the *LEGB rule*).

Analogy: a function is a hotel room. Things you create in the room (local variables) stay in the room when you check out. You can see the hotel lobby (globals) from your room, but you shouldn't rearrange the lobby furniture without permission (`global`).

- Reading a global inside a function works.
- **Assigning** to a name inside a function makes it local — unless you declare `global name`.
- Using `global` makes code hard to test and reason about. Prefer **parameters in, return values out**.
- Global **constants** (UPPER_CASE, never reassigned) are perfectly fine.

## 3. Syntax

```python
GLOBAL_CONSTANT = 10          # global

def function_name():
    local_var = 5             # local
    print(GLOBAL_CONSTANT)    # reading a global is OK

def change_global():
    global counter            # needed to assign to a global
    counter += 1
```

| Part | Meaning |
|---|---|
| `local variable` | Assigned inside a function; invisible outside. |
| `global variable` | Assigned at module level; readable everywhere. |
| `global name` | Allows a function to rebind a global name. |
| `nonlocal name` | Allows a nested function to rebind an enclosing variable. |

## 4. Example 1 — Basic Example: Local vs global

```python
message = "I am global"


def show():
    local_message = "I am local"
    print(local_message)
    print(message)              # reading a global works


show()
try:
    print(local_message)
except NameError as error:
    print("NameError:", error)


def shadow():
    message = "I am a local with the same name"   # new local, global untouched
    print(message)


shadow()
print(message)
```

## 5. Example 2 — Practical Example: Global counters vs returning values

```python
# Version 1: global state (works, but harder to test)
errors_seen = 0


def scan_line_global(line):
    global errors_seen
    if "ERROR" in line:
        errors_seen += 1


for line in ["INFO ok", "ERROR db", "ERROR disk"]:
    scan_line_global(line)
print("Global counter:", errors_seen)


# Version 2: pure function - input in, result out (preferred)
def count_errors(lines):
    count = 0                       # local
    for line in lines:
        if "ERROR" in line:
            count += 1
    return count


print("Returned count:", count_errors(["INFO ok", "ERROR db", "ERROR disk"]))


# Enclosing scope with nonlocal: a counter factory
def make_counter():
    total = 0

    def increment(step=1):
        nonlocal total
        total += step
        return total

    return increment


request_counter = make_counter()
request_counter()
request_counter()
print("Requests counted:", request_counter(5))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `local_message` only exists inside `show()`; printing it outside raises `NameError`.
- `shadow()` assigns `message`, creating a **new local** variable; the global stays unchanged.

**Example 2**
- Version 1 needs `global errors_seen` to modify the counter. Any function could change it — hard to track.
- Version 2 is a **pure function**: same input → same output, no hidden state. Easy to test.
- `make_counter` returns an inner function that remembers `total` from the enclosing scope (a *closure*). `nonlocal` lets it update that variable.

## 7. Expected Output

**Example 1:**

```text
I am local
I am global
NameError: name 'local_message' is not defined
I am a local with the same name
I am global
```

**Example 2:**

```text
Global counter: 2
Returned count: 2
Requests counted: 7
```

## 8. Common Mistakes

**1. `UnboundLocalError`**

`count = 0; def f(): count += 1` fails because assigning makes `count` local, and it has no value yet. Pass it as a parameter or (rarely) use `global`.

**2. Overusing `global`**

Global mutable state makes bugs hard to find and tests unreliable. Return values instead.

**3. Shadowing built-ins**

`list = [1, 2]` or `sum = 0` hides the built-in function. Then `list(...)` fails later. Choose other names.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Predict the output:** Without running it, predict what this prints, then verify: `x = 10`, `def f(): x = 20; print(x)`, call `f()`, then `print(x)`.
- **Task 2 (Medium) — Fix the UnboundLocalError:** This code fails: `deployments = 0` / `def deploy(): deployments += 1`. Fix it twice: once with `global`, once properly by passing the value in and returning the new value.
- **Task 3 (Practical Challenge) — Config with constants:** Define global constants `DEFAULT_REGION` and `ALLOWED_ENVS`. Write a pure function `build_config(env, region=None)` that validates `env` against `ALLOWED_ENVS`, uses `DEFAULT_REGION` if no region is given, and returns a dict — or raises `ValueError` for bad input. Show a success and a failure.

## 10. DevOps/MLOps Connection

- **DevOps:** global mutable state in long-running scripts or Lambda functions causes hard-to-reproduce bugs (Lambda re-uses globals between invocations!).
- **Cloud:** creating a boto3 client *globally* in Lambda is a deliberate exception: it is reused across invocations for speed.
- **MLOps:** pure, deterministic functions make pipelines reproducible — same data + same parameters = same model.

## 11. Interview Questions

**Q1. Explain the LEGB rule.**

<details><summary>Show answer</summary>

Python resolves names by searching Local, then Enclosing function scopes, then Global (module), then Built-in.

</details>

**Q2. What causes `UnboundLocalError`?**

<details><summary>Show answer</summary>

Assigning to a name inside a function makes it local for the whole function; reading it before assignment raises the error.

</details>

**Q3. What is the difference between `global` and `nonlocal`?**

<details><summary>Show answer</summary>

`global` binds to a module-level name; `nonlocal` binds to a name in the nearest enclosing function scope.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 43 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 042](../../04-functions/day-042/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 044 ➡](../../04-functions/day-044/README.md)
