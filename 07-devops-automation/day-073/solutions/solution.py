"""
Day 073 — Python Automation for Log Analysis: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

LINE = re.compile(r"^(?P<ts>\S+ \S+) (?P<level>INFO|WARNING|ERROR) \[(?P<ip>[\d.]+)\] (?P<msg>.+)$")
records = [m.groupdict() for m in map(LINE.match, Path("../../datasets/app.log").read_text().splitlines()) if m]

# ===== Task 1 =====
print(Counter(r["level"] for r in records))

# ===== Task 2 =====
per_ip = defaultdict(Counter)
for r in records:
    per_ip[r["ip"]][r["level"]] += 1
for ip, c in sorted(per_ip.items(), key=lambda kv: kv[1]["ERROR"], reverse=True):
    total = sum(c.values())
    print(f"{ip:<14} errors={c['ERROR']:<3} of {total:<3} ({c['ERROR'] / total * 100:.0f}%)")

# ===== Task 3 =====
failed = Counter(re.search(r"user=(\w+)", r["msg"]).group(1) for r in records if "Failed login" in r["msg"])
print("Failed logins per user:", dict(failed))


def minutes(ts):
    h, m = ts[11:16].split(":")
    return int(h) * 60 + int(m)


deployments = [r for r in records if r["msg"].startswith("Deployment")]
for d in deployments:
    start = minutes(d["ts"])
    errors_after = sum(1 for r in records if r["level"] == "ERROR" and 0 <= minutes(r["ts"]) - start <= 2)
    print(f"{d['ts'][11:]}  {d['msg']:<24} errors in next 2 min: {errors_after}")
