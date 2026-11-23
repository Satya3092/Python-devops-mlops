# Day 052 — Exception Handling

[⬅ Day 051](../../05-files-exceptions/day-051/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 053 ➡](../../05-files-exceptions/day-053/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Understand what exceptions are and read tracebacks
- Catch errors with `try` / `except`
- Catch specific exception types and access the error message

## 2. Topic Explanation

An **exception** is an error that happens while the program runs: a missing file, bad user input, a network timeout. If nobody handles it, Python stops and prints a **traceback** (read it from the **bottom** up: the last line names the error type and message).

`try/except` lets you **catch** the error and decide what to do:

```python
try:
    port = int(user_input)
except ValueError:
    print("Port must be a number")
```

Common exception types:

| Exception | When |
|---|---|
| `ValueError` | right type, wrong value: `int("abc")` |
| `TypeError` | wrong type: `"a" + 1` |
| `KeyError` | missing dict key |
| `IndexError` | list index out of range |
| `FileNotFoundError` | file missing |
| `ZeroDivisionError` | divide by zero |
| `PermissionError` | no access rights |

Best practices:
- Catch **specific** exceptions, never a bare `except:`.
- Use `except SomeError as error:` to get the message.
- Keep the `try` block small — only the lines that can fail.

Analogy: `try/except` is a safety net under a trapeze. The act still happens; if someone falls, the net catches them and the show goes on.

## 3. Syntax

```python
try:
    risky_operation()
except SpecificError as error:
    handle(error)
except (ErrorA, ErrorB):
    handle_both()
```

| Part | Meaning |
|---|---|
| `try:` | Block of code that might raise an exception. |
| `except Type:` | Runs only if that type of exception occurred. |
| `as error` | Gives access to the exception object (`str(error)` is the message). |
| `(A, B)` | Catch several types with one handler. |

## 4. Example 1 — Basic Example: Catching common errors

```python
values = ["42", "3.5", "abc", "100"]
for value in values:
    try:
        number = int(value)
        print(f"{value!r} -> {number}")
    except ValueError as error:
        print(f"{value!r} -> ValueError: {error}")

config = {"host": "localhost"}
try:
    print(config["port"])
except KeyError as error:
    print("Missing key:", error)

try:
    print(10 / 0)
except ZeroDivisionError:
    print("Cannot divide by zero")

try:
    with open("does_not_exist.txt", encoding="utf-8") as f:
        f.read()
except FileNotFoundError as error:
    print("File problem:", error.filename, "-", error.strerror)
```

## 5. Example 2 — Practical Example: Robust parsing of messy metrics

```python
raw_metrics = [
    "web-01,cpu,45.2",
    "web-02,cpu,ninety",          # bad number
    "web-03,cpu",                 # missing field
    "db-01,cpu,77.0",
    "",                           # empty line
    "db-02,cpu,0",
]

parsed = []
problems = []
for line_number, line in enumerate(raw_metrics, start=1):
    try:
        host, metric, value = line.split(",")
        parsed.append((host, metric, float(value)))
    except ValueError as error:
        problems.append(f"line {line_number}: {error}")

print("Parsed:", parsed)
print("Problems:")
for p in problems:
    print("  ", p)

# Use the clean data safely
values = [v for _, _, v in parsed]
try:
    ratio = values[0] / values[-1]
except ZeroDivisionError:
    ratio = None
except IndexError:
    ratio = None
print("Ratio first/last:", ratio)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `int("abc")` raises `ValueError`; the loop continues with the next value instead of crashing.
- `KeyError`, `ZeroDivisionError` and `FileNotFoundError` are caught separately. `FileNotFoundError` gives `.filename` and `.strerror`.
- `{value!r}` shows the value with quotes (its `repr`).

**Example 2**
- One bad line no longer kills the whole job. Both "wrong number of fields" (unpacking) and "not a number" (`float`) raise `ValueError`, so one handler covers both.
- Problems are collected and reported — the program degrades gracefully.
- The last value is 0, so the division raises `ZeroDivisionError`, which we handle.

## 7. Expected Output

**Example 1:**

```text
'42' -> 42
'3.5' -> ValueError: invalid literal for int() with base 10: '3.5'
'abc' -> ValueError: invalid literal for int() with base 10: 'abc'
'100' -> 100
Missing key: 'port'
Cannot divide by zero
File problem: does_not_exist.txt - No such file or directory
```

**Example 2:**

```text
Parsed: [('web-01', 'cpu', 45.2), ('db-01', 'cpu', 77.0), ('db-02', 'cpu', 0.0)]
Problems:
   line 2: could not convert string to float: 'ninety'
   line 3: not enough values to unpack (expected 3, got 2)
   line 5: not enough values to unpack (expected 3, got 1)
Ratio first/last: None
```

## 8. Common Mistakes

**1. Bare `except:`**

It also catches `KeyboardInterrupt` and hides real bugs (like typos). Catch specific exceptions.

**2. Silently ignoring errors**

`except ValueError: pass` hides problems. At least log or count them.

**3. Huge try blocks**

Wrapping 50 lines in one `try` makes it unclear which line failed. Keep `try` blocks small.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Safe integer input:** Ask the user for their age. If it is not a valid integer, print `Please enter a whole number` instead of crashing.
- **Task 2 (Medium) — Safe list access:** Write `get_item(items, index)` that returns the item or the string `out of range` when the index is invalid (catch `IndexError`). Test with indexes 0, 5 and -1 on `["a", "b", "c"]`.
- **Task 3 (Practical Challenge) — Config loader with clear errors:** Write `load_port(path)` that reads a JSON file and returns `config["server"]["port"]` as an int. Handle: missing file, invalid JSON (`json.JSONDecodeError`), missing keys and a non-numeric port, returning `None` and printing a specific message for each. Test it with 4 small files you create in the solution.

## 10. DevOps/MLOps Connection

- **DevOps:** automation must survive bad input, missing files and flaky networks — and report *what* went wrong.
- **Cloud:** boto3 raises `botocore.exceptions.ClientError` for API errors (AccessDenied, NoSuchBucket); you catch and handle them (Day 82).
- **Data engineering:** skip/quarantine bad records instead of failing the whole batch.
- **MLOps:** a prediction API must return a clean 400/422 error for invalid input, not crash (Day 98).

## 11. Interview Questions

**Q1. Why should you avoid a bare `except:`?**

<details><summary>Show answer</summary>

It catches everything including SystemExit and KeyboardInterrupt and hides programming errors.

</details>

**Q2. How do you catch multiple exception types in one clause?**

<details><summary>Show answer</summary>

`except (ValueError, TypeError) as error:`.

</details>

**Q3. How do you read a Python traceback?**

<details><summary>Show answer</summary>

From the bottom: the last line shows the exception type and message; the lines above show the call stack leading to it, most recent call last.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 52 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 051](../../05-files-exceptions/day-051/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 053 ➡](../../05-files-exceptions/day-053/README.md)
