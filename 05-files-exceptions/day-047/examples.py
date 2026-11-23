"""
Day 047 — Reading Files
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Different ways to read
# ======================================================================
with open("requirements_sample.txt", encoding="utf-8") as f:
    whole = f.read()
print("read() ->", len(whole), "characters")

with open("requirements_sample.txt", encoding="utf-8") as f:
    first_line = f.readline()
    second_line = f.readline()
print("readline() ->", repr(first_line), repr(second_line))

with open("requirements_sample.txt", encoding="utf-8") as f:
    lines = f.readlines()
print("readlines() ->", len(lines), "lines")

packages = []
with open("requirements_sample.txt", encoding="utf-8") as f:
    for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        name, version = line.split("==")
        packages.append((name, version))
print("Pinned packages:", packages)

# ======================================================================
# Example 2 — Analysing an nginx access log line by line
# ======================================================================
status_counts = {}
bytes_total = 0
ip_hits = {}
errors = []

with open("nginx_access.log", encoding="utf-8") as log_file:
    for line_number, line in enumerate(log_file, start=1):
        parts = line.split()
        ip = parts[0]
        method = parts[4].strip('"')
        path = parts[5]
        status = int(parts[7])
        size = int(parts[8])

        status_counts[status] = status_counts.get(status, 0) + 1
        ip_hits[ip] = ip_hits.get(ip, 0) + 1
        bytes_total += size
        if status >= 400:
            errors.append(f"line {line_number}: {status} {method} {path} from {ip}")

print("Requests by status:", dict(sorted(status_counts.items())))
print("Total bytes served:", bytes_total)
top_ip = max(ip_hits, key=ip_hits.get)
print(f"Top client: {top_ip} ({ip_hits[top_ip]} requests)")
print("Errors:")
for e in errors:
    print("  ", e)
