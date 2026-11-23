"""
Day 073 — Python Automation for Log Analysis
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Parse and count with Counter
# ======================================================================
import re
from collections import Counter
from pathlib import Path

LOG_PATH = Path("../../datasets/app.log")
LINE = re.compile(r"^(?P<ts>\S+ \S+) (?P<level>INFO|WARNING|ERROR) \[(?P<ip>[\d.]+)\] (?P<msg>.+)$")

records = []
with LOG_PATH.open(encoding="utf-8") as f:
    for line in f:
        m = LINE.match(line.strip())
        if m:
            records.append(m.groupdict())

print("Parsed records:", len(records))
levels = Counter(r["level"] for r in records)
print("By level:", dict(levels))
print("Top IPs:", Counter(r["ip"] for r in records).most_common(2))
print("First record:", records[0])

# ======================================================================
# Example 2 — Full analysis: windows, anomalies and a JSON report
# ======================================================================
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

LOG_PATH = Path("../../datasets/app.log")
LINE = re.compile(r"^(?P<ts>\S+ \S+) (?P<level>INFO|WARNING|ERROR) \[(?P<ip>[\d.]+)\] (?P<msg>.+)$")
MS = re.compile(r"(\d+)ms")
USER = re.compile(r"user=(\w+)")
ERROR_RATE_LIMIT = 15.0          # percent
SLOW_MS = 2000


def parse(path):
    for line in path.read_text(encoding="utf-8").splitlines():
        m = LINE.match(line)
        if m:
            yield m.groupdict()


def analyse(records):
    levels = Counter()
    per_minute = defaultdict(Counter)
    error_messages = Counter()
    failed_logins = Counter()
    slow = []
    for r in records:
        levels[r["level"]] += 1
        per_minute[r["ts"][:16]][r["level"]] += 1
        if r["level"] == "ERROR":
            error_messages[MS.sub("<N>ms", r["msg"])] += 1     # normalise numbers
        if "Failed login" in r["msg"]:
            failed_logins[USER.search(r["msg"]).group(1)] += 1
        ms = MS.search(r["msg"])
        if ms and int(ms.group(1)) >= SLOW_MS:
            slow.append((r["ts"], int(ms.group(1)), r["msg"]))
    total = sum(levels.values())
    error_rate = levels["ERROR"] / total * 100
    busiest_minute = max(per_minute, key=lambda m: per_minute[m]["ERROR"])
    return {
        "total": total,
        "levels": dict(levels),
        "error_rate_percent": round(error_rate, 1),
        "alert": error_rate > ERROR_RATE_LIMIT,
        "top_errors": error_messages.most_common(3),
        "failed_logins": dict(failed_logins),
        "worst_minute": {"minute": busiest_minute, "errors": per_minute[busiest_minute]["ERROR"]},
        "slow_requests": len(slow),
        "slowest": max(slow, key=lambda s: s[1])[:2] if slow else None,
    }


report = analyse(parse(LOG_PATH))
print(f"Lines analysed : {report['total']}")
print(f"Levels         : {report['levels']}")
print(f"Error rate     : {report['error_rate_percent']}%  ALERT={report['alert']}")
print("Top errors     :")
for message, count in report["top_errors"]:
    print(f"   {count} x {message}")
print(f"Failed logins  : {report['failed_logins']}")
print(f"Worst minute   : {report['worst_minute']}")
print(f"Slow requests  : {report['slow_requests']} (slowest {report['slowest']})")

Path("log_report.json").write_text(json.dumps(report, indent=2))
print("Saved log_report.json with keys:", list(json.loads(Path("log_report.json").read_text())))
