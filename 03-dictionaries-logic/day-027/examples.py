"""
Day 027 — Dictionary Methods
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Looping and modifying
# ======================================================================
ports = {"ssh": 22, "http": 80, "https": 443}

print("Keys:", list(ports.keys()))
print("Values:", list(ports.values()))
for service, port in ports.items():
    print(f"  {service:<6} -> {port}")

ports.update({"postgres": 5432, "http": 8080})
print("After update:", ports)

removed = ports.pop("ssh")
print("Removed ssh port:", removed)

ports.setdefault("redis", 6379)
print("After setdefault:", ports)

defaults = {"timeout": 30, "retries": 3}
custom = {"retries": 5}
print("Merged with |:", defaults | custom)

# ======================================================================
# Example 2 — Counting log levels and grouping by host
# ======================================================================
log_lines = [
    "web-01 INFO Request served",
    "web-02 ERROR Connection refused",
    "web-01 WARNING Slow response",
    "web-03 INFO Request served",
    "web-02 ERROR Timeout",
    "web-01 INFO Health check ok",
    "web-02 INFO Request served",
]

level_counts = {}
errors_by_host = {}
for line in log_lines:
    host, level, message = line.split(" ", 2)
    level_counts[level] = level_counts.get(level, 0) + 1
    if level == "ERROR":
        errors_by_host.setdefault(host, []).append(message)

print("Log level counts:")
for level, count in level_counts.items():
    print(f"  {level:<8}{count}")

print("Errors grouped by host:")
for host, messages in errors_by_host.items():
    print(f"  {host}: {messages}")

most_common = max(level_counts, key=level_counts.get)
print("Most common level:", most_common)
