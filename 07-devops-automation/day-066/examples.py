"""
Day 066 — Python System Administration Automation
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Collecting system facts
# ======================================================================
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

# ======================================================================
# Example 2 — Idempotent generation of a systemd unit and a cron entry
# ======================================================================
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
