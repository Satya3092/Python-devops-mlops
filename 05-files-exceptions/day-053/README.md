# Day 053 — try, except, else, finally

[⬅ Day 052](../../05-files-exceptions/day-052/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 054 ➡](../../05-files-exceptions/day-054/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 5 — File Handling and Error Handling | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Use `else` for code that runs only when no exception occurred
- Use `finally` for cleanup that must always run
- Re-raise exceptions and understand the full try statement flow

## 2. Topic Explanation

The full `try` statement has four parts:

```python
try:
    result = risky()          # 1. try this
except SomeError:
    handle()                  # 2. only if it failed
else:
    use(result)               # 3. only if it did NOT fail
finally:
    cleanup()                 # 4. ALWAYS, no matter what
```

- **`else`** keeps the `try` block small: only the risky line is inside `try`, and the "success path" goes in `else`.
- **`finally`** is for cleanup: closing connections, removing lock files, releasing resources, logging "job finished". It runs even if there was an unhandled exception or a `return`.
- **`raise`** inside `except` re-raises the current exception after you logged it — useful when you can't really fix the problem.

Analogy: a surgery. *try* = operate, *except* = handle complications, *else* = normal recovery plan, *finally* = always clean the theatre and count the instruments.

## 3. Syntax

```python
try:
    ...
except ErrorType as error:
    ...
    raise            # optional: re-raise
else:
    ...
finally:
    ...
```

| Part | Meaning |
|---|---|
| `else:` | Runs when the try block raised nothing. |
| `finally:` | Always runs — success, handled error or unhandled error. |
| `raise` | Alone inside except: re-raises the current exception. |

## 4. Example 1 — Basic Example: Seeing the flow

```python
def divide(a, b):
    print(f"--- divide({a}, {b}) ---")
    try:
        result = a / b
    except ZeroDivisionError:
        print("except: cannot divide by zero")
        return None
    else:
        print("else: success, result =", result)
        return result
    finally:
        print("finally: always runs")


print("Returned:", divide(10, 2))
print("Returned:", divide(1, 0))
```

## 5. Example 2 — Practical Example: A deployment with a lock file and guaranteed cleanup

```python
import os

LOCK_FILE = "deploy.lock"


def deploy(version, fail=False):
    if os.path.exists(LOCK_FILE):
        print("Another deployment is running - abort")
        return False

    open(LOCK_FILE, "w").close()                     # create the lock
    print(f"Deploying {version} (lock acquired)")
    try:
        if fail:
            raise RuntimeError("health check failed after rollout")
        print("Rollout complete")
    except RuntimeError as error:
        print("Deployment error:", error)
        print("Rolling back...")
        return False
    else:
        print("Recording successful release", version)
        return True
    finally:
        os.remove(LOCK_FILE)                         # ALWAYS release the lock
        print("Lock released")


print("Result:", deploy("v1.2.0"))
print()
print("Result:", deploy("v1.3.0", fail=True))
print("Lock left behind?", os.path.exists(LOCK_FILE))
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Success path: `try` → `else` → `finally`.
- Error path: `try` → `except` → `finally`. Even though `except` executes `return None`, `finally` still runs before the function returns.

**Example 2**
- A lock file prevents two deployments running at the same time (very common in CI scripts).
- `raise RuntimeError(...)` simulates a failed health check.
- Whatever happens, `finally` deletes the lock — otherwise one failure would block every future deployment.
- `else` only records the release when the rollout succeeded.

## 7. Expected Output

**Example 1:**

```text
--- divide(10, 2) ---
else: success, result = 5.0
finally: always runs
Returned: 5.0
--- divide(1, 0) ---
except: cannot divide by zero
finally: always runs
Returned: None
```

**Example 2:**

```text
Deploying v1.2.0 (lock acquired)
Rollout complete
Recording successful release v1.2.0
Lock released
Result: True

Deploying v1.3.0 (lock acquired)
Deployment error: health check failed after rollout
Rolling back...
Lock released
Result: False
Lock left behind? False
```

## 8. Common Mistakes

**1. Putting everything in `try`**

Code that cannot fail belongs in `else`, so you don't accidentally catch errors from it.

**2. Returning from `finally`**

A `return` inside `finally` swallows exceptions and overrides other returns. Use `finally` only for cleanup.

**3. Cleanup without `finally`**

If an error happens, cleanup code after the try block never runs. Use `finally` or a `with` statement.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Trace the flow:** Write `check(value)` that converts value to int inside try, prints `invalid` in except, `valid: n` in else and `checked` in finally. Call it with `"7"` and `"x"`.
- **Task 2 (Medium) — Always close the connection:** Simulate a database connection with a dict `{"open": True}`. Write `run_query(conn, query)` that raises `ValueError` for queries containing `DROP`, and always sets `conn["open"] = False` in `finally`. Show the connection is closed after a good and a bad query.
- **Task 3 (Practical Challenge) — Retry with finally-based metrics:** Write `fetch_with_retry(results, max_attempts=3)` where `results` is a list of booleans simulating each attempt. Use try/except/else/finally inside a loop: raise `ConnectionError` on False, return on success in `else`, and count attempts in `finally`. Re-raise the last error if all attempts fail. Test success on attempt 2, and total failure.

## 10. DevOps/MLOps Connection

- **DevOps:** releasing locks, deleting temporary files, closing SSH sessions and always sending a "job finished" notification (`finally`).
- **Cloud:** cleaning up temporary resources (test instances, temporary buckets) even when a test fails.
- **MLOps:** always ending an experiment run / closing a tracking session, and releasing GPU memory after training.

## 11. Interview Questions

**Q1. When does the `else` clause of a try statement run?**

<details><summary>Show answer</summary>

Only if the try block completed without raising an exception.

</details>

**Q2. Does `finally` run if the try block returns?**

<details><summary>Show answer</summary>

Yes. `finally` runs before the function actually returns.

</details>

**Q3. Why might you re-raise an exception after catching it?**

<details><summary>Show answer</summary>

To log or clean up locally while still letting the caller (or the process) know the operation failed.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 53 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 052](../../05-files-exceptions/day-052/README.md) | [📚 Phase 5: File Handling and Error Handling](../README.md) | [🏠 Home](../../README.md) | [Day 054 ➡](../../05-files-exceptions/day-054/README.md)
