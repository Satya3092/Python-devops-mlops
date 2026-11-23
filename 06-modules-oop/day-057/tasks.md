# Day 057 — Practice Tasks: Python Packages

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Use the package

**Problem statement:** Using `infra_tools`, generate hostnames for service `api` in `staging` with indexes 1–3 and print them.

**Input requirements:** No user input required.

**Expected behavior:** `api-staging-01` … `api-staging-03`.

**Expected output:**

```text
api-staging-01
api-staging-02
api-staging-03
```

## Task 2 — Medium: Add a module

**Problem statement:** Add a module `infra_tools/ports.py` (written by the solution) with `is_privileged(port)` (True if < 1024). Import it and test ports 22, 8080.

**Input requirements:** No user input required.

**Expected behavior:** 22 True, 8080 False.

**Expected output:**

```text
22 True
8080 False
```

## Task 3 — Practical Challenge: Requirements checker

**Problem statement:** Write `check_requirements(lines)` that takes lines like `requests==2.32.3`, ignores comments/blank lines, and reports for each package whether it is installed and whether the installed version matches the pinned one (use `importlib.metadata`). Test it with a small list including a package that is not installed.

**Input requirements:** No user input required.

**Expected behavior:** A status line per package (OK / version mismatch / missing).

**Expected output:**

```text
pip                    version mismatch (installed 26.2.1.post1)
definitely-not-installed-pkg MISSING (wanted 1.0)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
