# Day 062 — Logging Module

[⬅ Day 061](../../06-modules-oop/day-061/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 063 ➡](../../06-modules-oop/day-063/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Replace `print` with proper logging levels
- Configure format, level and log files with `basicConfig`
- Use named loggers, handlers and rotating log files

## 2. Topic Explanation

`print()` is fine for learning, but real tools need **logging**: timestamps, severity levels, output to files, and the ability to turn detail up or down without changing code.

Levels (lowest → highest):

| Level | Use for |
|---|---|
| `DEBUG` | detailed diagnostic info |
| `INFO` | normal operations ("backup started") |
| `WARNING` | something unexpected, still working (default threshold) |
| `ERROR` | an operation failed |
| `CRITICAL` | the program may not continue |

Only messages **at or above** the configured level are shown.

```python
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")
log = logging.getLogger("backup")
log.info("Backup started")
```

Concepts:
- **Logger** — what you call (`getLogger(__name__)` gives one per module).
- **Handler** — where logs go: console (`StreamHandler`), file (`FileHandler`), rotating file (`RotatingFileHandler`).
- **Formatter** — what each line looks like.
- `log.exception("msg")` inside `except` logs the full traceback.

Containers and Kubernetes collect **stdout/stderr**, so in containers log to the console; on VMs, log files + logrotate are common.

## 3. Syntax

```python
import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)
logger.debug("...")  logger.info("...")  logger.warning("...")
logger.error("...")  logger.critical("...")
logger.exception("...")   # inside except: includes traceback
```

| Part | Meaning |
|---|---|
| `basicConfig` | One-line configuration of the root logger. |
| `level` | Minimum level to emit. |
| `format` | Placeholders: %(asctime)s, %(levelname)s, %(name)s, %(message)s, %(lineno)d... |
| `getLogger(name)` | Named logger, usually `__name__`. |
| `logger.exception` | ERROR level + traceback. |

## 4. Example 1 — Basic Example: Levels and formatting

```python
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-8s %(name)s: %(message)s",   # no time so the output is stable
    stream=sys.stdout,
)
log = logging.getLogger("demo")

log.debug("Not shown: DEBUG is below INFO")
log.info("Application started")
log.warning("Disk usage at %d%%", 82)          # lazy % formatting
log.error("Could not connect to %s", "db-01")
log.critical("Out of memory - shutting down")

try:
    1 / 0
except ZeroDivisionError:
    log.exception("Calculation failed")
```

## 5. Example 2 — Practical Example: Console + rotating file logging for a backup job

```python
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logger(name, log_file, level=logging.DEBUG):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)                       # console: INFO and above
    console.setFormatter(logging.Formatter("%(levelname)s | %(message)s"))

    file_handler = RotatingFileHandler(log_file, maxBytes=2000, backupCount=2)
    file_handler.setLevel(logging.DEBUG)                 # file: everything
    file_handler.setFormatter(logging.Formatter("%(levelname)s %(name)s line %(lineno)d: %(message)s"))

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger


log = setup_logger("backup", "backup.log")
databases = ["orders", "users", "payments"]
log.info("Backup job started for %d databases", len(databases))
for db in databases:
    log.debug("Connecting to %s", db)
    if db == "payments":
        log.error("Backup of %s failed: permission denied", db)
        continue
    log.info("Backed up %s", db)
log.info("Backup job finished")

print("--- backup.log (file contains DEBUG lines too) ---")
print(Path("backup.log").read_text().strip())
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `level=logging.INFO` hides the DEBUG message.
- `%(levelname)-8s` left-pads the level to 8 characters for aligned output.
- Passing values as arguments (`"%d%%", 82`) is the recommended lazy formatting (the string is only built if the message is emitted).
- `log.exception` adds the traceback automatically.

**Example 2**
- One logger, two handlers: the console shows INFO+, the file records DEBUG+.
- `RotatingFileHandler(maxBytes=2000, backupCount=2)` rotates the file when it grows past 2000 bytes, keeping `backup.log.1` and `.2` — no more full disks from logs.
- `%(lineno)d` records the source line, which helps debugging.

## 7. Expected Output

**Example 1:**

```text
INFO     demo: Application started
WARNING  demo: Disk usage at 82%
ERROR    demo: Could not connect to db-01
CRITICAL demo: Out of memory - shutting down
ERROR    demo: Calculation failed
Traceback (most recent call last):
  File "examples.py", in <module>
    1 / 0
    ~~^~~
ZeroDivisionError: division by zero
```

**Example 2:**

```text
INFO | Backup job started for 3 databases
INFO | Backed up orders
INFO | Backed up users
ERROR | Backup of payments failed: permission denied
INFO | Backup job finished
--- backup.log (file contains DEBUG lines too) ---
INFO backup line 26: Backup job started for 3 databases
DEBUG backup line 28: Connecting to orders
INFO backup line 32: Backed up orders
DEBUG backup line 28: Connecting to users
INFO backup line 32: Backed up users
DEBUG backup line 28: Connecting to payments
ERROR backup line 30: Backup of payments failed: permission denied
INFO backup line 33: Backup job finished
```

## 8. Common Mistakes

**1. Calling `basicConfig` too late**

It only works if no handlers are configured yet. Call it once at program start.

**2. Adding handlers repeatedly**

Calling `setup_logger` twice adds duplicate handlers → every line printed twice. Configure once.

**3. Logging secrets**

Never log passwords, tokens or full request bodies with personal data.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — First logger:** Configure logging at WARNING level (format `LEVEL: message`, to stdout) and emit one message of each level. Only 3 should appear.
- **Task 2 (Medium) — Log to a file:** Configure a logger named `deploy` that writes INFO+ to `deploy.log` with format `%(levelname)s %(message)s`. Log 3 deployment steps and one error, then print the file.
- **Task 3 (Practical Challenge) — Instrument a function:** Write `process_orders(orders, logger)` that logs DEBUG for each order, WARNING for orders with amount > 1000, and uses `logger.exception` for orders with a missing amount (KeyError), continuing with the rest. Log a final INFO summary. Use a console handler with format `%(levelname)s %(message)s` at DEBUG level.

## 10. DevOps/MLOps Connection

- **DevOps:** structured, levelled logs are what you ship to ELK/EFK, Loki or CloudWatch. `LOG_LEVEL` environment variables switch verbosity without redeploying.
- **Kubernetes:** log to stdout; the container runtime and Fluent Bit collect it.
- **MLOps:** log data sizes, training progress, metrics and prediction latencies; a model service without logs is impossible to debug.

## 11. Interview Questions

**Q1. Why use logging instead of print?**

<details><summary>Show answer</summary>

Levels, timestamps, configurable outputs (files, syslog, remote), formatting and the ability to change verbosity without code changes.

</details>

**Q2. What is the default logging level?**

<details><summary>Show answer</summary>

WARNING.

</details>

**Q3. What is the difference between a logger and a handler?**

<details><summary>Show answer</summary>

A logger is the object your code calls; handlers decide where the records go (console, file, network).

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 62 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 061](../../06-modules-oop/day-061/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 063 ➡](../../06-modules-oop/day-063/README.md)
