"""
Day 028 — Nested Lists and Nested Dictionaries
Examples for 100 Days of Python: From Beginner to DevOps and MLOps.

Run:  python examples.py
"""

# ======================================================================
# Example 1 — Nested list (matrix) and nested dict
# ======================================================================
# CPU usage of 3 servers measured at 4 points in time
cpu_matrix = [
    [20, 35, 50, 40],   # web-01
    [70, 85, 90, 95],   # web-02
    [10, 15, 12, 18],   # db-01
]
print("web-02 at time 3:", cpu_matrix[1][2])
print("All readings for db-01:", cpu_matrix[2])
print("Max of web-02:", max(cpu_matrix[1]))

user = {
    "name": "asha",
    "groups": ["devops", "docker"],
    "address": {"city": "Pune", "country": "India"},
}
print("City:", user["address"]["city"])
print("First group:", user["groups"][0])
user["groups"].append("sudo")
print("Groups now:", user["groups"])

# ======================================================================
# Example 2 — Exploring a cloud-style inventory response
# ======================================================================
inventory = {
    "region": "ap-south-1",
    "instances": [
        {"id": "i-001", "type": "t3.micro", "state": "running",
         "tags": {"Name": "web-01", "Env": "prod"}},
        {"id": "i-002", "type": "t3.large", "state": "stopped",
         "tags": {"Name": "batch-01", "Env": "dev"}},
        {"id": "i-003", "type": "m5.xlarge", "state": "running",
         "tags": {"Name": "db-01"}},                  # no Env tag!
    ],
}

print(f"Region: {inventory['region']}")
print(f"{'ID':<7}{'NAME':<10}{'TYPE':<11}{'STATE':<9}ENV")
running_count = 0
for instance in inventory["instances"]:
    name = instance["tags"].get("Name", "-")
    env = instance["tags"].get("Env", "MISSING")
    print(f"{instance['id']:<7}{name:<10}{instance['type']:<11}{instance['state']:<9}{env}")
    if instance["state"] == "running":
        running_count += 1

print("Running instances:", running_count)
untagged = [i["id"] for i in inventory["instances"] if "Env" not in i["tags"]]
print("Instances missing an Env tag:", untagged)

# Safe navigation for optional nested keys
monitoring = inventory.get("settings", {}).get("monitoring", "disabled")
print("Monitoring:", monitoring)
