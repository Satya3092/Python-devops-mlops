# Day 063 — Practice Tasks: Object-Oriented Programming Introduction

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Explore objects

**Problem statement:** For the values `42`, `3.14`, `"hi"`, `[1]`, `(1,)`, `{"a": 1}` print the class name and the number of public methods (names not starting with `_`).

**Input requirements:** No user input required.

**Expected behavior:** Six lines with class names and method counts.

**Expected output:**

```text
int    11 public methods
float  7 public methods
str    47 public methods
list   11 public methods
tuple  2 public methods
dict   11 public methods
```

## Task 2 — Medium: A Dog class

**Problem statement:** Create a class `Dog` with a method `bark(self)` that returns `"<name> says woof"`. Create two dogs, set their `name` attributes and call `bark`.

**Input requirements:** No user input required.

**Expected behavior:** Two bark messages.

**Expected output:**

```text
Rex says woof
Bella says woof
```

## Task 3 — Practical Challenge: Model a container

**Problem statement:** Create a class `Container` with methods `start()`, `stop()` and `status()` that change/read a `state` attribute (`created` → `running` → `exited`). Create two containers from the same class, operate them differently and print their statuses to show each object keeps its own state.

**Input requirements:** No user input required.

**Expected behavior:** Two containers with different states.

**Expected output:**

```text
web: created | worker: created
web: running | worker: exited
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
