"""
Day 033 — Nested Loops
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Multiplication grid
# ======================================================================
for row in range(1, 4):
    line = ""
    for col in range(1, 6):
        line += f"{row * col:4}"
    print(line)

pattern_rows = 4
for i in range(1, pattern_rows + 1):
    stars = ""
    for _ in range(i):
        stars += "*"
    print(stars)

# ======================================================================
# Example 2 — Deployment matrix and duplicate detection
# ======================================================================
environments = ["dev", "staging", "prod"]
regions = ["us-east-1", "eu-west-1"]
services = ["api", "worker"]

count = 0
for env in environments:
    for region in regions:
        for service in services:
            count += 1
            print(f"{count:2}. deploy {service:<7} -> {env:<8} @ {region}")
print("Total deployments:", count)

# Find servers that share the same IP (configuration error)
servers = [("web-01", "10.0.0.5"), ("web-02", "10.0.0.6"), ("db-01", "10.0.0.5")]
for i in range(len(servers)):
    for j in range(i + 1, len(servers)):          # compare each pair once
        if servers[i][1] == servers[j][1]:
            print(f"IP conflict: {servers[i][0]} and {servers[j][0]} both use {servers[i][1]}")
