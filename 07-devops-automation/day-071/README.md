# Day 071 — Automating Linux Commands with subprocess

[⬅ Day 070](../../07-devops-automation/day-070/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 072 ➡](../../07-devops-automation/day-072/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Chain commands and replace shell pipelines with Python
- Stream long-running command output line by line
- Run commands in parallel and collect results (fan-out)

## 2. Topic Explanation

On Day 61 you learned `subprocess.run`. Today you build real automation on top of it:

**1. Pipelines without the shell.** Instead of `cat access.log | grep 500 | wc -l`, run one command and do the filtering in Python — or connect processes with `input=`:
```python
first = subprocess.run(["printf", "b\\na\\n"], capture_output=True, text=True)
sorted_out = subprocess.run(["sort"], input=first.stdout, capture_output=True, text=True)
```

**2. Streaming output.** `subprocess.Popen` starts a process and lets you read its output **while it runs** — essential for long builds (`docker build`, `terraform apply`) so logs appear live.

**3. Parallel execution.** Checking 50 servers one by one is slow. `concurrent.futures.ThreadPoolExecutor` runs many subprocesses at the same time (fan-out) and collects the results.

**4. Retries for flaky commands** — network operations (`git fetch`, `apt-get update`) sometimes fail transiently.

Keep using **argument lists**, **timeouts**, and **exit-code checks** from Day 61.

## 3. Syntax

```python
import subprocess
from concurrent.futures import ThreadPoolExecutor

proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
for line in proc.stdout:
    print(line, end="")
proc.wait()

with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(function, items))
```

| Part | Meaning |
|---|---|
| `input=` | Feed text to a command's stdin (replaces a pipe). |
| `Popen` | Start a process without waiting; read output as it arrives. |
| `stderr=STDOUT` | Merge errors into the same stream. |
| `ThreadPoolExecutor` | Run functions concurrently in threads. |
| `pool.map` | Apply a function to many items, results in order. |

## 4. Example 1 — Basic Example: Pipelines and live output

```python
import subprocess
import sys

# Pipeline: generate text -> sort -> uniq -c   (like: ... | sort | uniq -c)
generated = subprocess.run(["printf", "web\ndb\nweb\ncache\nweb\ndb\n"], capture_output=True, text=True, check=True)
sorted_text = subprocess.run(["sort"], input=generated.stdout, capture_output=True, text=True, check=True)
counted = subprocess.run(["uniq", "-c"], input=sorted_text.stdout, capture_output=True, text=True, check=True)
print("uniq -c result:")
print(counted.stdout.rstrip())

# The same counting done in Python (no extra processes needed)
counts = {}
for word in generated.stdout.split():
    counts[word] = counts.get(word, 0) + 1
print("Python result:", dict(sorted(counts.items())))

# Streaming output from a 'long-running' command
script = "import time\nfor i in range(1, 4):\n    print(f'step {i}/3 done', flush=True)\n    time.sleep(0.2)"
proc = subprocess.Popen([sys.executable, "-c", script], stdout=subprocess.PIPE,
                        stderr=subprocess.STDOUT, text=True)
for line in proc.stdout:
    print("[live]", line.rstrip())
print("exit code:", proc.wait())
```

## 5. Example 2 — Practical Example: Parallel health checks with retries

```python
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

# Simulated 'check' commands: each host is a small Python program that exits 0 (ok) or 1 (fail)
HOSTS = {"web-01": 0, "web-02": 0, "db-01": 1, "cache-01": 0, "queue-01": 0}


def check_host(host, attempts=2):
    """Run a (simulated) health check; retry once on failure."""
    exit_code = HOSTS[host]
    command = [sys.executable, "-c", f"import time, sys; time.sleep(0.5); sys.exit({exit_code})"]
    for attempt in range(1, attempts + 1):
        result = subprocess.run(command, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return host, "OK", attempt
    return host, "FAILED", attempts


start = time.perf_counter()
sequential = [check_host(h, attempts=1) for h in HOSTS]
sequential_time = time.perf_counter() - start

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    parallel = list(pool.map(check_host, HOSTS))
parallel_time = time.perf_counter() - start

for host, status, attempts in parallel:
    print(f"{host:<9} {status:<7} after {attempts} attempt(s)")
print(f"Sequential took ~{sequential_time:.1f}s, parallel took ~{parallel_time:.1f}s")
failed = [h for h, s, _ in parallel if s != "OK"]
exit_code = 1 if failed else 0
print("Exit code for CI:", exit_code, "| failed:", failed)   # real script: sys.exit(exit_code)
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- Three processes are chained by passing one command's `stdout` as the next command's `input` — a pipeline with no shell involved.
- The same result in pure Python is shorter and has no dependency on external tools; prefer it when the logic is simple.
- `Popen` starts the child immediately; iterating `proc.stdout` prints each line **as soon as** the child produces it (`flush=True` in the child avoids buffering). `proc.wait()` returns the exit code.

**Example 2**
- Each "host check" is a child process that takes 0.5 s and exits 0 or 1 — a stand-in for `ssh host systemctl is-active app` or `curl -f`.
- `check_host` retries on failure.
- Sequentially, 5 checks take ~2.5 s; with `ThreadPoolExecutor` they run at the same time (~1 s including db-01's retry).
- The final exit code tells CI whether to fail the job.

## 7. Expected Output

**Example 1:**

```text
uniq -c result:
      1 cache
      2 db
      3 web
Python result: {'cache': 1, 'db': 2, 'web': 3}
[live] step 1/3 done
[live] step 2/3 done
[live] step 3/3 done
exit code: 0
```

**Example 2:**

```text
web-01    OK      after 1 attempt(s)
web-02    OK      after 1 attempt(s)
db-01     FAILED  after 2 attempt(s)
cache-01  OK      after 1 attempt(s)
queue-01  OK      after 1 attempt(s)
Sequential took ~2.6s, parallel took ~1.1s
Exit code for CI: 1 | failed: ['db-01']
```

> ℹ️ Timings in Example 2 depend on your machine.

## 8. Common Mistakes

**1. Deadlocks with Popen**

Using `stdout=PIPE` and `stderr=PIPE` but only reading one can hang when a buffer fills. Merge with `stderr=STDOUT` or use `communicate()`.

**2. Too many parallel workers**

Hitting 500 servers at once can overload networks/APIs. Limit `max_workers`.

**3. Re-implementing tools badly**

If a robust tool exists (Ansible for SSH fan-out), use it. Python glue is great for orchestration and reporting.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Word frequency via pipeline:** Pass the text `"apple banana apple cherry banana apple"` (one word per line) to `sort` then `uniq -c` then `sort -rn` using `input=` chaining, and print the result.
- **Task 2 (Medium) — Live progress:** Use `Popen` to run a child Python process that prints `Downloading part N` for N = 1..4, and prefix each received line with a timestamp-free counter `[k]` in the parent. Print the exit code.
- **Task 3 (Practical Challenge) — Parallel command runner:** Write `run_all(commands, workers=3)` that runs a dict of name → command list in parallel and returns name → (returncode, first line of output). Use it with 4 commands: `uname -s`, `python --version` (via sys.executable), `ls /nonexistent`, `echo done`. Print a summary table sorted by name and count failures.

## 10. DevOps/MLOps Connection

- **DevOps:** orchestrating `docker build` → `docker push` → `kubectl apply` with live logs; checking many hosts/endpoints in parallel; retrying flaky network commands.
- **CI/CD:** custom pipeline steps that stream tool output into the CI log and fail correctly.
- **MLOps:** running several training/evaluation jobs in parallel with different parameters and collecting their results.

## 11. Interview Questions

**Q1. How do you read a subprocess's output while it is still running?**

<details><summary>Show answer</summary>

Use `subprocess.Popen(..., stdout=PIPE, text=True)` and iterate over `proc.stdout`.

</details>

**Q2. How can you avoid `shell=True` when you need a pipeline?**

<details><summary>Show answer</summary>

Run each command separately and pass `stdout` of one as `input` to the next, or use Popen with `stdin=prev.stdout`, or implement the filtering in Python.

</details>

**Q3. Why do threads speed up running many subprocesses despite the GIL?**

<details><summary>Show answer</summary>

The work happens in separate processes and threads mostly wait on I/O; the GIL is released while waiting.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 71 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 070](../../07-devops-automation/day-070/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 072 ➡](../../07-devops-automation/day-072/README.md)
