"""
Day 050 — Working with CSV Files
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Writing and reading a CSV file
# ======================================================================
import csv

rows = [
    ["name", "role", "city"],
    ["Asha", "DevOps Engineer", "Pune"],
    ["Ravi", "SRE", "Bengaluru"],
    ["Meera", "ML Engineer", "Hyderabad, Telangana"],   # contains a comma!
]

with open("team.csv", "w", newline="", encoding="utf-8") as f:
    csv.writer(f).writerows(rows)

with open("team.csv", encoding="utf-8") as f:
    print("Raw file:")
    print(f.read(), end="")

with open("team.csv", newline="", encoding="utf-8") as f:
    reader = csv.reader(f)
    header = next(reader)
    print("Header:", header)
    for row in reader:
        print(row)

# ======================================================================
# Example 2 — Server utilisation report from a CSV
# ======================================================================
import csv

servers = [
    {"hostname": "web-01", "env": "prod", "cpu": 45, "memory": 62, "monthly_cost": 70.08},
    {"hostname": "web-02", "env": "prod", "cpu": 91, "memory": 88, "monthly_cost": 70.08},
    {"hostname": "db-01", "env": "prod", "cpu": 58, "memory": 93, "monthly_cost": 280.32},
    {"hostname": "test-01", "env": "dev", "cpu": 3, "memory": 10, "monthly_cost": 140.16},
]
with open("servers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(servers[0].keys()))
    writer.writeheader()
    writer.writerows(servers)

# Read it back as dicts and analyse
alerts, idle = [], []
total_cost = 0.0
with open("servers.csv", newline="", encoding="utf-8") as f:
    for row in csv.DictReader(f):
        cpu, memory = int(row["cpu"]), int(row["memory"])
        cost = float(row["monthly_cost"])
        total_cost += cost
        if cpu > 85 or memory > 90:
            alerts.append({"hostname": row["hostname"], "cpu": cpu, "memory": memory})
        if cpu < 5:
            idle.append((row["hostname"], cost))

print(f"Total monthly cost: ${total_cost:.2f}")
print("Idle servers (save money):", idle)

with open("alerts.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["hostname", "cpu", "memory"])
    writer.writeheader()
    writer.writerows(alerts)

with open("alerts.csv", encoding="utf-8") as f:
    print("alerts.csv:")
    print(f.read(), end="")
