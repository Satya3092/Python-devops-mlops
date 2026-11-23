"""
Day 008 — Comparison Operators
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Basic comparisons
# ======================================================================
cpu = 75
print("cpu == 75:", cpu == 75)
print("cpu != 75:", cpu != 75)
print("cpu > 80:", cpu > 80)
print("cpu <= 80:", cpu <= 80)
print("60 <= cpu < 80:", 60 <= cpu < 80)
print("'prod' == 'Prod':", "prod" == "Prod")
print("'apple' < 'banana':", "apple" < "banana")

# ======================================================================
# Example 2 — Health-check thresholds
# ======================================================================
CPU_LIMIT = 80
MEMORY_LIMIT = 90
EXPECTED_VERSION = "1.4.2"

cpu_usage = 83
memory_usage = 64
deployed_version = "1.4.1"
http_status = 200

cpu_alert = cpu_usage > CPU_LIMIT
memory_alert = memory_usage >= MEMORY_LIMIT
version_drift = deployed_version != EXPECTED_VERSION
is_success = 200 <= http_status < 300

print("CPU alert:", cpu_alert)
print("Memory alert:", memory_alert)
print("Version drift detected:", version_drift)
print("HTTP success:", is_success)
