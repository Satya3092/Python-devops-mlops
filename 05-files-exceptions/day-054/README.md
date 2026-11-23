# Day 054 — Creating Custom Exceptions

[⬅ Day 053](../../05-files-exceptions/day-053/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 055 ➡](../../05-files-exceptions/day-055/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Raise exceptions deliberately with `raise`
- Create custom exception classes that inherit from `Exception`
- Build an exception hierarchy for a tool

## 2. Topic Explanation

Built-in exceptions describe *Python* problems. Your tool has **domain** problems: "deployment failed", "config invalid", "quota exceeded". Custom exceptions make these explicit.

```python
class DeploymentError(Exception):
    pass    # a docstring describing the error is even better (see examples)

raise DeploymentError("health check failed on web-02")
```

- A custom exception is a **class** that inherits from `Exception` (classes are covered on Days 63–65; for now copy the pattern).
- The name should end with `Error`.
- Use `raise` to signal a problem as early as possible (**fail fast**) — e.g. validate inputs at the top of a function.
- A **hierarchy** lets callers catch broadly or precisely:

```python
class ToolError(Exception): ...
class ConfigError(ToolError): ...
class DeploymentError(ToolError): ...
# except ToolError catches both; except ConfigError catches only one
```

You can also add extra data to an exception (e.g. which host failed) by overriding `__init__`.

## 3. Syntax

```python
class MyError(Exception):
    """What this error means."""

raise MyError("explanation")

try:
    ...
except MyError as error:
    ...
```

| Part | Meaning |
|---|---|
| `class X(Exception)` | Defines a new exception type based on Exception. |
| `raise X("msg")` | Signals the error with a message. |
| `hierarchy` | Subclasses can be caught by their parent class. |
| `raise ... from error` | Chains a new exception to the original cause. |

## 4. Example 1 — Basic Example: Raising built-in and custom exceptions

```python
def set_replicas(count):
    if not isinstance(count, int):
        raise TypeError("replicas must be an integer")
    if count < 0:
        raise ValueError("replicas cannot be negative")
    return f"Scaled to {count} replicas"


for value in (3, -1, "two"):
    try:
        print(set_replicas(value))
    except (TypeError, ValueError) as error:
        print(f"{type(error).__name__}: {error}")


class InsufficientFundsError(Exception):
    """Raised when an account balance is too low."""


try:
    raise InsufficientFundsError("balance 100, requested 250")
except InsufficientFundsError as error:
    print("Custom error caught:", error)
```

## 5. Example 2 — Practical Example: An exception hierarchy for a deployment tool

```python
class DeployToolError(Exception):
    """Base class for every error raised by our deployment tool."""


class ConfigError(DeployToolError):
    """The deployment configuration is invalid."""


class HealthCheckError(DeployToolError):
    """A host failed its health check after deployment."""

    def __init__(self, host, status_code):
        super().__init__(f"{host} returned HTTP {status_code}")
        self.host = host
        self.status_code = status_code


def validate_config(config):
    for key in ("service", "version", "hosts"):
        if key not in config:
            raise ConfigError(f"missing required key '{key}'")
    if not config["hosts"]:
        raise ConfigError("at least one host is required")


def deploy(config, health):
    validate_config(config)
    for host in config["hosts"]:
        status = health.get(host, 200)
        if status != 200:
            raise HealthCheckError(host, status)
        print(f"  {host}: deployed {config['service']} {config['version']}")
    return "success"


scenarios = [
    ({"service": "orders", "version": "1.2", "hosts": ["web-01", "web-02"]}, {}),
    ({"service": "orders", "hosts": ["web-01"]}, {}),
    ({"service": "orders", "version": "1.3", "hosts": ["web-01", "web-02"]}, {"web-02": 503}),
]
for config, health in scenarios:
    print("Deploying", config)
    try:
        print("Result:", deploy(config, health))
    except HealthCheckError as error:
        print(f"Rollback needed! host={error.host} code={error.status_code}")
    except DeployToolError as error:
        print(f"{type(error).__name__}: {error}")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `raise TypeError(...)` / `raise ValueError(...)` validate inputs early (fail fast).
- `InsufficientFundsError` is a minimal custom exception: just a class with a docstring.

**Example 2**
- `DeployToolError` is the base; `ConfigError` and `HealthCheckError` are specific kinds.
- `HealthCheckError.__init__` stores extra attributes (`host`, `status_code`) and passes a message to the parent with `super().__init__(...)`.
- The caller handles `HealthCheckError` specially (rollback) and every other tool error generically via the base class. Order matters: specific `except` clauses come first.

## 7. Expected Output

**Example 1:**

```text
Scaled to 3 replicas
ValueError: replicas cannot be negative
TypeError: replicas must be an integer
Custom error caught: balance 100, requested 250
```

**Example 2:**

```text
Deploying {'service': 'orders', 'version': '1.2', 'hosts': ['web-01', 'web-02']}
  web-01: deployed orders 1.2
  web-02: deployed orders 1.2
Result: success
Deploying {'service': 'orders', 'hosts': ['web-01']}
ConfigError: missing required key 'version'
Deploying {'service': 'orders', 'version': '1.3', 'hosts': ['web-01', 'web-02']}
  web-01: deployed orders 1.3
Rollback needed! host=web-02 code=503
```

## 8. Common Mistakes

**1. Inheriting from `BaseException`**

Custom exceptions should inherit from `Exception`; `BaseException` is reserved for things like `KeyboardInterrupt`.

**2. Raising strings**

`raise "error"` is a `TypeError` in Python 3. Raise an exception instance.

**3. Catching the base class first**

If `except DeployToolError` comes before `except HealthCheckError`, the specific handler never runs.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Validate an email:** Write `validate_email(email)` that raises `ValueError` if the email has no `@` or no `.` after the `@`. Test with three emails.
- **Task 2 (Medium) — Quota exceeded:** Create `QuotaExceededError`. Write `request_instances(current, requested, limit=20)` that raises it with a clear message when the limit would be exceeded, otherwise returns the new total. Handle it in the caller.
- **Task 3 (Practical Challenge) — Backup tool errors:** Create a hierarchy `BackupError` → `SourceMissingError`, `InsufficientSpaceError` (store `needed_gb` and `free_gb`). Write `backup(source, size_gb, free_gb)` that raises the right error. Run three scenarios and handle each appropriately (print specific advice for space problems).

## 10. DevOps/MLOps Connection

- **DevOps:** CLI tools define errors like `ConfigError` and `DeploymentError` so the main program can map them to exit codes and clear messages.
- **Cloud:** botocore defines a hierarchy (`ClientError`, `NoCredentialsError`, `EndpointConnectionError`) — the same pattern you built today.
- **MLOps:** raise `DataValidationError` when incoming data fails schema checks, or `ModelNotFoundError` when an API starts without a model file.

## 11. Interview Questions

**Q1. How do you create a custom exception?**

<details><summary>Show answer</summary>

Define a class that inherits from `Exception` (or a subclass), optionally adding attributes via `__init__`.

</details>

**Q2. Why create an exception hierarchy?**

<details><summary>Show answer</summary>

Callers can catch all errors from a library via the base class or handle specific cases precisely.

</details>

**Q3. What does `raise NewError(...) from error` do?**

<details><summary>Show answer</summary>

Chains exceptions: the new exception records the original as its `__cause__`, preserving debugging information.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 54 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 053](../../05-files-exceptions/day-053/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 055 ➡](../../05-files-exceptions/day-055/README.md)
