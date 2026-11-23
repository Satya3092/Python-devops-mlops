# Day 061 — Subprocess Module

[⬅ Day 060](../../06-modules-oop/day-060/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 062 ➡](../../06-modules-oop/day-062/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 6 — Advanced Python and OOP | 🟡 Intermediate | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Run external commands with `subprocess.run`
- Capture output, check exit codes and handle errors
- Avoid shell-injection risks and use timeouts

## 2. Topic Explanation

`subprocess` lets Python run **other programs** — `git`, `docker`, `kubectl`, `terraform`, any Linux command — and work with their output.

```python
import subprocess
result = subprocess.run(["git", "--version"], capture_output=True, text=True)
print(result.stdout)
```

Key arguments of `subprocess.run`:

| Argument | Purpose |
|---|---|
| `["cmd", "arg1"]` | command as a **list** (safest) |
| `capture_output=True` | collect stdout/stderr instead of printing them |
| `text=True` | return strings instead of bytes |
| `check=True` | raise `CalledProcessError` if exit code ≠ 0 |
| `timeout=30` | raise `TimeoutExpired` if it takes too long |
| `cwd="path"` | run in another directory |
| `env={...}` | custom environment variables |
| `input="..."` | send text to the command's stdin |

The result object has `.returncode`, `.stdout`, `.stderr`.

**Security:** prefer a **list** of arguments. `shell=True` with user-provided text allows **shell injection** (`"; rm -rf /"`). Only use `shell=True` with fixed, trusted strings — and when you really need pipes, consider doing the "pipe" in Python instead.

## 3. Syntax

```python
import subprocess
result = subprocess.run(
    ["command", "arg"],
    capture_output=True, text=True, check=False, timeout=30,
)
result.returncode, result.stdout, result.stderr
```

| Part | Meaning |
|---|---|
| `list of args` | No shell parsing — safe from injection. |
| `capture_output / text` | Get output as strings. |
| `check=True` | Raise CalledProcessError on non-zero exit. |
| `timeout` | Kill the command if it runs too long. |
| `returncode` | 0 means success (just like `$?` in Bash). |

## 4. Example 1 — Basic Example: Running commands and reading results

```python
import subprocess
import sys

result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
print("Return code:", result.returncode)
print("Output:", result.stdout.strip() or result.stderr.strip())

result = subprocess.run(["echo", "Hello from a child process"], capture_output=True, text=True)
print("echo said:", result.stdout.strip())

result = subprocess.run(["ls", "this-folder-does-not-exist"], capture_output=True, text=True)
print("ls exit code:", result.returncode)
print("ls stderr:", result.stderr.strip().split(":")[-1].strip())

try:
    subprocess.run(["ls", "this-folder-does-not-exist"], capture_output=True, text=True, check=True)
except subprocess.CalledProcessError as error:
    print("CalledProcessError, exit code", error.returncode)

try:
    subprocess.run(["sleep", "5"], timeout=1)
except subprocess.TimeoutExpired:
    print("Command timed out after 1 second")
```

## 5. Example 2 — Practical Example: A safe command runner for automation

```python
import shutil
import subprocess


def run(command, timeout=30):
    """Run a command list, return (ok, output). Never raises for normal failures."""
    if shutil.which(command[0]) is None:
        return False, f"{command[0]}: command not found"
    try:
        result = subprocess.run(command, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return False, f"timed out after {timeout}s"
    output = (result.stdout or result.stderr).strip()
    return result.returncode == 0, output


checks = {
    "Kernel": ["uname", "-sr"],
    "Disk (/)": ["df", "-h", "/"],
    "Uptime": ["uptime"],
    "Docker": ["docker", "--version"],
    "Bad command": ["kubectl-that-does-not-exist", "version"],
}

for name, command in checks.items():
    ok, output = run(command)
    first_line = output.splitlines()[-1] if output else ""
    print(f"[{'OK' if ok else 'FAIL':<4}] {name:<12} {first_line[:60]}")

# Processing output in Python instead of using shell pipes
ok, output = run(["df", "-P"])
if ok:
    rows = [line.split() for line in output.splitlines()[1:]]
    busiest = max(rows, key=lambda r: int(r[4].rstrip("%")))
    print(f"Fullest filesystem: {busiest[5]} at {busiest[4]}")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `sys.executable` is the current Python interpreter — a portable command to run.
- A non-zero `returncode` means failure; `stderr` holds the error text.
- `check=True` turns failures into a `CalledProcessError` exception.
- `timeout=1` stops `sleep 5` early with `TimeoutExpired`.

**Example 2**
- `run()` wraps subprocess with three safety nets: tool existence (`shutil.which`), timeout, and a simple `(ok, output)` result.
- Each check is a **list** of arguments — no shell, no injection risk.
- Instead of `df -P | sort | tail -1`, we parse the output in Python: easier to test and portable.

## 7. Expected Output

**Example 1:**

```text
Return code: 0
Output: Python 3.13.18
echo said: Hello from a child process
ls exit code: 2
ls stderr: No such file or directory
CalledProcessError, exit code 2
Command timed out after 1 second
```

**Example 2:**

```text
[OK  ] Kernel       Linux 6.8.0-49-generic
[OK  ] Disk (/)     /dev/sda1        50G   41G  9.0G  82% /
[OK  ] Uptime       10:15:32 up 12 days,  3:04,  1 user,  load average: 0.52, 0.48, 0.45
[OK  ] Docker       Docker version 27.3.1, build ce12230
[FAIL] Bad command  kubectl-that-does-not-exist: command not found
Fullest filesystem: / at 82%
```

> ℹ️ Your values (paths, hostnames, sizes, times) will differ from the output shown — it depends on your machine. Examples that call Linux commands work on Linux, macOS and WSL.

## 8. Common Mistakes

**1. `shell=True` with user input**

`subprocess.run(f"ping {host}", shell=True)` lets a host like `x; rm -rf ~` execute extra commands. Use a list: `["ping", "-c", "1", host]`.

**2. Ignoring the return code**

A failed command still returns a result object. Check `returncode` or use `check=True`.

**3. No timeout**

A hung command (waiting for a password prompt, network) blocks your automation forever. Always set `timeout`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Python version:** Run `python --version` via `sys.executable` and print only the version number.
- **Task 2 (Medium) — Git information:** Write `git_info()` that returns a dict with git's version (or `not installed`) using `shutil.which` and `subprocess.run`. Print it.
- **Task 3 (Practical Challenge) — Service status checker:** Write `count_lines(command)` that runs a command and returns how many lines it printed, and `top_processes(n)` that runs `ps -eo pid,comm,%mem --sort=-%mem` and returns the top n as a list of tuples `(pid, name, mem_percent)`. Print the top 3 processes in a table. Handle errors gracefully.

## 10. DevOps/MLOps Connection

- **DevOps:** wrapping `git`, `docker`, `kubectl`, `helm`, `terraform` and `ansible-playbook` in Python gives you error handling, retries and structured logs that Bash makes painful.
- **CI/CD:** custom build steps that run tools and fail the pipeline on non-zero exit codes.
- **MLOps:** triggering `dvc`, `docker build` or training scripts from an orchestration script (Day 100).

## 11. Interview Questions

**Q1. Why is passing a list to subprocess.run safer than a string with shell=True?**

<details><summary>Show answer</summary>

No shell is involved, so special characters in arguments cannot inject extra commands.

</details>

**Q2. How do you capture a command's output as text?**

<details><summary>Show answer</summary>

`subprocess.run(cmd, capture_output=True, text=True).stdout`.

</details>

**Q3. How do you make subprocess raise an exception on failure?**

<details><summary>Show answer</summary>

Pass `check=True`; non-zero exit codes raise `CalledProcessError`.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 61 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 060](../../06-modules-oop/day-060/README.md) | [📚 Phase 6: Advanced Python and OOP](../README.md) | [🏠 Home](../../README.md) | [Day 062 ➡](../../06-modules-oop/day-062/README.md)
