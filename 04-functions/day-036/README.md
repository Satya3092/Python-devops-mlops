# Day 036 — Introduction to Functions

[⬅ Day 035](../../03-dictionaries-logic/day-035/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 037 ➡](../../04-functions/day-037/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 4 — Functions and Modular Programming | 🟡 Beginner+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain why functions exist (reuse, readability, testing)
- Define a function with `def` and call it
- Write docstrings and follow function naming conventions

## 2. Topic Explanation

A **function** is a named block of code that performs one job. You **define** it once and **call** it as many times as you like.

```python
def greet():
    print("Hello!")

greet()   # call
greet()   # call again
```

Why functions matter:
- **DRY** (Don't Repeat Yourself): on Day 15 you copy-pasted the same `if/elif/else` three times. A function writes it once.
- **Readability:** `check_disk_usage()` explains itself.
- **Testing:** small functions are easy to test (CI unit tests).
- **Reuse:** put functions in a module and import them anywhere (Day 56).

Analogy: a function is a **recipe card**. Writing the card (`def`) doesn't cook anything. Cooking happens when someone follows the card (calling it).

Conventions: names in `snake_case`, starting with a verb (`get_`, `check_`, `create_`). The first line inside can be a **docstring** — a triple-quoted description shown by `help()`.

Bash equivalent: `greet() { echo "Hello"; }` then `greet`.

## 3. Syntax

```python
def function_name():
    """Short description of what the function does."""
    statement_1
    statement_2

function_name()      # call it
```

| Part | Meaning |
|---|---|
| `def` | Keyword to define a function. |
| `function_name` | snake_case, usually a verb. |
| `()` | Parameter list (empty for now — Day 37). |
| `docstring` | Triple-quoted text describing the function. |
| `function_name()` | Calling the function runs its body. |

## 4. Example 1 — Basic Example: Defining and calling a function

```python
def print_banner():
    """Print a decorative banner."""
    print("=" * 30)
    print("   100 Days of Python")
    print("=" * 30)


print("Before calling")
print_banner()
print_banner()
print("Docstring:", print_banner.__doc__)
```

## 5. Example 2 — Practical Example: Refactoring a script into functions

```python
import platform
import datetime


def show_header():
    """Print the report header with the current date."""
    today = datetime.date(2026, 11, 20)        # fixed date so the output is stable
    print(f"Server report - {today}")
    print("-" * 32)


def show_system_info():
    """Print basic information about the machine running the script."""
    print("Python version  :", platform.python_version()[:4])
    print("Operating system:", platform.system())


def show_footer():
    """Print the closing line."""
    print("-" * 32)
    print("End of report")


def main():
    """Run the whole report: every step is one function call."""
    show_header()
    show_system_info()
    show_footer()


main()
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `def print_banner():` defines the function but prints nothing yet.
- The body runs each time we write `print_banner()`.
- `print_banner.__doc__` reads the docstring.

**Example 2**
- `import platform` / `import datetime` load standard-library modules (Day 56).
- The script is split into small functions, each with one job.
- `main()` orchestrates them — reading `main` tells you what the program does without reading every detail. This structure is standard for real automation scripts.

## 7. Expected Output

**Example 1:**

```text
Before calling
==============================
   100 Days of Python
==============================
==============================
   100 Days of Python
==============================
Docstring: Print a decorative banner.
```

**Example 2:**

```text
Server report - 2026-11-20
--------------------------------
Python version  : 3.13
Operating system: Linux
--------------------------------
End of report
```

> ℹ️ Your Python version and operating system lines will show your own machine's values.

## 8. Common Mistakes

**1. Calling before defining**

Python reads top to bottom. Calling `greet()` above `def greet():` raises `NameError`.

**2. Forgetting the parentheses**

`print_banner` (no `()`) refers to the function object and does nothing. Use `print_banner()`.

**3. Functions doing too much**

A 200-line function is hard to test. Aim for one responsibility per function.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Say hello:** Write a function `say_hello()` that prints three lines introducing the course, and call it twice.
- **Task 2 (Medium) — Separator helper:** Write `print_separator()` that prints 40 dashes. Use it to separate three sections (Linux, Docker, Kubernetes) where each section prints one fact.
- **Task 3 (Practical Challenge) — Refactor a deployment script:** Turn this flat script into functions `pull_code()`, `run_tests()`, `build_image()`, `deploy()` and a `main()` that calls them in order. Each function prints what it does, e.g. `[1/4] Pulling latest code from main`. Add a docstring to each function.

## 10. DevOps/MLOps Connection

- **DevOps:** every maintainable automation script is a set of small functions plus a `main()`. Ansible modules, Jenkins shared libraries and Lambda handlers are all functions.
- **Cloud:** an AWS Lambda is literally one function `def lambda_handler(event, context):`.
- **MLOps:** pipelines are chains of functions: `load_data() → preprocess() → train() → evaluate() → save_model()` (Day 100).

## 11. Interview Questions

**Q1. What is a function and why use one?**

<details><summary>Show answer</summary>

A reusable, named block of code. Functions reduce duplication, improve readability, and make code testable.

</details>

**Q2. What is a docstring?**

<details><summary>Show answer</summary>

A string literal as the first statement of a function/class/module that documents it; accessible via `help()` or `__doc__`.

</details>

**Q3. What does `if __name__ == "__main__":` do?**

<details><summary>Show answer</summary>

Runs code only when the file is executed directly, not when imported as a module (covered on Day 56).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 36 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 035](../../03-dictionaries-logic/day-035/README.md) | [📚 Phase 4: Functions and Modular Programming](../README.md) | [🏠 Home](../../README.md) | [Day 037 ➡](../../04-functions/day-037/README.md)
