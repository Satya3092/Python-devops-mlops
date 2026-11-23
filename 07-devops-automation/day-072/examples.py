"""
Day 072 — Regular Expressions
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Regex fundamentals
# ======================================================================
import re

text = "Order 1042 shipped to 10.0.3.25 on 2026-11-20; order 1043 pending. Contact ops@example.com"

print("First number :", re.search(r"\d+", text).group())
print("All numbers  :", re.findall(r"\d+", text))
print("Dates        :", re.findall(r"\d{4}-\d{2}-\d{2}", text))
print("IPv4         :", re.findall(r"\b(?:\d{1,3}\.){3}\d{1,3}\b", text))
print("Email        :", re.search(r"[\w.+-]+@[\w-]+\.[\w.]+", text).group())

m = re.search(r"order (?P<id>\d+) (?P<state>\w+)", text, re.IGNORECASE)
print("Named groups :", m.group("id"), m.group("state"), m.groupdict())

print("Starts with 'Order'?", bool(re.match(r"Order", text)))
print("Masked       :", re.sub(r"\d{4}-\d{2}-\d{2}", "<DATE>", text)[:60])

# ======================================================================
# Example 2 — Parsing an access log and masking secrets
# ======================================================================
import re

ACCESS_LOG = """\
192.168.1.10 - - [20/Nov/2026:10:00:01 +0000] "GET /index.html HTTP/1.1" 200 512 "-" "curl/8.5"
10.0.0.5 - - [20/Nov/2026:10:00:04 +0000] "POST /api/login HTTP/1.1" 401 64 "-" "Mozilla/5.0"
10.0.0.9 - - [20/Nov/2026:10:00:09 +0000] "GET /api/orders?id=7 HTTP/1.1" 500 256 "-" "python-requests/2.32"
bad line without the right format
"""

LINE = re.compile(r"""
    ^(?P<ip>\d{1,3}(?:\.\d{1,3}){3})         # client IP
    \s-\s-\s
    \[(?P<time>[^\]]+)\]\s                    # [timestamp]
    "(?P<method>[A-Z]+)\s(?P<path>\S+)\s[^"]+"\s
    (?P<status>\d{3})\s(?P<size>\d+)          # status and size
""", re.VERBOSE)

for line in ACCESS_LOG.splitlines():
    m = LINE.match(line)
    if not m:
        print("SKIP:", line)
        continue
    d = m.groupdict()
    print(f"{d['ip']:<13} {d['method']:<5} {d['path']:<16} {d['status']} {d['size']:>4}B @ {d['time']}")

config_dump = "db_host=10.0.0.20 db_password=Sup3rS3cret api_token=ghp_abc123XYZ debug=true"
masked = re.sub(r"(?i)(password|token|secret)=\S+", r"\1=****", config_dump)
print("Masked config:", masked)

versions = ["v1.2.3", "1.10.0", "v2.0.0-rc.1", "release-7", "v3.1"]
semver = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([\w.]+))?$")
for v in versions:
    m = semver.match(v)
    print(f"{v:<12} ->", m.groups() if m else "not semver")
