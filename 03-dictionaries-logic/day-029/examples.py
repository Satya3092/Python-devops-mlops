"""
Day 029 — For Loops
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Looping over different collections
# ======================================================================
for letter in "Py":
    print("Letter:", letter)

fruits = ["apple", "mango", "banana"]
for fruit in fruits:
    print("I like", fruit)

for number, fruit in enumerate(fruits, start=1):
    print(number, fruit)

prices = [40, 90, 15]
for fruit, price in zip(fruits, prices):
    print(f"{fruit} costs {price}")

stock = {"apple": 10, "mango": 0}
for item, quantity in stock.items():
    print(item, "in stock" if quantity > 0 else "SOLD OUT")

# ======================================================================
# Example 2 — Checking a fleet of servers
# ======================================================================
servers = [
    {"name": "web-01", "cpu": 45, "disk": 60, "status": "running"},
    {"name": "web-02", "cpu": 92, "disk": 71, "status": "running"},
    {"name": "db-01", "cpu": 30, "disk": 94, "status": "running"},
    {"name": "batch-01", "cpu": 0, "disk": 20, "status": "stopped"},
]

alerts = []
total_cpu = 0
running = 0

for number, server in enumerate(servers, start=1):
    print(f"[{number}/{len(servers)}] Checking {server['name']}...")
    if server["status"] != "running":
        print("    skipped (not running)")
        continue                       # skip to the next server (Day 32)
    running += 1
    total_cpu += server["cpu"]
    if server["cpu"] > 90:
        alerts.append(f"{server['name']}: CPU {server['cpu']}%")
    if server["disk"] > 90:
        alerts.append(f"{server['name']}: disk {server['disk']}%")

print(f"Average CPU of running servers: {total_cpu / running:.1f}%")
print("Alerts:")
for alert in alerts:
    print("  -", alert)
