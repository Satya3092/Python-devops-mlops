# Day 045 — Functions Revision and Mini Project

[⬅ Day 044](../../04-functions/day-044/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 046 ➡](../../05-files-exceptions/day-046/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 90–120 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Revise all function concepts from Days 36–44
- Design a small program as a set of single-purpose functions
- Build the mini project: **Command-line Calculator** (seed of Project 2)

## 2. Topic Explanation

**Revision cheat-sheet**

| Concept | Example |
|---|---|
| Define / call | `def f(): ...` → `f()` |
| Parameters | `def f(a, b)` |
| Return | `return a + b` |
| Defaults | `def f(a, b=2)` |
| Keyword args | `f(b=3, a=1)` |
| Keyword-only | `def f(a, *, force=False)` |
| `*args` | tuple of extra positionals |
| `**kwargs` | dict of extra keywords |
| Scope | local vs global, LEGB |
| Lambda | `key=lambda x: x[1]` |

**Design principle:** each function does **one** thing, takes inputs as parameters and returns outputs. Input/output (asking the user, printing) lives at the edges — usually in `main()`.

**Mini project: Calculator**
- `add`, `subtract`, `multiply`, `divide`, `power` — pure functions.
- A **dispatch dictionary** maps operator symbols to functions: `OPERATIONS["+"](2, 3)`. Functions are values in Python — you can store them in dicts!
- `calculate(a, op, b)` validates input and returns a result or an error message.
- `main()` processes a list of expressions (or user input).

The full version with a menu and exception handling lives in [Project 2](../../projects/02-python-calculator/).

## 3. Syntax

```python
OPERATIONS = {"+": add, "-": subtract}    # functions stored in a dict
result = OPERATIONS[symbol](a, b)          # look up and call
```

| Part | Meaning |
|---|---|
| `function as value` | Functions can be stored in variables, lists and dicts. |
| `dispatch dict` | Maps a key to the function that handles it. |
| `OPERATIONS[symbol](a, b)` | Look up the function, then call it. |

## 4. Example 1 — Basic Example: Functions are values

```python
def shout(text):
    return text.upper() + "!"


def whisper(text):
    return text.lower() + "..."


styles = {"loud": shout, "quiet": whisper}
for name, func in styles.items():
    print(f"{name:<6}-> {func('Deploy complete')}")

pipeline = [str.strip, str.lower, lambda s: s.replace(" ", "-")]
value = "  Payment Service  "
for step in pipeline:
    value = step(value)
print("Slug:", value)
```

## 5. Example 2 — Practical Example: Mini project — Calculator with a dispatch table

```python
def add(a, b):
    return a + b


def subtract(a, b):
    return a - b


def multiply(a, b):
    return a * b


def divide(a, b):
    if b == 0:
        return None                 # signal "cannot compute"
    return a / b


def power(a, b):
    return a ** b


OPERATIONS = {"+": add, "-": subtract, "*": multiply, "/": divide, "**": power}


def parse_number(text):
    """Return a float, or None if the text is not a number."""
    text = text.strip()
    if text.replace(".", "", 1).lstrip("-").isdigit():
        return float(text)
    return None


def calculate(expression):
    """Evaluate 'a op b' and return (ok, result_or_message)."""
    parts = expression.split()
    if len(parts) != 3:
        return False, "use the format: number operator number"
    a, op, b = parse_number(parts[0]), parts[1], parse_number(parts[2])
    if a is None or b is None:
        return False, "operands must be numbers"
    if op not in OPERATIONS:
        return False, f"unknown operator '{op}' (use {' '.join(OPERATIONS)})"
    result = OPERATIONS[op](a, b)
    if result is None:
        return False, "division by zero"
    return True, round(result, 4)


def main():
    expressions = ["12 + 30", "7 / 2", "2 ** 10", "5 / 0", "9 % 2", "ten * 3", "4 *"]
    for expression in expressions:
        ok, value = calculate(expression)
        label = "=" if ok else "error:"
        print(f"{expression:<10} {label} {value}")


main()
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Functions are stored in a dict and called through it: `func('...')`.
- `pipeline` is a list of functions (including methods `str.strip` and a lambda) applied one after another — a mini data-processing pipeline.

**Example 2 (mini project)**
- Five pure math functions; `divide` returns `None` for division by zero instead of crashing.
- `OPERATIONS` maps symbols to functions — no long `if/elif` chain needed. Adding a new operator = one new dict entry.
- `parse_number` validates text before converting (Day 52 will show a cleaner way with try/except).
- `calculate` returns a tuple `(ok, value)` so the caller can decide how to display success or failure.
- `main` contains the only `print` statements — everything else is testable.

## 7. Expected Output

**Example 1:**

```text
loud  -> DEPLOY COMPLETE!
quiet -> deploy complete...
Slug: payment-service
```

**Example 2:**

```text
12 + 30    = 42.0
7 / 2      = 3.5
2 ** 10    = 1024.0
5 / 0      error: division by zero
9 % 2      error: unknown operator '%' (use + - * / **)
ten * 3    error: operands must be numbers
4 *        error: use the format: number operator number
```

## 8. Common Mistakes

**1. Calling the function when storing it**

`{"+": add()}` calls `add` immediately (and fails). Store the function itself: `{"+": add}`.

**2. Mixing I/O with logic**

Functions that both calculate and print are hard to reuse. Return values; print in `main`.

**3. Inconsistent return types**

Returning a number sometimes and a message string other times confuses callers. Use a clear contract like `(ok, value)` or raise exceptions.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Temperature converter module:** Write `c_to_f`, `f_to_c`, `c_to_k` functions and a dispatch dict keyed by `"c->f"`, `"f->c"`, `"c->k"`. Convert 100 using each.
- **Task 2 (Medium) — Statistics helper:** Write `stats(*values, precision=2)` returning a dict with count, min, max, mean and median. Use it on response times `[120, 87, 450, 134, 98, 101]`.
- **Task 3 (Practical Challenge) — Extend the calculator:** Add `%` (modulo) and `//` (floor division) to the mini project, make both safe for zero, and add a `history` list (passed in as a parameter, not global) that stores every successful calculation as a string. Print the history at the end.

## 10. DevOps/MLOps Connection

- **DevOps:** dispatch dictionaries power CLI tools (`tool start|stop|status` → function per command) and ChatOps bots.
- **Cloud:** Lambda routers map API paths to handler functions in exactly the same way.
- **MLOps:** a pipeline is a list of functions (preprocessing steps) applied in order — the idea behind scikit-learn `Pipeline` (Day 100).

## 11. Interview Questions

**Q1. What does it mean that functions are 'first-class objects' in Python?**

<details><summary>Show answer</summary>

Functions can be assigned to variables, stored in data structures, passed as arguments and returned from other functions.

</details>

**Q2. What is a dispatch table and why use it?**

<details><summary>Show answer</summary>

A dict mapping keys to functions; it replaces long if/elif chains and makes adding new cases trivial.

</details>

**Q3. How do you make a function easy to unit test?**

<details><summary>Show answer</summary>

Keep it pure: take inputs as parameters, return outputs, avoid global state and I/O inside.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 45 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 044](../../04-functions/day-044/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 046 ➡](../../05-files-exceptions/day-046/README.md)
