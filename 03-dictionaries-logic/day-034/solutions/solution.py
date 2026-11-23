"""
Day 034 — List Comprehension: reference solutions.

Try the tasks in ../tasks.md yourself FIRST.
Then compare your approach with these solutions.

Run from the day folder:  python solutions/solution.py
"""
# ===== Task 1 =====
names = ["asha", "ravi", "meera"]
print([name.title() for name in names])
print([len(name) for name in names])

# ===== Task 2 =====
logs = ["INFO ok", "ERROR db", "WARNING cpu", "ERROR disk", "INFO done"]
errors = [line.split(" ", 1)[1] for line in logs if line.startswith("ERROR")]
levels = [line.split()[0] for line in logs]
counts = {level: levels.count(level) for level in levels}
print(errors)
print(counts)

# ===== Task 3 =====
pods = [
    {"name": "api-1", "cpu_m": 250, "ready": True},
    {"name": "api-2", "cpu_m": 250, "ready": False},
    {"name": "worker-1", "cpu_m": 500, "ready": True},
    {"name": "cron-1", "cpu_m": 100, "ready": True},
]
not_ready = [p["name"] for p in pods if not p["ready"]]
ready_cpu_cores = sum([p["cpu_m"] for p in pods if p["ready"]]) / 1000
cpu_map = {p["name"]: p["cpu_m"] / 1000 for p in pods}
prefixes = {p["name"].split("-")[0] for p in pods}
print("Not ready:", not_ready)
print("Ready CPU (cores):", ready_cpu_cores)
print("CPU map:", cpu_map)
print("Apps:", sorted(prefixes))
