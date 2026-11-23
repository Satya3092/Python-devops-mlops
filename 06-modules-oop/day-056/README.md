# Day 056 — Modules and Imports

[⬅ Day 055](../../05-files-exceptions/day-055/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 057 ➡](../../06-modules-oop/day-057/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Import standard-library modules (`import`, `from ... import`, `as`)
- Create your own module and import it
- Understand `if __name__ == "__main__":`

## 2. Topic Explanation

A **module** is simply a `.py` file containing functions, classes and variables. **Importing** a module lets you reuse its code.

Python ships with a huge **standard library** ("batteries included"): `os`, `sys`, `json`, `csv`, `datetime`, `math`, `random`, `subprocess`, `logging`... no installation needed.

Import styles:

| Style | Use as |
|---|---|
| `import math` | `math.sqrt(16)` |
| `from math import sqrt` | `sqrt(16)` |
| `import datetime as dt` | `dt.date.today()` (alias) |
| `from os import path, getcwd` | several names |

Avoid `from module import *` — it hides where names come from.

**Your own modules:** put functions in `devops_utils.py` and in another file in the same folder write `import devops_utils`. Python finds modules in the script's folder, then the standard library, then installed packages (`sys.path`).

`if __name__ == "__main__":` — when a file is **run directly**, `__name__` is `"__main__"`; when it is **imported**, `__name__` is the module name. Code under this guard runs only when executed directly — perfect for tests or a CLI entry point.

PEP 8 import order: standard library, then third-party, then your own modules — each group separated by a blank line.

## 3. Syntax

```python
import module_name
from module_name import name1, name2
import long_module_name as alias

if __name__ == "__main__":
    main()
```

| Part | Meaning |
|---|---|
| `import x` | Loads module x; access members with `x.name`. |
| `from x import y` | Imports a specific name into your file. |
| `as alias` | Gives a shorter name. |
| `__name__` | `"__main__"` when run directly, module name when imported. |

## 4. Example 1 — Basic Example: Using the standard library

```python
import math
import random
from datetime import date, timedelta
import platform as pf

print("sqrt(144) =", math.sqrt(144))
print("ceil(7.2) =", math.ceil(7.2))
print("pi =", round(math.pi, 4))

random.seed(42)                     # fixed seed -> same "random" numbers every run
print("Random port:", random.randint(30000, 32767))
print("Random choice:", random.choice(["web-01", "web-02", "web-03"]))

release = date(2026, 11, 20)
print("Release date + 14 days:", release + timedelta(days=14))
print("Running on:", pf.system())
```

## 5. Example 2 — Practical Example: Importing your own module

```python
import devops_utils
from devops_utils import percent, status

print("Module name:", devops_utils.__name__)
print("Default threshold:", devops_utils.DEFAULT_THRESHOLD)

disks = {"/": (41, 50), "/var": (19, 20), "/data": (120, 500)}
for mount, (used, total) in disks.items():
    usage = percent(used, total)
    print(f"{mount:<6} {usage:>5}% {status(usage)}")

print("Docstring:", percent.__doc__)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `math`, `random`, `datetime` and `platform` are standard-library modules.
- `from datetime import date, timedelta` imports two names directly.
- `import platform as pf` creates an alias.
- `random.seed(42)` makes random results reproducible — essential for ML experiments later.

**Example 2**
- `devops_utils.py` sits in the same folder, so `import devops_utils` finds it.
- When imported, its `if __name__ == "__main__":` block does **not** run (no "Self-test" line). Run `python devops_utils.py` directly to see it.
- Both `devops_utils.percent` and the directly imported `percent` refer to the same function.

## 7. Expected Output

**Example 1:**

```text
sqrt(144) = 12.0
ceil(7.2) = 8
pi = 3.1416
Random port: 32619
Random choice: web-01
Release date + 14 days: 2026-12-04
Running on: Linux
```

**Example 2:**

```text
Module name: devops_utils
Default threshold: 80
/       82.0% ALERT
/var    95.0% ALERT
/data   24.0% OK
Docstring: Return used/total as a percentage rounded to 1 decimal.
```

> ℹ️ `Running on:` shows your operating system.

## 8. Common Mistakes

**1. Naming your file like a module**

A file called `random.py` or `json.py` in your folder shadows the standard library and breaks imports. Use unique names.

**2. Circular imports**

If `a.py` imports `b.py` and `b.py` imports `a.py`, you get import errors. Move shared code to a third module.

**3. `from x import *`**

Pollutes your namespace and hides where names come from. Import explicitly.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Math helpers:** Use `math` to print the square root of 2 (4 decimals), `math.floor(9.99)`, and `math.factorial(5)`.
- **Task 2 (Medium) — Your first module:** Create `string_tools.py` (in the solution this file is written for you) with `slugify(text)` and `shorten(text, n)`. Import it and use both functions.
- **Task 3 (Practical Challenge) — Unit converter module with self-test:** Create `units.py` with `bytes_to_human(n)` that returns strings like `1.5 GB`, plus a `__main__` self-test. Import it and print sizes for 512, 2048, 5_000_000 and 7_500_000_000 bytes. Then run the module directly with `subprocess` (preview of Day 61) to show the self-test output.

## 10. DevOps/MLOps Connection

- **DevOps:** split big scripts into reusable modules (`aws_helpers.py`, `notify.py`) shared across many automation jobs.
- **Cloud/Ansible:** Ansible modules and boto3 are just Python modules you import.
- **MLOps:** separate `data.py`, `train.py`, `serve.py` modules; the FastAPI app imports the same preprocessing module used in training so they never drift apart.

## 11. Interview Questions

**Q1. What is the difference between a module and a package?**

<details><summary>Show answer</summary>

A module is a single .py file; a package is a directory of modules (usually with `__init__.py`).

</details>

**Q2. What does `if __name__ == "__main__":` do?**

<details><summary>Show answer</summary>

Runs the block only when the file is executed directly, not when it is imported.

</details>

**Q3. How does Python find modules to import?**

<details><summary>Show answer</summary>

It searches the directories in `sys.path`: the script's directory, PYTHONPATH, the standard library and site-packages.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 56 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 055](../../05-files-exceptions/day-055/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 057 ➡](../../06-modules-oop/day-057/README.md)
