"""
Day 072 — Regular Expressions: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import re

# ===== Task 1 =====
print(re.findall(r"#\w+", "Learning #Python for #DevOps and #MLOps #100DaysOfCode"))

# ===== Task 2 =====
HOSTNAME = re.compile(r"^[a-z0-9](?:[a-z0-9-]{1,18})[a-z0-9]$")


def is_valid_hostname(name):
    return bool(HOSTNAME.match(name))


for name in ["web-01", "db-prod-3", "-bad", "UPPER", "ab"]:
    print(f"{name:<10} {is_valid_hostname(name)}")

# ===== Task 3 =====
EVENT = re.compile(r"^(?P<age>\d+[smhd])\s+(?P<type>Normal|Warning)\s+(?P<reason>\w+)\s+(?P<object>\S+)\s+(?P<message>.+)$")
lines = [
    "5m Warning BackOff pod/api-7d9f Back-off restarting failed container",
    "2m Normal Pulled pod/api-7d9f Successfully pulled image",
    "30s Warning FailedScheduling pod/worker-1 0/3 nodes are available",
]
reasons = {}
for line in lines:
    event = EVENT.match(line).groupdict()
    reasons[event["reason"]] = reasons.get(event["reason"], 0) + 1
    if event["type"] == "Warning":
        print(event)
print(reasons)
