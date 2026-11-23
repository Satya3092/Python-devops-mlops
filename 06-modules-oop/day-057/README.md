# Day 057 — Python Packages

[⬅ Day 056](../../06-modules-oop/day-056/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 058 ➡](../../06-modules-oop/day-058/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Organise modules into a package with `__init__.py`
- Use absolute and relative imports inside a package
- Install third-party packages with `pip` inside a virtual environment

## 2. Topic Explanation

A **package** is a folder of modules. A file called `__init__.py` marks the folder as a regular package and runs when the package is imported.

```
infra_tools/
├── __init__.py      # package initialisation, public API
├── network.py       # module
└── naming.py        # module
```

Imports:
- `import infra_tools.network` then `infra_tools.network.is_valid_ip(...)`
- `from infra_tools.network import is_valid_ip`
- Inside the package, **relative imports** use dots: `from .network import is_valid_ip`.
- `__init__.py` can re-export the most important functions so users can write `from infra_tools import is_valid_ip`.

**Third-party packages** come from **PyPI** (Python Package Index) and are installed with `pip`. Always install them inside a **virtual environment** so each project has its own isolated dependencies:

```bash
python3 -m venv .venv            # create
source .venv/bin/activate        # activate (Linux/macOS)
.venv\Scripts\activate           # activate (Windows)
pip install requests             # install
pip freeze > requirements.txt    # record exact versions
pip install -r requirements.txt  # reproduce on another machine / in Docker
```

Analogy: a virtual environment is like a separate Docker image for your Python libraries — projects can't break each other.

## 3. Syntax

```python
from package.module import function
from package import exported_name
from .sibling_module import name        # relative (inside a package)

python3 -m venv .venv && source .venv/bin/activate
pip install package_name==1.2.3
```

| Part | Meaning |
|---|---|
| `__init__.py` | Marks a package; runs on import; can define the public API. |
| `package.module` | Dotted path to a module inside a package. |
| `.module` | Relative import from the same package. |
| `python -m venv` | Creates an isolated environment. |
| `pip install` | Installs packages from PyPI. |

## 4. Example 1 — Basic Example: Importing from a local package

```python
import infra_tools
from infra_tools.naming import hostname
from infra_tools import is_valid_ip

print("Package version:", infra_tools.__version__)
print(hostname("orders", "prod", 1))
print(hostname("search", "dev", 12))

for ip in ["10.0.0.1", "256.1.1.1", "192.168.1", "172.16.5.20"]:
    print(f"{ip:<14} valid={is_valid_ip(ip)}")
```

## 5. Example 2 — Practical Example: Inspecting the environment and installed packages

```python
import sys
from importlib import metadata

in_venv = sys.prefix != sys.base_prefix
print("Running inside a virtual environment?", in_venv)
print("Python executable ends with:", sys.executable.split("/")[-1])

for package in ["requests", "PyYAML", "psutil", "not-a-real-package"]:
    try:
        version = metadata.version(package)
        print(f"{package:<20} installed, version {version}")
    except metadata.PackageNotFoundError:
        print(f"{package:<20} NOT installed -> pip install {package}")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `infra_tools/__init__.py` re-exports `is_valid_ip` and `hostname`, so both `from infra_tools import is_valid_ip` and the full dotted path work.
- `__version__` is a common convention for package versions.

**Example 2**
- In a venv, `sys.prefix` (the venv) differs from `sys.base_prefix` (the system Python).
- `importlib.metadata.version()` reads the version of an installed package — useful in CI checks and support scripts.
- Missing packages raise `PackageNotFoundError`, which we handle with a helpful hint.

## 7. Expected Output

**Example 1:**

```text
Package version: 0.1.0
orders-prod-01
search-dev-12
10.0.0.1       valid=True
256.1.1.1      valid=False
192.168.1      valid=False
172.16.5.20    valid=True
```

**Example 2:**

```text
Running inside a virtual environment? False
Python executable ends with: python3
requests             installed, version 2.34.2
PyYAML               installed, version 6.0.3
psutil               installed, version 7.2.2
not-a-real-package   NOT installed -> pip install not-a-real-package
```

> ℹ️ Whether you are in a virtual environment and which package versions are installed depend on your setup.

## 8. Common Mistakes

**1. Installing packages globally with sudo**

`sudo pip install` can break system tools (e.g. apt, yum). Use a virtual environment.

**2. Not pinning versions**

`requests` today and in six months may differ. Pin with `requests==2.32.3` for reproducible builds.

**3. Committing the venv**

Never commit `.venv/` to Git — commit `requirements.txt` instead. (It's in this repo's `.gitignore`.)

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Use the package:** Using `infra_tools`, generate hostnames for service `api` in `staging` with indexes 1–3 and print them.
- **Task 2 (Medium) — Add a module:** Add a module `infra_tools/ports.py` (written by the solution) with `is_privileged(port)` (True if < 1024). Import it and test ports 22, 8080.
- **Task 3 (Practical Challenge) — Requirements checker:** Write `check_requirements(lines)` that takes lines like `requests==2.32.3`, ignores comments/blank lines, and reports for each package whether it is installed and whether the installed version matches the pinned one (use `importlib.metadata`). Test it with a small list including a package that is not installed.

## 10. DevOps/MLOps Connection

- **DevOps:** package your automation as an installable Python package (`pip install .`) so every server/CI runner gets the same tools.
- **Docker:** `COPY requirements.txt` + `RUN pip install -r requirements.txt` is in almost every Python Dockerfile.
- **MLOps:** pinned dependencies are critical — a different scikit-learn version can fail to load a saved model (Day 97).

## 11. Interview Questions

**Q1. What is the purpose of `__init__.py`?**

<details><summary>Show answer</summary>

It marks a directory as a regular package and runs package initialisation code; it can define the package's public API.

</details>

**Q2. Why use virtual environments?**

<details><summary>Show answer</summary>

To isolate project dependencies, avoid version conflicts and keep the system Python clean.

</details>

**Q3. What is the difference between `pip freeze` and a hand-written requirements file?**

<details><summary>Show answer</summary>

`pip freeze` lists every installed package with exact versions (including transitive deps); a hand-written file lists direct dependencies, sometimes with ranges.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 57 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 056](../../06-modules-oop/day-056/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 058 ➡](../../06-modules-oop/day-058/README.md)
