# Day 063 — Object-Oriented Programming Introduction

[⬅ Day 062](../../06-modules-oop/day-062/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 064 ➡](../../06-modules-oop/day-064/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain classes, objects, attributes and methods in plain English
- Understand why OOP helps organise larger programs
- Recognise that you have been using objects since Day 1

## 2. Topic Explanation

**Object-Oriented Programming (OOP)** organises code around **objects** — bundles of **data** (attributes) and **behaviour** (methods).

- A **class** is a **blueprint**. Example: the *idea* of a server.
- An **object** (or *instance*) is one thing built from the blueprint: `web-01`, `db-01`.
- **Attributes** are the object's data: `name`, `ip`, `cpu_usage`.
- **Methods** are functions that belong to the object: `restart()`, `is_healthy()`.

Analogy: a **Dockerfile is a class**, and each **running container is an object**. One Dockerfile, many containers — each with its own state (its own memory, its own logs), but all built the same way.

You have used objects all along:
- `"web-01".upper()` → `upper` is a method of the `str` object.
- `servers.append(...)` → method of a `list` object.
- `Path("x").exists()` → method of a `Path` object.

Why OOP?
- **Grouping:** data and the functions that work on it live together.
- **Reuse:** many objects from one class; new classes can extend existing ones (inheritance, Day 65).
- **Modelling:** real systems (servers, pipelines, models) map naturally to classes.
- **Libraries:** scikit-learn models, boto3 clients and FastAPI apps are all objects.

The four pillars you'll meet: **encapsulation**, **abstraction**, **inheritance**, **polymorphism**.

## 3. Syntax

```python
class ClassName:                 # PascalCase
    def method(self):            # self = this particular object
        ...

obj = ClassName()                # create an object (instance)
obj.attribute = "value"          # attribute
obj.method()                     # call a method
```

| Part | Meaning |
|---|---|
| `class` | Keyword that defines a blueprint. |
| `ClassName` | PascalCase name. |
| `self` | First parameter of methods: the object the method is called on. |
| `ClassName()` | Calling the class creates a new object. |
| `obj.method()` | Calls the method on that object. |

## 4. Example 1 — Basic Example: Everything is an object

```python
text = "web-01"
numbers = [3, 1, 2]
config = {"env": "prod"}

print(type(text), "->", text.upper())          # method of str
numbers.sort()                                  # method of list
print(type(numbers), "->", numbers)
print(type(config), "->", list(config.keys()))  # method of dict
print("Is a str an object?", isinstance(text, object))
print("Some methods of str:", [m for m in dir(text) if not m.startswith("_")][:8])
```

## 5. Example 2 — Practical Example: From loose dicts and functions to a class

```python
# Without OOP: data and functions are separate
server_a = {"name": "web-01", "cpu": 45}
server_b = {"name": "web-02", "cpu": 93}


def is_overloaded(server):
    return server["cpu"] > 90


print("Dict version:", is_overloaded(server_a), is_overloaded(server_b))


# With OOP: data + behaviour live together
class Server:
    def describe(self):
        status = "OVERLOADED" if self.is_overloaded() else "ok"
        return f"{self.name} cpu={self.cpu}% -> {status}"

    def is_overloaded(self):
        return self.cpu > 90


web_01 = Server()            # an object built from the blueprint
web_01.name = "web-01"       # (tomorrow you'll set these in a constructor)
web_01.cpu = 45

web_02 = Server()
web_02.name = "web-02"
web_02.cpu = 93

for server in (web_01, web_02):
    print(server.describe())
print("Same class, different objects:", type(web_01) is type(web_02), web_01 is web_02)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `type()` shows that strings, lists and dicts are instances of classes (`str`, `list`, `dict`).
- `dir(text)` lists the methods a string object has.

**Example 2**
- The dict version needs separate functions that receive the data.
- The `Server` class bundles data (`name`, `cpu`) and behaviour (`describe`, `is_overloaded`).
- `self` refers to the object the method was called on: `web_02.describe()` makes `self` be `web_02`.
- Two objects share one class but hold different data. Setting attributes one by one is clumsy — tomorrow's `__init__` constructor fixes that.

## 7. Expected Output

**Example 1:**

```text
<class 'str'> -> WEB-01
<class 'list'> -> [1, 2, 3]
<class 'dict'> -> ['env']
Is a str an object? True
Some methods of str: ['capitalize', 'casefold', 'center', 'count', 'encode', 'endswith', 'expandtabs', 'find']
```

**Example 2:**

```text
Dict version: False True
web-01 cpu=45% -> ok
web-02 cpu=93% -> OVERLOADED
Same class, different objects: True False
```

## 8. Common Mistakes

**1. Forgetting `self`**

`def describe():` inside a class fails when called on an object: `TypeError: takes 0 positional arguments but 1 was given`.

**2. Confusing class and object**

`Server.describe()` (on the class) fails; call methods on an instance: `web_01.describe()`.

**3. Using OOP for everything**

A 20-line script doesn't need classes. Use them when you have state + behaviour that belong together.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Explore objects:** For the values `42`, `3.14`, `"hi"`, `[1]`, `(1,)`, `{"a": 1}` print the class name and the number of public methods (names not starting with `_`).
- **Task 2 (Medium) — A Dog class:** Create a class `Dog` with a method `bark(self)` that returns `"<name> says woof"`. Create two dogs, set their `name` attributes and call `bark`.
- **Task 3 (Practical Challenge) — Model a container:** Create a class `Container` with methods `start()`, `stop()` and `status()` that change/read a `state` attribute (`created` → `running` → `exited`). Create two containers from the same class, operate them differently and print their statuses to show each object keeps its own state.

## 10. DevOps/MLOps Connection

- **DevOps:** tools like Ansible, Fabric, Pulumi and the Kubernetes Python client expose objects (`Host`, `Deployment`, `Stack`).
- **Cloud:** `boto3.client("s3")` returns an object whose methods are API calls.
- **ML/MLOps:** every scikit-learn model is an object with `fit()` and `predict()` methods; FastAPI apps and Pydantic request models are classes. Understanding OOP makes these libraries click.

## 11. Interview Questions

**Q1. What is the difference between a class and an object?**

<details><summary>Show answer</summary>

A class is a blueprint/type; an object is a specific instance created from it with its own state.

</details>

**Q2. What is `self`?**

<details><summary>Show answer</summary>

A reference to the current instance; Python passes it automatically as the first argument of instance methods.

</details>

**Q3. Name the four pillars of OOP.**

<details><summary>Show answer</summary>

Encapsulation, abstraction, inheritance and polymorphism.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 63 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 062](../../06-modules-oop/day-062/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 064 ➡](../../06-modules-oop/day-064/README.md)
