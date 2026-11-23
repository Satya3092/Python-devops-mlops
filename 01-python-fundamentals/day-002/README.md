# Day 002 — Variables and Naming Conventions

[⬅ Day 001](../../01-python-fundamentals/day-001/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 003 ➡](../../01-python-fundamentals/day-003/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 1 — Python Fundamentals | 🟢 Beginner | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Create variables and assign values to them
- Update and reuse variables
- Follow PEP 8 naming conventions (`snake_case`, `UPPER_CASE` constants)
- Know which names are not allowed

## 2. Topic Explanation

A **variable** is a name that points to a value. Think of it as a **label on a box**: the box holds the data, and the label lets you find it later.

```python
server_name = "web-01"
```

Here `server_name` is the label, `=` means "store", and `"web-01"` is the value. This is called **assignment**. Note: `=` does **not** mean "equals" as in maths — it means "put the value on the right into the name on the left".

You can change what a variable holds at any time; the newest value wins.

**Naming rules (must follow or Python errors):**
- Use letters, digits and underscores only: `max_retries`, `port2`.
- Cannot start with a digit: `2port` is invalid.
- Cannot be a Python keyword such as `if`, `for`, `class`, `import`.
- Names are case-sensitive: `Port` and `port` are different.

**Naming conventions (PEP 8 — the official style guide):**
- `snake_case` for variables: `cpu_threshold`, `docker_image`.
- `UPPER_CASE` for constants (values you do not intend to change): `MAX_RETRIES = 3`.
- Choose meaningful names: `disk_usage_percent` beats `d` or `x1`.

You already do this in Bash (`SERVER=web-01`). In Python, spaces around `=` are fine and recommended, and you do not need `$` to read a variable.

## 3. Syntax

```python
variable_name = value
CONSTANT_NAME = value
a, b = value1, value2     # assign several at once
```

| Part | Meaning |
|---|---|
| `variable_name` | The label you choose (snake_case). |
| `=` | Assignment operator: stores the right-hand value in the left-hand name. |
| `value` | Any data: text, number, True/False, list, ... |
| `CONSTANT_NAME` | Upper-case name signals 'do not change this'. Python does not enforce it — it is a convention. |
| `a, b = 1, 2` | Multiple assignment: `a` gets 1, `b` gets 2. |

## 4. Example 1 — Basic Example: Creating and updating variables

```python
course = "100 Days of Python"
day = 2
is_learning = True

print(course)
print("Today is day", day)
print("Learning?", is_learning)

# Variables can be updated - the old value is replaced
day = 3
print("Tomorrow is day", day)
```

## 5. Example 2 — Practical Example: Describing a server with variables

```python
# Constants (UPPER_CASE) - settings we do not plan to change
MAX_CPU_PERCENT = 80
DEFAULT_PORT = 8080

# Variables (snake_case) describing one server
server_name = "prod-api-01"
environment = "production"
cpu_usage = 72
open_port = DEFAULT_PORT

# Multiple assignment in a single line
region, instance_type = "us-east-1", "t3.medium"

print("Server:", server_name)
print("Environment:", environment)
print("Region:", region, "| Type:", instance_type)
print("CPU usage:", cpu_usage, "% (limit", MAX_CPU_PERCENT, "%)")
print("Listening on port", open_port)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `course = "100 Days of Python"` stores text; `day = 2` stores a whole number; `is_learning = True` stores a yes/no value.
- `print(course)` prints the **value**, not the word "course".
- `day = 3` re-assigns: the label `day` now points to `3`.

**Example 2**
- `MAX_CPU_PERCENT` and `DEFAULT_PORT` are written in upper case to signal they are configuration constants.
- `open_port = DEFAULT_PORT` copies the value of one variable into another.
- `region, instance_type = "us-east-1", "t3.medium"` assigns two variables in one line (the order matters).

## 7. Expected Output

**Example 1:**

```text
100 Days of Python
Today is day 2
Learning? True
Tomorrow is day 3
```

**Example 2:**

```text
Server: prod-api-01
Environment: production
Region: us-east-1 | Type: t3.medium
CPU usage: 72 % (limit 80 %)
Listening on port 8080
```

## 8. Common Mistakes

**1. Using a variable before assigning it**

`print(hostname)` before `hostname = ...` raises `NameError`. Python reads top to bottom, so assign first.

**2. Invalid names**

`server-name = 'x'` fails because `-` means minus. Use `server_name`. `2nd_server` fails because names cannot start with a digit.

**3. Meaningless names**

`x = 80` tells the reader nothing. `cpu_threshold = 80` documents itself. Future-you will thank you.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Personal profile:** Create variables `full_name`, `city`, `years_experience` and `favourite_tool`, then print each one with a label.
- **Task 2 (Medium) — Swap two values:** You have `primary_db = "db-01"` and `replica_db = "db-02"`. A failover happened: swap the values so the replica becomes primary. Print before and after.
- **Task 3 (Practical Challenge) — Docker run summary:** Store container settings in well-named variables (image name, tag, container name, host port, container port, restart policy). Use a constant for the registry `REGISTRY = "docker.io"`. Print a summary and the equivalent `docker run` command built from the variables.

## 10. DevOps/MLOps Connection

- **DevOps:** Every script starts by naming its settings: `BACKUP_DIR`, `RETENTION_DAYS`, `SLACK_CHANNEL`. Good names make on-call debugging fast.
- **Cloud automation:** AWS scripts hold `region`, `bucket_name`, `instance_id` in variables so the same script works across environments.
- **MLOps:** Hyper-parameters (`learning_rate`, `n_estimators`, `MODEL_VERSION`) are variables/constants that you log for every training run.

## 11. Interview Questions

**Q1. What is a variable in Python?**

<details><summary>Show answer</summary>

A name that refers to an object (value) stored in memory. Assignment `x = 5` binds the name `x` to the object `5`.

</details>

**Q2. What naming convention does PEP 8 recommend for variables and constants?**

<details><summary>Show answer</summary>

`snake_case` for variables and functions, `UPPER_CASE` for constants, `PascalCase` for classes.

</details>

**Q3. Does Python enforce constants?**

<details><summary>Show answer</summary>

No. `UPPER_CASE` is only a convention telling other developers not to reassign the value.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 2 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 001](../../01-python-fundamentals/day-001/README.md) | [📚 Phase 1: Python Fundamentals](../README.md) | [🏠 Home](../../README.md) | [Day 003 ➡](../../01-python-fundamentals/day-003/README.md)
