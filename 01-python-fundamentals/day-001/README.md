# Day 001 — Introduction to Python, Installation, IDE, First Program

[📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 002 ➡](../../01-python-fundamentals/day-002/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Explain what Python is and why DevOps and MLOps engineers use it
- Install Python 3 and VS Code on Windows or Ubuntu
- Run Python in the interactive shell (REPL) and from a `.py` file
- Write your first program with `print()` and add comments

## 2. Topic Explanation

**Python** is a programming language: a way to give a computer step-by-step instructions using words that look a lot like English. It is popular because it is easy to read, has a huge library of ready-made tools, and runs everywhere (Linux, Windows, macOS, containers, AWS Lambda...).

You already write **shell scripts**. Think of Python as a "super shell script": it can do everything Bash does, but it also handles JSON, APIs, error handling, data analysis and machine learning far more cleanly.

How Python runs your code:

1. You write instructions in a text file ending in `.py` (for example `hello.py`).
2. The **Python interpreter** (the program called `python` / `python3`) reads the file **top to bottom**, one line at a time.
3. Each line is executed immediately. There is no separate compile step.

Two ways to run Python:

- **REPL** (Read–Eval–Print Loop): type `python3` in a terminal and you get a `>>>` prompt. Great for quick experiments.
- **Script**: save code in a file and run `python3 hello.py`. This is how real automation runs (cron jobs, CI pipelines, containers).

An **IDE/editor** such as **VS Code** gives you colours, auto-complete and a Run button. Installation steps for Windows and Ubuntu are in [`00-python-setup`](../../00-python-setup/README.md).

`print()` is a **function** — a named, reusable action. You "call" it with parentheses and give it something to show. A **comment** starts with `#`; Python ignores it. Comments are notes for humans.

## 3. Syntax

```python
# This is a comment - Python ignores it
print("text to display")
print("value 1", "value 2")   # several values are separated by a space
```

| Part | Meaning |
|---|---|
| `#` | Starts a comment. Everything after it on the line is ignored by Python. |
| `print` | Built-in function that writes text to the screen (standard output). |
| `( )` | Parentheses call the function and hold its inputs (called *arguments*). |
| `"text"` | A string: text wrapped in single `'` or double `"` quotes. |
| `,` | Separates multiple arguments; `print` puts a space between them. |

## 4. Example 1 — Basic Example: Hello, World!

```python
# My first Python program
print("Hello, World!")
print("I am learning Python for DevOps and MLOps.")
print("Day", 1, "of", 100)
```

## 5. Example 2 — Practical Example: A deployment banner

```python
# A banner like the ones CI/CD pipelines print in their logs
print("=" * 40)                  # "=" repeated 40 times
print("  Deploying: payment-service")
print("  Environment: staging")
print("  Version: 1.0.0")
print("=" * 40)
print("Step 1/3: Pulling Docker image")
print("Step 2/3: Running health checks")
print("Step 3/3: Switching traffic")
print("Deployment finished successfully!")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `# My first Python program` — a comment; it is not executed.
- `print("Hello, World!")` — calls `print` with one string; the quotes are not shown in the output.
- `print("Day", 1, "of", 100)` — four arguments (two strings, two numbers). `print` joins them with spaces.

**Example 2**
- `"=" * 40` — multiplying a string by a number repeats it. This draws a 40-character line.
- Each `print` call ends with a newline, so every message appears on its own line — just like `echo` in Bash.
- The program runs top to bottom, so the steps appear in order.

## 7. Expected Output

**Example 1:**

```text
Hello, World!
I am learning Python for DevOps and MLOps.
Day 1 of 100
```

**Example 2:**

```text
========================================
  Deploying: payment-service
  Environment: staging
  Version: 1.0.0
========================================
Step 1/3: Pulling Docker image
Step 2/3: Running health checks
Step 3/3: Switching traffic
Deployment finished successfully!
```

## 8. Common Mistakes

**1. Forgetting the quotes around text**

`print(Hello)` fails with `NameError: name 'Hello' is not defined`. Python thinks `Hello` is a variable. Use `print("Hello")`.

**2. Using `Print` instead of `print`**

Python is **case-sensitive**. `Print` and `print` are different names. Built-in functions are lowercase.

**3. Mixing quote types**

`print("Hello')` is an error — a string must start and end with the same quote character.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Introduce yourself:** Write a program that prints your name, your current role and why you are learning Python, each on its own line.
- **Task 2 (Medium) — Server welcome banner:** Print a login banner (like `/etc/motd`) for a server named `prod-web-01` that is surrounded by lines of 30 `*` characters.
- **Task 3 (Practical Challenge) — Pipeline stage log:** Simulate the log of a CI pipeline with stages Checkout, Build, Test and Deploy. Print a header, then one line per stage in the form `[stage n/4] Name ... OK`, and a final success message.

## 10. DevOps/MLOps Connection

- **DevOps:** Python is the most common language for automation scripts, Ansible modules, and CLI tools (the AWS CLI itself is written in Python).
- **Cloud automation:** AWS Lambda, boto3 and most cloud SDKs support Python first.
- **Data engineering:** Airflow DAGs and ETL jobs are written in Python.
- **Machine Learning / MLOps:** scikit-learn, PyTorch, TensorFlow, MLflow and FastAPI are all Python. Every MLOps pipeline you build later starts with a script like today's.
- The `print` banners you wrote are exactly what you see in Jenkins or GitHub Actions logs.

## 11. Interview Questions

**Q1. What is the difference between an interpreted and a compiled language? Which one is Python?**

<details><summary>Show answer</summary>

A compiled language is translated to machine code before running (C, Go). An interpreted language is executed by an interpreter at run time. Python is interpreted (CPython compiles to bytecode internally, but you never run a separate compile step).

</details>

**Q2. How do you check which Python version is installed?**

<details><summary>Show answer</summary>

Run `python3 --version` (or `python --version` on Windows). Inside Python: `import sys; print(sys.version)`.

</details>

**Q3. Why is Python popular in DevOps?**

<details><summary>Show answer</summary>

It is readable, cross-platform, comes pre-installed on most Linux systems, has libraries for everything (boto3, requests, paramiko, psutil) and integrates with tools like Ansible and Airflow.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 1 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 002 ➡](../../01-python-fundamentals/day-002/README.md)
