# Day 074 — Python Script for Server Health Monitoring

[⬅ Day 073](../../07-devops-automation/day-073/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 075 ➡](../../07-devops-automation/day-075/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Combine psutil metrics, thresholds and HTTP/port checks into one health script
- Return proper exit codes for monitoring systems (Nagios-style)
- Output machine-readable JSON for dashboards and alerting

## 2. Topic Explanation

A good health-check script:

1. **Collects** metrics: CPU, memory, disk, load, and the state of important services (is port 5432 open? does `/health` return 200?).
2. **Evaluates** each against thresholds → `OK` / `WARNING` / `CRITICAL`.
3. **Reports** in two formats: human-readable text and JSON.
4. **Exits** with a meaningful code — the Nagios plugin convention, also used by many tools:

| Exit code | Meaning |
|---|---|
| 0 | OK |
| 1 | WARNING |
| 2 | CRITICAL |
| 3 | UNKNOWN (the check itself failed) |

Checking a TCP port uses the `socket` module: `socket.create_connection((host, port), timeout=2)` succeeds if something is listening.

Design tip: **separate collection from evaluation**. Functions that take metrics as input (instead of reading them) are easy to unit test with fake values.

## 3. Syntax

```python
import socket
with socket.create_connection((host, port), timeout=2):
    is_open = True

def evaluate(value, warning, critical): ...
sys.exit(worst_status_code)
```

| Part | Meaning |
|---|---|
| `socket.create_connection` | Opens a TCP connection; raises OSError if closed/unreachable. |
| `timeout` | Never wait forever on the network. |
| `exit code` | 0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN. |
| `pure evaluate()` | Logic that takes values as input — easy to test. |

## 4. Example 1 — Basic Example: Testable evaluation logic with fake metrics

```python
STATUS_CODE = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}
THRESHOLDS = {"cpu": (75, 90), "memory": (80, 90), "disk": (80, 90), "load_per_core": (1.0, 2.0)}


def evaluate(metric, value):
    warning, critical = THRESHOLDS[metric]
    if value is None:
        return "UNKNOWN"
    if value >= critical:
        return "CRITICAL"
    if value >= warning:
        return "WARNING"
    return "OK"


def overall(statuses):
    return max(statuses, key=STATUS_CODE.get)


fake_servers = {
    "web-01": {"cpu": 35.0, "memory": 61.2, "disk": 54.0, "load_per_core": 0.4},
    "web-02": {"cpu": 82.5, "memory": 71.0, "disk": 66.3, "load_per_core": 1.3},
    "db-01": {"cpu": 47.0, "memory": 93.4, "disk": 91.0, "load_per_core": 0.9},
    "new-vm": {"cpu": None, "memory": 20.0, "disk": 10.0, "load_per_core": 0.1},
}
for host, metrics in fake_servers.items():
    statuses = {m: evaluate(m, v) for m, v in metrics.items()}
    result = overall(statuses.values())
    problems = {m: s for m, s in statuses.items() if s != "OK"}
    print(f"{host:<7} {result:<9} exit={STATUS_CODE[result]}  {problems}")
```

## 5. Example 2 — Practical Example: Live health check: system metrics + ports + HTTP endpoint

```python
import json
import os
import socket
import sys
import threading
import urllib.request
from http.server import BaseHTTPRequestHandler, HTTPServer

import psutil

STATUS_CODE = {"OK": 0, "WARNING": 1, "CRITICAL": 2, "UNKNOWN": 3}


def level(value, warning, critical):
    return "CRITICAL" if value >= critical else "WARNING" if value >= warning else "OK"


def port_open(host, port, timeout=1.0):
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def http_ok(url, timeout=2.0):
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return response.status == 200
    except OSError:
        return False


# A tiny local web server so the HTTP check has something to talk to
class Health(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200 if self.path == "/health" else 404)
        self.end_headers()
        self.wfile.write(b"ok")

    def log_message(self, *args):
        pass


server = HTTPServer(("127.0.0.1", 0), Health)
threading.Thread(target=server.serve_forever, daemon=True).start()
app_port = server.server_address[1]

load_per_core = os.getloadavg()[0] / psutil.cpu_count() if hasattr(os, "getloadavg") else 0.0
checks = {
    "cpu": level(psutil.cpu_percent(interval=0.5), 75, 90),
    "memory": level(psutil.virtual_memory().percent, 80, 90),
    "disk": level(psutil.disk_usage("/").percent, 80, 90),
    "load": level(load_per_core, 1.0, 2.0),
    "app_port": "OK" if port_open("127.0.0.1", app_port) else "CRITICAL",
    "app_http": "OK" if http_ok(f"http://127.0.0.1:{app_port}/health") else "CRITICAL",
    "postgres_port": "OK" if port_open("127.0.0.1", 5432) else "WARNING",
}
server.shutdown()

worst = max(checks.values(), key=STATUS_CODE.get)
print(json.dumps({"host": socket.gethostname(), "status": worst, "checks": checks}, indent=2))
print("Nagios-style line:", f"{worst} - " + ", ".join(f"{k}={v}" for k, v in checks.items() if v != "OK"))
print("Would exit with code", STATUS_CODE[worst])   # real script: sys.exit(STATUS_CODE[worst])
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `evaluate` is a **pure function**: give it a metric and a value, get a status. No psutil needed, so it can be unit-tested with fake data.
- `overall` picks the worst status using the exit-code ordering. `None` (could not measure) becomes `UNKNOWN`.

**Example 2**
- A tiny `HTTPServer` runs in a background thread so the HTTP and port checks have a real target (your real check would point at your application).
- `port_open` and `http_ok` use timeouts and treat any `OSError` as "down".
- The result is printed as JSON (for dashboards/alerting) and as a one-line Nagios-style summary; the exit code follows the 0/1/2/3 convention.

## 7. Expected Output

**Example 1:**

```text
web-01  OK        exit=0  {}
web-02  WARNING   exit=1  {'cpu': 'WARNING', 'load_per_core': 'WARNING'}
db-01   CRITICAL  exit=2  {'memory': 'CRITICAL', 'disk': 'CRITICAL'}
new-vm  UNKNOWN   exit=3  {'cpu': 'UNKNOWN'}
```

**Example 2:**

```text
{
  "host": "ip-10-0-1-25",
  "status": "WARNING",
  "checks": {
    "cpu": "OK",
    "memory": "OK",
    "disk": "OK",
    "load": "OK",
    "app_port": "OK",
    "app_http": "OK",
    "postgres_port": "WARNING"
  }
}
Nagios-style line: WARNING - postgres_port=WARNING
Would exit with code 1
```

> ℹ️ Example 2 and Task 3 read live values; the output shown is a sample. If PostgreSQL is running locally, `postgres_port` will be OK.

## 8. Common Mistakes

**1. Checks without timeouts**

A hanging network check makes the monitor itself hang. Always set timeouts.

**2. Exit code 0 on failure**

Monitoring systems and CI read exit codes. Return non-zero for problems.

**3. Mixing collection and logic**

If thresholds logic reads psutil directly, you can't test it. Pass values into pure functions.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Port checker:** Write `check_ports(host, ports)` returning a dict port → open/closed using `socket.create_connection` with a 0.5 s timeout. Start a local server socket on a free port in the solution so at least one port is open, and check it plus port 1.
- **Task 2 (Medium) — Threshold function tests:** Write `classify(value, warning, critical)` and test it with `assert` statements for at least 5 cases (below warning, equal to warning, between, equal to critical, above). Print `all tests passed`.
- **Task 3 (Practical Challenge) — Health check with exit codes:** Write `health_check(metrics, thresholds)` that returns (status, exit_code, problems) for a metrics dict. Run it for two fake servers and once for live psutil values `{cpu, memory, disk}`.

## 10. DevOps/MLOps Connection

- **DevOps / Monitoring:** custom checks for Nagios/Icinga/Zabbix, Kubernetes liveness/readiness probe scripts, Consul health checks, synthetic monitoring.
- **Cloud:** run the script on a schedule and push results as CloudWatch custom metrics; alarms trigger SNS/Slack.
- **MLOps:** model-server health = process up + `/health` endpoint OK + latency below threshold + model loaded.

## 11. Interview Questions

**Q1. What exit codes do Nagios-compatible checks use?**

<details><summary>Show answer</summary>

0 OK, 1 WARNING, 2 CRITICAL, 3 UNKNOWN.

</details>

**Q2. How do you check if a TCP port is open in Python?**

<details><summary>Show answer</summary>

`socket.create_connection((host, port), timeout=...)` inside try/except OSError.

</details>

**Q3. What's the difference between liveness and readiness probes?**

<details><summary>Show answer</summary>

Liveness: is the process alive (restart if not)? Readiness: can it serve traffic now (remove from load balancing if not)?

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 74 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 073](../../07-devops-automation/day-073/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 075 ➡](../../07-devops-automation/day-075/README.md)
