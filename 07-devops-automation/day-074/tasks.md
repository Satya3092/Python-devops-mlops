# Day 074 — Practice Tasks: Python Script for Server Health Monitoring

> 💡 **Try every task on your own first.** Create a file such as `my_solution.py` in this folder.
> Only open [`solutions/solution.py`](solutions/solution.py) after you have made a real attempt.

⬅ Back to the [lesson](README.md)

## Task 1 — Easy: Port checker

**Problem statement:** Write `check_ports(host, ports)` returning a dict port → open/closed using `socket.create_connection` with a 0.5 s timeout. Start a local server socket on a free port in the solution so at least one port is open, and check it plus port 1.

**Input requirements:** No user input required.

**Expected behavior:** The started port is open, port 1 is closed.

**Expected output:**

```text
listening port: open | port 1: closed
```

## Task 2 — Medium: Threshold function tests

**Problem statement:** Write `classify(value, warning, critical)` and test it with `assert` statements for at least 5 cases (below warning, equal to warning, between, equal to critical, above). Print `all tests passed`.

**Input requirements:** No user input required.

**Expected behavior:** Prints `all tests passed`.

**Expected output:**

```text
all tests passed
```

## Task 3 — Practical Challenge: Health check with exit codes

**Problem statement:** Write `health_check(metrics, thresholds)` that returns (status, exit_code, problems) for a metrics dict. Run it for two fake servers and once for live psutil values `{cpu, memory, disk}`.

**Input requirements:** No user input required.

**Expected behavior:** Status lines for each run.

**Expected output:**

```text
web-01: OK (exit 0)
db-01: CRITICAL (exit 2) -> disk=CRITICAL
{"cpu": 7.0, "memory": 38.4, "disk": 44.4}
Local check: OK (exit 0)
```

---

When you are done, tick the tasks off in the lesson's [completion checklist](README.md#12-day-completion-checklist).
