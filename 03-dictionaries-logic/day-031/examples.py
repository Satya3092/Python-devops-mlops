"""
Day 031 — Range Function
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — range variations
# ======================================================================
print(list(range(5)))
print(list(range(1, 6)))
print(list(range(0, 20, 5)))
print(list(range(10, 0, -2)))
print("Length of range(1, 100):", len(range(1, 100)))

for i in range(3):
    print("Hello number", i)

total = 0
for n in range(1, 101):
    total += n
print("Sum 1..100 =", total)

# ======================================================================
# Example 2 — Generating names, IPs and port ranges
# ======================================================================
# Generate 5 worker hostnames: worker-01 ... worker-05
hostnames = [f"worker-{n:02d}" for n in range(1, 6)]
print(hostnames)

# Assign IP addresses from 10.0.1.10 upwards
for offset, host in enumerate(hostnames):
    print(f"{host} -> 10.0.1.{10 + offset}")

# Every 15 minutes in an hour (cron-like schedule)
print("Backup minutes:", list(range(0, 60, 15)))

# Port range for NodePort services (sample of the first five)
node_ports = range(30000, 32768)
print("Number of NodePorts available:", len(node_ports))
print("First five:", list(node_ports[:5]))

# Countdown before a maintenance window
for minutes_left in range(15, 0, -5):
    print(f"Maintenance starts in {minutes_left} minutes")
