"""
Day 024 — Tuples: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
data_centre = (19.07, 72.87)
lat, lon = data_centre
print(f"Data centre at lat {lat}, lon {lon}")

# ===== Task 2 =====
v1 = tuple(int(p) for p in "1.10.2".split("."))
v2 = tuple(int(p) for p in "1.9.8".split("."))
if v1 > v2:
    print(f"{v1} is newer than {v2}")
else:
    print(f"{v2} is newer than {v1}")

# ===== Task 3 =====
inventory = [
    ("web-01", "10.0.1.10", 4, 8, "web"),
    ("web-02", "10.0.1.11", 4, 8, "web"),
    ("db-01", "10.0.2.10", 16, 64, "db"),
    ("db-02", "10.0.2.11", 16, 64, "db"),
]
total_cores = 0
total_memory = 0
for hostname, ip, cores, memory, role in inventory:
    print(f"{hostname:<8} {ip:<12} {cores:>3} cores {memory:>3} GB  {role}")
    total_cores += cores
    total_memory += memory
print(f"Total: {total_cores} cores, {total_memory} GB")
db_hosts = []
for hostname, *_, role in inventory:
    if role == "db":
        db_hosts.append(hostname)
print("DB servers:", db_hosts)
