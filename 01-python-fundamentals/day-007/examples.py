"""
Day 007 — Arithmetic Operators
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — All arithmetic operators
# ======================================================================
a = 17
b = 5
print("a + b  =", a + b)
print("a - b  =", a - b)
print("a * b  =", a * b)
print("a / b  =", a / b)
print("a // b =", a // b)
print("a % b  =", a % b)
print("a ** 2 =", a ** 2)
print("divmod(a, b) =", divmod(a, b))

# ======================================================================
# Example 2 — Capacity planning and uptime
# ======================================================================
# How many nodes do we need for 23 pods if each node fits 4 pods?
total_pods = 23
pods_per_node = 4
full_nodes = total_pods // pods_per_node
leftover_pods = total_pods % pods_per_node
nodes_needed = full_nodes + (1 if leftover_pods > 0 else 0)
print("Full nodes:", full_nodes, "| leftover pods:", leftover_pods)
print("Nodes needed:", nodes_needed)

# Convert uptime in seconds to days, hours, minutes
uptime_seconds = 400_000
days, remainder = divmod(uptime_seconds, 86_400)
hours, remainder = divmod(remainder, 3_600)
minutes = remainder // 60
print("Uptime:", days, "days", hours, "hours", minutes, "minutes")

# Storage growth: 50 GB growing 10% per month for 12 months
storage_gb = 50 * 1.10 ** 12
print("Storage after 12 months:", round(storage_gb, 1), "GB")
