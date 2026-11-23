# Day 066 — Python System Administration Automation

[⬅ Day 065](../../06-modules-oop/day-065/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 067 ➡](../../07-devops-automation/day-067/README.md)

| Phase | Difficulty | Estimated time |
|---|---|---|
| 7 — Python for DevOps Automation | 🟠 Intermediate+ | 60–90 min |

## 1. Learning Objectives

By the end of today you will be able to:

- Collect basic system facts with `platform`, `socket`, `getpass` and `os`
- Generate system configuration files (systemd units, cron entries) from Python
- Write idempotent admin scripts that check before they change

## 2. Topic Explanation

System administrators repeat the same tasks: check facts about a machine, make sure tools are installed, generate service files, schedule jobs, clean up. Python turns these into **repeatable, testable scripts**.

Useful standard-library modules:

| Module | Gives you |
|---|---|
| `platform` | OS name, release, architecture, Python version |
| `socket` | hostname, IP lookups |
| `getpass` | current user name (and hidden password prompts) |
| `os` | CPU count, load average, environment, permissions |
| `shutil` | `which`, disk usage |
| `pwd` / `grp` (Linux) | users and groups (`/etc/passwd`, `/etc/group`) |

**Idempotency** — a key DevOps idea from Ansible and Terraform: running a script twice should give the same result as running it once. So admin scripts **check the current state first** ("is the file already correct?") and only change what is different.

Today you will write a facts collector (like `ansible -m setup`) and a generator for systemd units and cron entries that only rewrites files when the content changes.

## 3. Syntax

```python
import platform, socket, getpass, os
platform.system(), platform.release(), platform.machine()
socket.gethostname()
getpass.getuser()
os.cpu_count(), os.getloadavg()          # getloadavg: Linux/macOS
```

| Part | Meaning |
|---|---|
| `platform.*` | Operating system and hardware details. |
| `socket.gethostname()` | The machine's hostname. |
| `getpass.getuser()` | The user running the script. |
| `os.getloadavg()` | 1, 5 and 15-minute load averages (Unix). |
| `idempotent write` | Compare new content with existing content before writing. |

## 4. Example 1 — Basic Example: Collecting system facts

```python
import getpass
import os
import platform
import shutil
import socket
import sys


def gather_facts():
    """Return a dict of facts about this machine (like 'ansible -m setup')."""
    facts = {
        "hostname": socket.gethostname(),
        "user": getpass.getuser(),
        "os": platform.system(),
        "kernel": platform.release(),
        "architecture": platform.machine(),
        "python": platform.python_version(),
        "cpu_count": os.cpu_count(),
        "is_root": hasattr(os, "geteuid") and os.geteuid() == 0,
    }
    if hasattr(os, "getloadavg"):
        facts["load_average"] = tuple(round(x, 2) for x in os.getloadavg())
    facts["tools"] = {tool: bool(shutil.which(tool)) for tool in ["git", "docker", "kubectl", "terraform"]}
    return facts


for key, value in gather_facts().items():
    print(f"{key:<13}: {value}")
print("Script run with:", sys.executable.split("/")[-1])
```

## 5. Example 2 — Practical Example: Idempotent generation of a systemd unit and a cron entry

```python
from pathlib import Path

UNIT_TEMPLATE = """[Unit]
Description={description}
After=network.target

[Service]
User={user}
WorkingDirectory={workdir}
ExecStart={python} {script}
Restart=on-failure
Environment=APP_ENV={env}

[Install]
WantedBy=multi-user.target
"""


def write_if_changed(path, content):
    """Write only when content differs. Returns 'created', 'updated' or 'unchanged'."""
    path = Path(path)
    if path.exists() and path.read_text() == content:
        return "unchanged"
    state = "updated" if path.exists() else "created"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content)
    return state


def cron_line(minute, hour, command, comment):
    return f"{minute} {hour} * * * {command}  # {comment}\n"


settings = {"description": "Orders API", "user": "appuser", "workdir": "/opt/orders",
            "python": "/opt/orders/.venv/bin/python", "script": "app.py", "env": "prod"}

out_dir = Path("generated")                     # real target: /etc/systemd/system
unit = UNIT_TEMPLATE.format(**settings)
print("1st run:", write_if_changed(out_dir / "orders-api.service", unit))
print("2nd run:", write_if_changed(out_dir / "orders-api.service", unit))
settings["env"] = "staging"
print("changed :", write_if_changed(out_dir / "orders-api.service", UNIT_TEMPLATE.format(**settings)))

cron = cron_line(30, 2, "/opt/orders/.venv/bin/python /opt/orders/backup.py", "nightly backup")
print("cron    :", write_if_changed(out_dir / "orders-backup.cron", cron))
print()
print((out_dir / "orders-api.service").read_text())
print("Next steps on a real server: sudo systemctl daemon-reload && sudo systemctl enable --now orders-api")
```

Both examples are in [`examples.py`](examples.py). Run them with `python examples.py`.

## 6. Code Explanation

**Example 1**
- `gather_facts` returns a dict, so the same function can feed a report, a JSON API or a CMDB.
- `hasattr(os, "geteuid")` / `hasattr(os, "getloadavg")` make the script safe on Windows, where those functions don't exist.
- `shutil.which` checks for required tools.

**Example 2**
- The unit file is a **template** filled with `.format(**settings)`.
- `write_if_changed` makes the script **idempotent**: the second run reports `unchanged` and doesn't touch the file (so no needless service restarts).
- Changing a setting triggers `updated`. This is exactly how Ansible's `template` module reports `changed`.
- Files are written to `generated/` for safety; on a server you'd write to `/etc/systemd/system` with root permissions.

## 7. Expected Output

**Example 1:**

```text
hostname     : ip-10-0-1-25
user         : ubuntu
os           : Linux
kernel       : 6.8.0-1018-aws
architecture : x86_64
python       : 3.12.3
cpu_count    : 2
is_root      : False
load_average : (0.12, 0.08, 0.05)
tools        : {'git': True, 'docker': True, 'kubectl': False, 'terraform': True}
Script run with: python3
```

**Example 2:**

```text
1st run: created
2nd run: unchanged
changed : updated
cron    : created

[Unit]
Description=Orders API
After=network.target

[Service]
User=appuser
WorkingDirectory=/opt/orders
ExecStart=/opt/orders/.venv/bin/python app.py
Restart=on-failure
Environment=APP_ENV=staging

[Install]
WantedBy=multi-user.target

Next steps on a real server: sudo systemctl daemon-reload && sudo systemctl enable --now orders-api
```

> ℹ️ Example 1 shows sample output from an Ubuntu EC2 instance; your machine's facts will differ.

## 8. Common Mistakes

**1. Running admin scripts as root by default**

Only elevate (sudo) for the steps that need it. Check `os.geteuid() == 0` and fail with a clear message when root is required.

**2. Non-idempotent scripts**

Appending a cron line on every run creates duplicates. Check for existing content first.

**3. Platform assumptions**

`os.getloadavg`, `pwd` and `/proc` don't exist on Windows. Guard with `hasattr` or `platform.system()`.

## 9. Practice Tasks

Full details, sample input and expected output are in [`tasks.md`](tasks.md). Solutions are kept separately in [`solutions/solution.py`](solutions/solution.py) — try first!

- **Task 1 (Easy) — Facts summary:** Print a one-line summary like `ubuntu@web-01 | Linux 6.8 | 4 CPUs | Python 3.12.3` using `getpass`, `socket`, `platform` and `os`.
- **Task 2 (Medium) — Users with login shells (Linux):** Parse a sample `/etc/passwd` content (given as a string in the solution) and list users whose shell is `/bin/bash` or `/bin/zsh` with their UID and home directory. Skip system users (UID < 1000) except root.
- **Task 3 (Practical Challenge) — Idempotent hosts-file manager:** Write `ensure_host_entry(path, ip, hostname)` that adds `ip hostname` to a hosts-style file only if that hostname isn't already present, and updates the IP if the hostname exists with a different IP. Return `added`, `updated` or `unchanged`. Demonstrate all three on a sample file.

## 10. DevOps/MLOps Connection

- **DevOps:** fact gathering, bootstrap scripts, generating service units and cron jobs — the building blocks of configuration management.
- **Cloud:** EC2 user-data and AMI build scripts (Packer) often run Python to configure instances idempotently.
- **MLOps:** preparing GPU/inference hosts (drivers present? enough disk? correct Python?) before deploying model servers.

## 11. Interview Questions

**Q1. What does idempotent mean in automation?**

<details><summary>Show answer</summary>

Running the operation multiple times has the same effect as running it once — scripts check current state and only change what's different.

</details>

**Q2. How can a Python script check if it is running as root?**

<details><summary>Show answer</summary>

On Unix, `os.geteuid() == 0`.

</details>

**Q3. Why generate config files from templates instead of editing them by hand?**

<details><summary>Show answer</summary>

Consistency across servers, version control of the template and variables, fewer typos and easy re-generation.

</details>

## 12. Day Completion Checklist

- [ ] Understood the concept
- [ ] Practiced Example 1
- [ ] Practiced Example 2
- [ ] Completed Task 1
- [ ] Completed Task 2
- [ ] Completed Task 3
- [ ] Answered the interview questions without peeking
- [ ] Ticked Day 66 in the [main progress tracker](../../README.md#-100-day-progress-tracker)

---

[⬅ Day 065](../../06-modules-oop/day-065/README.md) | [📚 Phase 7: Python for DevOps Automation](../README.md) | [🏠 Home](../../README.md) | [Day 067 ➡](../../07-devops-automation/day-067/README.md)
